import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


st.set_page_config(page_title="시계열 ML 분석 대시보드", layout="wide")
st.title("시계열 머신러닝 분석 대시보드")


def load_summary(filename: str) -> dict | None:
    path = RESULTS_DIR / filename
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def run_full_pipeline() -> tuple[bool, str]:
    command = [sys.executable, "main.py"]
    proc = subprocess.run(
        command,
        cwd=str(BASE_DIR),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    logs = (proc.stdout or "") + "\n" + (proc.stderr or "")
    return proc.returncode == 0, logs


with st.sidebar:
    st.header("실행")
    if st.button("전체 분석 다시 실행", width="stretch"):
        with st.spinner("분석 실행 중..."):
            ok, logs = run_full_pipeline()
        if ok:
            st.success("분석 실행이 완료되었습니다.")
        else:
            st.error("분석 중 오류가 발생했습니다. 로그를 확인하세요.")
        st.session_state["last_logs"] = logs

    if "last_logs" in st.session_state:
        with st.expander("최근 실행 로그"):
            st.code(st.session_state["last_logs"][:12000], language="text")


st.subheader("데이터셋 요약")
meta_path = PROCESSED_DIR / "dataset_metadata.json"
if meta_path.exists():
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    rows = []
    for city, info in meta.get("cities", {}).items():
        rows.append(
            {
                "city": city,
                "rows": info.get("rows"),
                "start_date": info.get("start_date"),
                "end_date": info.get("end_date"),
            }
        )
    if rows:
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    st.caption(f"features: {', '.join(meta.get('features', []))}")
    st.caption(f"target: {meta.get('target', 'AQI')}")
else:
    st.warning("dataset_metadata.json 파일이 없습니다. 먼저 main.py 또는 prepare_dataset.py를 실행하세요.")


tabs = st.tabs(
    [
        "1) 예측 결과",
        "2) 이상치 탐지",
        "3) 결측치 보간",
        "4) 보간 오차 비교",
        "코드/분석 설명",
    ]
)


def show_image(tab, path: Path, title: str):
    with tab:
        st.subheader(title)
        if path.exists():
            st.image(str(path), width="stretch")
        else:
            st.info(f"{path.name} 파일이 아직 없습니다. 전체 분석을 실행하세요.")


show_image(tabs[0], RESULTS_DIR / "project1_predictions.png", "프로젝트 1: LSTM / XGBoost 예측 비교")
show_image(tabs[1], RESULTS_DIR / "project2_anomalies.png", "프로젝트 2: 이상치 탐지 결과")
show_image(tabs[2], RESULTS_DIR / "project3_imputation.png", "프로젝트 3: 보간 결과 비교")
show_image(tabs[3], RESULTS_DIR / "project3_errors.png", "프로젝트 3: 보간 오차(MAE/RMSE)")

with tabs[0]:
    summary = load_summary("project1_summary.json")
    st.markdown("#### 해석")
    if summary:
        metric_rows = [
            {
                "모델": model,
                "MAE": values["MAE"],
                "RMSE": values["RMSE"],
            }
            for model, values in summary["metrics"].items()
        ]
        st.dataframe(pd.DataFrame(metric_rows), width="stretch", hide_index=True)
        st.success(f"RMSE 기준 추천 모델: **{summary['best_model_by_rmse']}**")
        st.write(summary["interpretation"])
        st.caption(f"적용 폰트: {summary.get('font_used', '-')}")
    else:
        st.info("요약 파일이 없습니다. 전체 분석을 다시 실행하세요.")

with tabs[1]:
    summary = load_summary("project2_summary.json")
    st.markdown("#### 해석")
    if summary:
        counts = summary["anomaly_counts"]
        ratios = summary["ratios"]
        st.write(
            f"- Autoencoder 이상치: **{counts['autoencoder']}개** ({ratios['autoencoder_pct']:.2f}%)\n"
            f"- Isolation Forest 이상치: **{counts['isolation_forest']}개** ({ratios['isolation_forest_pct']:.2f}%)\n"
            f"- 합의 이상치: **{counts['consensus']}개** ({ratios['consensus_pct_of_test']:.2f}%)"
        )
        st.write(summary["interpretation"])
        st.caption(f"적용 폰트: {summary.get('font_used', '-')}")
    else:
        st.info("요약 파일이 없습니다. 전체 분석을 다시 실행하세요.")

with tabs[2]:
    st.markdown("#### 해석")
    st.write(
        "- 검은 선은 기준(원본) 시계열, 색 선은 보간 결과입니다.\n"
        "- 피크/급락 구간에서 원본 선과 더 밀착될수록 보간 품질이 좋습니다."
    )

with tabs[3]:
    summary = load_summary("project3_summary.json")
    st.markdown("#### 해석")
    if summary:
        st.dataframe(pd.DataFrame(summary["pm25_metrics"]), width="stretch", hide_index=True)
        st.success(f"PM2.5 기준 추천 보간법: **{summary['best_method_by_rmse']}**")
        st.write(summary["interpretation"])
        st.caption(f"적용 폰트: {summary.get('font_used', '-')}")
    else:
        st.info("요약 파일이 없습니다. 전체 분석을 다시 실행하세요.")

with tabs[4]:
    st.subheader("분석 기법별 데이터 활용")
    st.markdown(
        """
        - **예측(프로젝트1)**: 과거 7일의 `PM2.5, PM10, NO2, SO2, CO, O3, AQI`로 다음날 `AQI` 예측  
        - **이상치 탐지(프로젝트2)**: 7일 윈도우를 정규화 후 Autoencoder 재구성오차 + IsolationForest로 이상치 탐지  
        - **결측치 보간(프로젝트3)**: 10% 결측치를 인위적으로 만든 뒤 Forward/Linear/Polynomial/KNN/Spline 비교  
        """
    )
    st.subheader("핵심 코드 위치")
    st.markdown(
        """
        - 데이터 다운로드/정제: `utils.py` (`build_processed_bundle`, `preprocess_city_data`)  
        - 전체 실행: `main.py`  
        - 예측 모델: `project1_multivariate_forecasting.py`  
        - 이상치 탐지: `project2_anomaly_detection.py`  
        - 보간 비교: `project3_imputation.py`
        """
    )
