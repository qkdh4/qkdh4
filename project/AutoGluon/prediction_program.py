from __future__ import annotations

import contextlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, TextIO

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import (
    MODELS_DIR,
    RESULTS_DIR,
    build_processed_bundle,
    configure_matplotlib_font,
    ensure_directories,
    load_prepared_city_data,
    prune_model_directories,
    save_result_summary,
)

AQI_BANDS = [
    {"min": 0, "max": 50, "label": "좋음", "color": "#2ECC71", "advice": "야외 활동에 제약이 거의 없습니다."},
    {"min": 51, "max": 100, "label": "보통", "color": "#F1C40F", "advice": "민감군은 장시간 야외 활동을 조절하세요."},
    {"min": 101, "max": 150, "label": "민감군 주의", "color": "#E67E22", "advice": "호흡기 질환자는 마스크 착용을 권장합니다."},
    {"min": 151, "max": 200, "label": "나쁨", "color": "#E74C3C", "advice": "실외 운동을 줄이고 실내 공기질 관리가 필요합니다."},
    {"min": 201, "max": 300, "label": "매우 나쁨", "color": "#8E44AD", "advice": "외출을 최소화하고 공기청정기 사용을 권장합니다."},
    {"min": 301, "max": 500, "label": "위험", "color": "#7F1D1D", "advice": "가급적 외출을 피하고 건강 이상 시 즉시 휴식하세요."},
]

UNIFORM_MODEL_FAMILIES: list[str] = [
    "SeasonalNaive",
    "AutoETS",
    "DynamicOptimizedTheta",
    "ETS",
    "Theta",
    "NPTS",
    "RecursiveTabular",
    "DirectTabular",
    "DeepAR",
    "TemporalFusionTransformer",
]


def _import_autogluon():
    if sys.version_info >= (3, 12):
        raise ImportError(
            f"현재 Python {sys.version_info.major}.{sys.version_info.minor} 환경에서는 "
            "autogluon.timeseries를 설치/사용할 수 없습니다. Python 3.11 환경에서 실행하세요."
        )
    try:
        from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor
    except ImportError as exc:
        raise ImportError(
            "AutoGluon TimeSeries가 설치되어 있지 않습니다. "
            "먼저 `pip install -r requirements.txt`를 실행하세요."
        ) from exc
    return TimeSeriesDataFrame, TimeSeriesPredictor


def get_aqi_band(aqi_value: float) -> Dict[str, str | int]:
    value = int(round(float(aqi_value)))
    for band in AQI_BANDS:
        if band["min"] <= value <= band["max"]:
            return band
    return AQI_BANDS[-1]


def classify_forecast_rows(predictions: pd.DataFrame) -> List[dict]:
    rows: List[dict] = []
    for _, row in predictions.iterrows():
        band = get_aqi_band(row["predicted_aqi"])
        rows.append(
            {
                "date": row["date"],
                "predicted_aqi": float(row["predicted_aqi"]),
                "grade": band["label"],
                "health_advice": band["advice"],
                "grade_color": band["color"],
            }
        )
    return rows


def prepare_autogluon_timeseries(city: str = "Delhi") -> pd.DataFrame:
    df = load_prepared_city_data(city)
    target = df[["Date", "AQI"]].copy()
    target["AQI"] = target["AQI"].clip(lower=0, upper=500)
    target = target.dropna(subset=["AQI"]).sort_values("Date")
    target["item_id"] = city
    target["timestamp"] = target["Date"]
    target["target"] = target["AQI"].astype(float)
    return target[["item_id", "timestamp", "target"]]


def _append_log(log_path: Path | None, message: str) -> None:
    if not log_path:
        return
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(message + "\n")


def _notify(
    message: str,
    progress_callback: Callable[[str], None] | None = None,
    log_path: Path | None = None,
) -> None:
    stamped = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    _append_log(log_path, stamped)
    if progress_callback is not None:
        progress_callback(stamped)


class _Tee:
    def __init__(self, *streams: TextIO):
        self.streams = streams
        self.encoding = getattr(streams[0], "encoding", "utf-8") if streams else "utf-8"

    def write(self, data: str) -> int:
        written = 0
        for stream in self.streams:
            written = stream.write(data)
        return written

    def flush(self) -> None:
        for stream in self.streams:
            stream.flush()

    def __getattr__(self, name: str):
        if self.streams:
            return getattr(self.streams[0], name)
        raise AttributeError(name)


def _build_hyperparameters(use_hpo: bool) -> str | dict[str, Any]:
    if not use_hpo:
        return "default"

    from autogluon.common import space

    return {
        "SeasonalNaive": {},
        "AutoETS": {},
        "DynamicOptimizedTheta": {},
        "RecursiveTabular": {},
        "DirectTabular": {},
        "TemporalFusionTransformer": {
            "hidden_dim": space.Int(16, 64),
            "dropout_rate": space.Categorical(0.1, 0.3),
        },
        "DeepAR": {
            "hidden_size": space.Int(32, 256),
            "dropout_rate": space.Categorical(0.1, 0.3, 0.5),
            "num_layers": space.Int(1, 3),
        },
    }


