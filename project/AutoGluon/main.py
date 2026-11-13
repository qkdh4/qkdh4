"""
단일 실행 파일:
- python main.py  -> Streamlit 웹앱 자동 실행
- streamlit run main.py -> 같은 웹앱 실행
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from prediction_program import run_prediction
from utils import RESULTS_DIR, build_processed_bundle, ensure_directories

SUPPORTED_CITIES = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"]
AUTOGLUON_ENV_PYTHON = Path(r"C:\Users\504\miniconda3\envs\autogluon-ts311\python.exe")


def _is_running_in_streamlit() -> bool:
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        return get_script_run_ctx() is not None
    except Exception:
        return False


def _auto_run_requested() -> bool:
    return "--auto-run" in sys.argv


def _python_supports_autogluon() -> bool:
    return sys.version_info < (3, 12)


def _recommended_python() -> Path | None:
    if AUTOGLUON_ENV_PYTHON.exists():
        return AUTOGLUON_ENV_PYTHON
    return None


def _load_last_summary() -> dict[str, Any] | None:
    summary_path = RESULTS_DIR / "prediction_summary.json"
    if not summary_path.exists():
        return None
    return json.loads(summary_path.read_text(encoding="utf-8"))


def _render_summary(summary: dict[str, Any]) -> None:
    st.subheader("분석 요약")
    metric_cols = st.columns(4)
    metric_cols[0].metric("도시", summary["city"], border=True)
    metric_cols[1].metric("훈련 모델 수", summary["models_trained"], border=True)
    metric_cols[2].metric(
        "홀드아웃 MAE",
        f"{summary['validation_metrics']['holdout_mae']:.3f}",
        border=True,
    )
    metric_cols[3].metric(
        "홀드아웃 RMSE",
        f"{summary['validation_metrics']['holdout_rmse']:.3f}",
        border=True,
    )

    st.info(summary["interpretation"], icon=":material/insights:")

    forecast_df = pd.DataFrame(summary["next_predictions"])
    forecast_df["date"] = pd.to_datetime(forecast_df["date"])
    st.line_chart(
        forecast_df.set_index("date")["predicted_aqi"],
        y_label="AQI",
        x_label="날짜",
        alt=f"{summary['city']}의 향후 AQI 예측 추세",
    )
    st.dataframe(
        forecast_df,
        hide_index=True,
        alt=f"{summary['city']}의 향후 AQI 예측 표",
    )

    leaderboard_df = pd.DataFrame(summary.get("top_leaderboard", []))
    if not leaderboard_df.empty:
        st.subheader("모델 리더보드 (상위 50개)")
        st.dataframe(
            leaderboard_df,
            hide_index=True,
            alt="AutoGluon 시계열 모델 성능 리더보드",
        )

    run_log_path = summary.get("artifacts", {}).get("run_log")
    if run_log_path:
        log_file = Path(run_log_path)
        if log_file.exists():
            st.subheader("학습 로그")
            log_text = log_file.read_text(encoding="utf-8", errors="replace")
            st.code(log_text[-15000:] if len(log_text) > 15000 else log_text, language="text")


def render_streamlit_app() -> None:
    ensure_directories()
    st.set_page_config(
        page_title="AutoGluon AQI analyzer",
        page_icon=":material/air:",
        layout="wide",
    )
    st.title("AutoGluon TimeSeries AQI 분석")
    st.caption("한 번 실행으로 데이터 준비 → 모델 탐색/HPO → 자동 앙상블 → 결과 저장까지 수행합니다.")

    runtime_supported = _python_supports_autogluon()
    recommended_python = _recommended_python()

    if not runtime_supported:
        st.error(
            f"현재 실행 중인 Python {sys.version_info.major}.{sys.version_info.minor}에서는 "
            "AutoGluon TimeSeries를 사용할 수 없습니다. Python 3.11 환경에서 실행하세요."
        )
        if recommended_python is not None:
            st.code(f"\"{recommended_python}\" \"{Path(__file__).resolve()}\"")

    with st.sidebar:
        st.header("실행 설정")
        city = st.selectbox("도시", SUPPORTED_CITIES, index=0, key="city")
        horizon = st.number_input("예측 일수", min_value=1, max_value=30, value=7, step=1, key="horizon")
        heavy_mode = st.toggle("최대 조합 모드", value=True, key="heavy_mode")

        if heavy_mode:
            train_hours = st.number_input("최대 학습 시간 (시간)", min_value=1, max_value=72, value=8, step=1, key="train_hours")
            num_hpo_trials = st.number_input("HPO 시도 횟수", min_value=10, max_value=5000, value=1000, step=10, key="num_hpo_trials")
            num_val_windows = st.number_input("검증 윈도우 수", min_value=1, max_value=10, value=5, step=1, key="num_val_windows")
        else:
            train_hours = st.number_input("최대 학습 시간 (시간)", min_value=1, max_value=24, value=2, step=1, key="train_hours_light")
            num_hpo_trials = st.number_input("HPO 시도 횟수", min_value=1, max_value=1000, value=200, step=10, key="num_hpo_trials_light")
            num_val_windows = st.number_input("검증 윈도우 수", min_value=1, max_value=5, value=3, step=1, key="num_val_windows_light")

        run_button = st.button(
            "전체 분석 실행",
            type="primary",
            key="run_analysis",
            width="stretch",
            disabled=not runtime_supported,
        )

    if "latest_summary" not in st.session_state:
        st.session_state.latest_summary = _load_last_summary()
    if "analysis_started" not in st.session_state:
        st.session_state.analysis_started = False

    should_auto_run = _auto_run_requested() and not st.session_state.analysis_started and runtime_supported
    if should_auto_run:
        run_button = True

    if run_button:
        st.session_state.analysis_started = True
        status_box = st.status("분석을 시작합니다...", expanded=True)
        try:
            status_box.write("1) 데이터 준비")
            metadata = build_processed_bundle(cities=[city], force_download=False)
            status_box.write(f"준비 완료: {city}, rows={metadata['cities'][city]['rows']}")

            log_path = RESULTS_DIR / "training_run.log"

            def callback(line: str) -> None:
                status_box.write(line)

            summary = run_prediction(
                city=city,
                horizon=int(horizon),
                train_seconds=int(train_hours) * 3600,
                num_val_windows=int(num_val_windows),
                num_hpo_trials=int(num_hpo_trials),
                progress_callback=callback,
                log_path=log_path,
                presets="best_quality",
            )
            st.session_state.latest_summary = summary
            status_box.update(label="분석 완료", state="complete")
        except Exception as exc:
            status_box.update(label="분석 실패", state="error")
            st.exception(exc)

    if st.session_state.latest_summary is not None:
        _render_summary(st.session_state.latest_summary)
    else:
        st.info("아직 실행된 결과가 없습니다. 왼쪽에서 설정 후 '전체 분석 실행'을 눌러주세요.")


def _launch_streamlit() -> None:
    script_path = Path(__file__).resolve()
    launcher_python = Path(sys.executable)
    if not _python_supports_autogluon():
        recommended = _recommended_python()
        if recommended is not None:
            launcher_python = recommended
        else:
            raise RuntimeError(
                "현재 Python 버전은 AutoGluon을 지원하지 않습니다. "
                "Python 3.11 환경을 만들고 그 환경에서 main.py를 실행하세요."
            )

    cmd = [
        str(launcher_python),
        "-m",
        "streamlit",
        "run",
        str(script_path),
        "--",
        "--auto-run",
    ]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if _is_running_in_streamlit():
        render_streamlit_app()
    else:
        _launch_streamlit()
