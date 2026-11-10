from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

from utils import (
    RESULTS_DIR,
    build_processed_bundle,
    configure_korean_matplotlib,
    ensure_directories,
    load_prepared_city_data,
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


def build_univariate_windows(series: pd.Series, lookback: int) -> tuple[np.ndarray, np.ndarray]:
    values = series.values.astype(float)
    X, y = [], []
    for i in range(len(values) - lookback):
        X.append(values[i : i + lookback])
        y.append(values[i + lookback])
    return np.array(X), np.array(y)


def recursive_forecast(model: XGBRegressor, history: List[float], lookback: int, horizon: int) -> List[float]:
    buffer = history[-lookback:].copy()
    preds: List[float] = []
    for _ in range(horizon):
        x = np.array(buffer[-lookback:]).reshape(1, -1)
        pred = float(model.predict(x)[0])
        preds.append(pred)
        buffer.append(pred)
    return preds


def get_aqi_band(aqi_value: float) -> Dict[str, str | int]:
    value = int(round(float(aqi_value)))
    for band in AQI_BANDS:
        if band["min"] <= value <= band["max"]:
            return band
    return AQI_BANDS[-1]


def classify_forecast_rows(next_dates: pd.DatetimeIndex, next_values: List[float]) -> List[dict]:
    rows = []
    for d, v in zip(next_dates, next_values):
        band = get_aqi_band(v)
        rows.append(
            {
                "date": d.strftime("%Y-%m-%d"),
                "predicted_aqi": float(v),
                "grade": band["label"],
                "health_advice": band["advice"],
                "grade_color": band["color"],
            }
        )
    return rows


def run_prediction(city: str = "Delhi", lookback: int = 14, horizon: int = 7) -> dict:
    ensure_directories()
    configure_korean_matplotlib()
    build_processed_bundle(cities=[city], force_download=False)

    df = load_prepared_city_data(city)
    # 원본 이상치/입력 오류로 인한 스케일 왜곡을 막기 위해 AQI 물리 범위를 클리핑
    aqi = df["AQI"].clip(lower=0, upper=500).copy()

    X, y = build_univariate_windows(aqi, lookback=lookback)
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = XGBRegressor(
        n_estimators=350,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
    )
    model.fit(X_train, y_train, verbose=False)

    y_pred = model.predict(X_test)
    mae = float(mean_absolute_error(y_test, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))

    history_values = aqi.tolist()
    next_values = recursive_forecast(model, history=history_values, lookback=lookback, horizon=horizon)
    next_dates = pd.date_range(start=aqi.index.max() + pd.Timedelta(days=1), periods=horizon, freq="D")
    forecast_rows = classify_forecast_rows(next_dates, next_values)

    forecast_df = pd.DataFrame(forecast_rows)
    forecast_csv = RESULTS_DIR / "next_aqi_forecast.csv"
    forecast_df.to_csv(forecast_csv, index=False, encoding="utf-8-sig")

    plt.figure(figsize=(14, 6))
    tail_days = min(120, len(aqi))
    plt.plot(aqi.index[-tail_days:], aqi.iloc[-tail_days:], color="#2C3E50", linewidth=2, label="최근 실제 AQI")
    plt.plot(next_dates, next_values, color="#2563EB", linewidth=2.5, marker="o", label="다음 AQI 예측")
    plt.fill_between(
        next_dates,
        np.array(next_values) - rmse,
        np.array(next_values) + rmse,
        color="#60A5FA",
        alpha=0.2,
        label=f"예측 불확실성(±RMSE={rmse:.2f})",
    )
    plt.title(f"{city} AQI 예측 ({horizon}일)")
    plt.xlabel("날짜")
    plt.ylabel("AQI")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    forecast_png = RESULTS_DIR / "next_aqi_forecast.png"
    plt.savefig(forecast_png, dpi=300, bbox_inches="tight")
    plt.close()

    last_actual = float(aqi.iloc[-1])
    first_forecast = float(next_values[0])
    delta_next_day = float(first_forecast - last_actual)
    trend_text = "상승" if delta_next_day > 0 else "하락" if delta_next_day < 0 else "보합"
    peak_value = float(max(next_values))
    peak_band = get_aqi_band(peak_value)
    latest_band = get_aqi_band(first_forecast)

    recent_tail = df.reset_index()[["Date", "AQI"]].tail(120).copy()
    recent_tail["Date"] = recent_tail["Date"].dt.strftime("%Y-%m-%d")

    interpretation = (
        f"내일 AQI는 최근 대비 {delta_next_day:+.1f}p ({trend_text})로 예측됩니다. "
        f"예측 기간 중 최고 위험 구간은 '{peak_band['label']}' 수준입니다. "
        "밴드(±RMSE)가 넓은 날짜는 변동성이 큰 구간으로 해석하세요."
    )

    summary = {
        "city": city,
        "lookback_days": lookback,
        "forecast_horizon_days": horizon,
        "validation_metrics": {"MAE": mae, "RMSE": rmse},
        "nowcast": {
            "last_actual_aqi": last_actual,
            "next_day_aqi": first_forecast,
            "delta_next_day": delta_next_day,
            "trend": trend_text,
            "current_grade": latest_band["label"],
            "current_grade_color": latest_band["color"],
            "current_health_advice": latest_band["advice"],
        },
        "next_predictions": forecast_rows,
        "forecast_stats": {
            "mean": float(np.mean(next_values)),
            "min": float(np.min(next_values)),
            "max": peak_value,
            "peak_grade": peak_band["label"],
            "peak_grade_color": peak_band["color"],
            "peak_advice": peak_band["advice"],
        },
        "recent_history": recent_tail.rename(columns={"Date": "date", "AQI": "aqi"}).to_dict(orient="records"),
        "artifacts": {
            "forecast_csv": str(forecast_csv),
            "forecast_png": str(forecast_png),
        },
        "interpretation": interpretation,
        "aqi_bands": AQI_BANDS,
    }
    save_result_summary("prediction_summary.json", summary)
    return summary


def main():
    summary = run_prediction(city="Delhi", lookback=14, horizon=7)
    print("=" * 60)
    print("AQI 예측 프로그램 실행 완료")
    print("=" * 60)
    print(f"도시: {summary['city']}")
    print(f"검증 MAE: {summary['validation_metrics']['MAE']:.4f}")
    print(f"검증 RMSE: {summary['validation_metrics']['RMSE']:.4f}")
    print(f"내일 예측: {summary['nowcast']['next_day_aqi']:.2f} ({summary['nowcast']['current_grade']})")
    print("예측 파일:")
    print(f"  - {summary['artifacts']['forecast_png']}")
    print(f"  - {summary['artifacts']['forecast_csv']}")


if __name__ == "__main__":
    main()