def _build_fast_hyperparameters() -> dict[str, Any]:
    return {
        "SeasonalNaive": {},
        "AutoETS": {},
        "DynamicOptimizedTheta": {},
        "RecursiveTabular": {},
        "DirectTabular": {},
    }


def _build_uniform_hyperparameters(variants_per_family: int = 2) -> dict[str, list[dict[str, Any]]]:
    safe_variants = max(1, int(variants_per_family))
    hyperparameters: dict[str, list[dict[str, Any]]] = {}
    for family in UNIFORM_MODEL_FAMILIES:
        variants: list[dict[str, Any]] = []
        for idx in range(1, safe_variants + 1):
            variants.append({"ag_args": {"name_suffix": f"U{idx:02d}"}})
        hyperparameters[family] = variants
    return hyperparameters


def _build_fit_log_payload(fit_kwargs: dict[str, Any], hyperparameter_mode: str) -> dict[str, Any]:
    payload = {
        "presets": fit_kwargs.get("presets"),
        "hyperparameters": hyperparameter_mode,
        "num_val_windows": fit_kwargs.get("num_val_windows"),
        "time_limit": fit_kwargs.get("time_limit"),
        "hyperparameter_tune_kwargs": fit_kwargs.get("hyperparameter_tune_kwargs"),
    }
    return payload


def run_prediction(
    city: str = "Delhi",
    horizon: int = 7,
    train_seconds: int | None = 28800,
    num_val_windows: int = 5,
    num_hpo_trials: int = 1000,
    uniform_model_budget: bool = True,
    uniform_variants_per_family: int = 2,
    progress_callback: Callable[[str], None] | None = None,
    log_path: str | Path | None = None,
    presets: str = "best_quality",
) -> dict:
    ensure_directories()
    configure_matplotlib_font()
    resolved_log_path = Path(log_path) if log_path else None
    if resolved_log_path and resolved_log_path.exists():
        resolved_log_path.unlink()

    _notify("데이터 번들 준비를 시작합니다.", progress_callback, resolved_log_path)
    build_processed_bundle(cities=[city], force_download=False)
    _notify("AutoGluon 모듈을 로드합니다.", progress_callback, resolved_log_path)
    TimeSeriesDataFrame, TimeSeriesPredictor = _import_autogluon()

    ts_df = prepare_autogluon_timeseries(city)
    if len(ts_df) <= horizon * 3:
        raise ValueError(f"훈련 데이터가 부족합니다. 최소 {horizon * 3 + 1}행 이상 필요합니다.")

    train_df = ts_df.iloc[:-horizon].copy()
    test_df = ts_df.iloc[-horizon:].copy()

    train_data = TimeSeriesDataFrame.from_data_frame(train_df, id_column="item_id", timestamp_column="timestamp")
    full_data = TimeSeriesDataFrame.from_data_frame(ts_df, id_column="item_id", timestamp_column="timestamp")

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    prune_model_directories(city=city, keep_last_n=4)
    model_path = MODELS_DIR / f"autogluon_timeseries_{city.lower()}_{run_id}"
    predictor = TimeSeriesPredictor(
        path=str(model_path),
        target="target",
        prediction_length=horizon,
        eval_metric="RMSE",
        freq="D",
    )

    use_hpo = num_hpo_trials > 0 and (train_seconds is None or train_seconds >= 60)
    if num_hpo_trials > 0 and not use_hpo:
        _notify(
            "학습 시간이 짧아 HPO를 자동 비활성화하고 기본 탐색으로 실행합니다.",
            progress_callback,
            resolved_log_path,
        )
    if uniform_model_budget and use_hpo:
        _notify(
            "균일 모델수 모드가 활성화되어 HPO를 비활성화합니다.",
            progress_callback,
            resolved_log_path,
        )
        use_hpo = False
    if use_hpo:
        os.environ.setdefault("RAY_TRAIN_ENABLE_V2_MIGRATION_WARNINGS", "0")

    short_run_mode = train_seconds is not None and train_seconds < 900
    if short_run_mode and not use_hpo and not uniform_model_budget:
        _notify(
            "짧은 시간 제한 감지: 무거운 사전학습 모델을 제외한 경량 모델셋으로 실행합니다.",
            progress_callback,
            resolved_log_path,
        )

    if uniform_model_budget:
        hyperparameters = _build_uniform_hyperparameters(variants_per_family=uniform_variants_per_family)
        hyperparameter_mode = "uniform_model_budget"
    elif short_run_mode and not use_hpo:
        hyperparameters = _build_fast_hyperparameters()
        hyperparameter_mode = "fast_model_set"
    else:
        hyperparameters = _build_hyperparameters(use_hpo=use_hpo)
        hyperparameter_mode = "search_space" if use_hpo else "default"

    fit_kwargs = {
        "train_data": train_data,
        "presets": presets,
        "hyperparameters": hyperparameters,
        "num_val_windows": num_val_windows,
    }
    if train_seconds:
        fit_kwargs["time_limit"] = train_seconds
    if use_hpo:
        fit_kwargs["hyperparameter_tune_kwargs"] = {
            "num_trials": num_hpo_trials,
            "scheduler": "local",
            "searcher": "random",
        }

    _notify(
        "모델 탐색/학습을 시작합니다. 시간이 오래 걸릴 수 있습니다.",
        progress_callback,
        resolved_log_path,
    )
    _append_log(
        resolved_log_path,
        json.dumps(
            {"fit_config": _build_fit_log_payload(fit_kwargs, hyperparameter_mode=hyperparameter_mode)},
            ensure_ascii=False,
            default=str,
        ),
    )
    hpo_effective = use_hpo
    try:
        if resolved_log_path:
            with resolved_log_path.open("a", encoding="utf-8") as raw_log:
                tee_out = _Tee(sys.stdout, raw_log)
                tee_err = _Tee(sys.stderr, raw_log)
                with contextlib.redirect_stdout(tee_out), contextlib.redirect_stderr(tee_err):
                    predictor.fit(**fit_kwargs)
        else:
            predictor.fit(**fit_kwargs)
    except ValueError as exc:
        message = str(exc)
        if use_hpo and "no model contains a hyperparameter search space" in message:
            _notify(
                "HPO 탐색공간을 인식하지 못해 HPO를 비활성화하고 재시도합니다.",
                progress_callback,
                resolved_log_path,
            )
            hpo_effective = False
            fit_kwargs["hyperparameters"] = "default"
            fit_kwargs.pop("hyperparameter_tune_kwargs", None)
            if resolved_log_path:
                with resolved_log_path.open("a", encoding="utf-8") as raw_log:
                    tee_out = _Tee(sys.stdout, raw_log)
                    tee_err = _Tee(sys.stderr, raw_log)
                    with contextlib.redirect_stdout(tee_out), contextlib.redirect_stderr(tee_err):
                        predictor.fit(**fit_kwargs)
            else:
                predictor.fit(**fit_kwargs)
        else:
            raise
    except (AssertionError, ImportError, ModuleNotFoundError) as exc:
        message = str(exc)
        hpo_runtime_issue = any(
            token in message
            for token in [
                "HyperOpt must be installed",
                "ray.tune",
                "No module named 'ray'",
            ]
        )
        if use_hpo and hpo_runtime_issue:
            _notify(
                f"HPO 런타임 의존성 문제({message})로 HPO를 비활성화하고 재시도합니다.",
                progress_callback,
                resolved_log_path,
            )
            hpo_effective = False
            fit_kwargs["hyperparameters"] = "default"
            fit_kwargs.pop("hyperparameter_tune_kwargs", None)
            if resolved_log_path:
                with resolved_log_path.open("a", encoding="utf-8") as raw_log:
                    tee_out = _Tee(sys.stdout, raw_log)
                    tee_err = _Tee(sys.stderr, raw_log)
                    with contextlib.redirect_stdout(tee_out), contextlib.redirect_stderr(tee_err):
                        predictor.fit(**fit_kwargs)
            else:
                predictor.fit(**fit_kwargs)
        else:
            raise
    _notify("모델 학습이 완료되었습니다.", progress_callback, resolved_log_path)

    leaderboard = predictor.leaderboard(data=full_data, silent=True)
    leaderboard_path = RESULTS_DIR / "model_leaderboard.csv"
    leaderboard.to_csv(leaderboard_path, index=False, encoding="utf-8-sig")
    _notify("리더보드를 저장했습니다.", progress_callback, resolved_log_path)

    holdout_forecast = predictor.predict(train_data).reset_index().sort_values("timestamp")
    holdout_forecast["predicted_aqi"] = holdout_forecast["mean"].clip(lower=0, upper=500)

    future_forecast = predictor.predict(full_data).reset_index().sort_values("timestamp")
    future_forecast["date"] = pd.to_datetime(future_forecast["timestamp"]).dt.strftime("%Y-%m-%d")
    future_forecast["predicted_aqi"] = future_forecast["mean"].clip(lower=0, upper=500)
    _notify("홀드아웃/미래 예측을 생성했습니다.", progress_callback, resolved_log_path)

    forecast_rows = classify_forecast_rows(future_forecast[["date", "predicted_aqi"]])
    forecast_df = pd.DataFrame(forecast_rows)
    forecast_csv = RESULTS_DIR / "next_aqi_forecast.csv"
    forecast_df.to_csv(forecast_csv, index=False, encoding="utf-8-sig")

    test_actual = test_df["target"].to_numpy(dtype=float)
    test_pred = holdout_forecast["predicted_aqi"].to_numpy(dtype=float)
    if len(test_actual) != len(test_pred):
        raise ValueError("홀드아웃 구간 길이와 예측 길이가 일치하지 않습니다.")
    holdout_rmse = float(np.sqrt(np.mean(np.square(test_actual - test_pred))))
    holdout_mae = float(np.mean(np.abs(test_actual - test_pred)))

    historical = ts_df["target"].to_numpy(dtype=float)
    future_dates = pd.to_datetime(future_forecast["timestamp"])
    future_pred = future_forecast["predicted_aqi"].to_numpy(dtype=float)

    plt.figure(figsize=(14, 6))
    history_tail = min(len(historical), 180)
    history_dates = pd.to_datetime(ts_df["timestamp"].iloc[-history_tail:])
    plt.plot(history_dates, historical[-history_tail:], label="Observed AQI", color="#2C3E50", linewidth=2)
    plt.plot(future_dates, future_pred, label="AutoGluon Forecast AQI", color="#2563EB", linewidth=2.5, marker="o")
    plt.title(f"{city} AQI AutoGluon(TimeSeries) {horizon}-Day Forecast")
    plt.xlabel("Date")
    plt.ylabel("AQI")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    forecast_png = RESULTS_DIR / "next_aqi_forecast.png"
    plt.savefig(forecast_png, dpi=300, bbox_inches="tight")
    plt.close()
    _notify("예측 시각화 파일을 저장했습니다.", progress_callback, resolved_log_path)

    best_model = str(leaderboard.iloc[0]["model"]) if len(leaderboard) > 0 else "unknown"
    ensemble_models = leaderboard[leaderboard["model"].astype(str).str.contains("WeightedEnsemble", na=False)]
    interpretation = (
        "AutoGluon TimeSeries가 다양한 시계열 모델/하이퍼파라미터 조합을 탐색하고 "
        "성능 상위 모델을 자동 앙상블했습니다."
    )

    summary = {
        "city": city,
        "forecast_horizon_days": horizon,
        "training_options": {
            "presets": presets,
            "hyperparameters": hyperparameter_mode if not hpo_effective else "search_space",
            "time_limit_seconds": train_seconds,
            "num_val_windows": num_val_windows,
            "num_hpo_trials": num_hpo_trials if hpo_effective else 0,
            "uniform_model_budget": uniform_model_budget,
            "uniform_family_count": len(UNIFORM_MODEL_FAMILIES) if uniform_model_budget else 0,
            "uniform_variants_per_family": uniform_variants_per_family if uniform_model_budget else 0,
        },
        "validation_metrics": {
            "holdout_mae": holdout_mae,
            "holdout_rmse": holdout_rmse,
        },
        "best_model": best_model,
        "models_trained": int(len(leaderboard)),
        "ensemble_models": ensemble_models["model"].astype(str).tolist(),
        "next_predictions": forecast_rows,
        "artifacts": {
            "forecast_csv": str(forecast_csv),
            "forecast_png": str(forecast_png),
            "leaderboard_csv": str(leaderboard_path),
            "model_path": str(model_path),
            "run_log": str(resolved_log_path) if resolved_log_path else None,
        },
        "interpretation": interpretation,
        "aqi_bands": AQI_BANDS,
        "top_leaderboard": leaderboard.head(50).replace({np.nan: None}).to_dict(orient="records"),
    }
    save_result_summary("prediction_summary.json", json.loads(json.dumps(summary, default=str)))
    prune_model_directories(city=city, keep_last_n=5)
    _notify("요약 결과 저장을 완료했습니다.", progress_callback, resolved_log_path)
    return summary


def main() -> None:
    summary = run_prediction(city="Delhi", horizon=7)
    print("=" * 70)
    print("AutoGluon TimeSeries AQI 예측 완료")
    print("=" * 70)
    print(f"도시: {summary['city']}")
    print(f"Best model: {summary['best_model']}")
    print(f"훈련된 모델 수: {summary['models_trained']}")
    print(f"검증 MAE: {summary['validation_metrics']['holdout_mae']:.4f}")
    print(f"검증 RMSE: {summary['validation_metrics']['holdout_rmse']:.4f}")
    print("생성 파일:")
    print(f"  - {summary['artifacts']['forecast_png']}")
    print(f"  - {summary['artifacts']['forecast_csv']}")
    print(f"  - {summary['artifacts']['leaderboard_csv']}")
    print(f"  - {summary['artifacts']['model_path']}")


if __name__ == "__main__":
    main()
