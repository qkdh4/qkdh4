from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from prediction_program import run_prediction
from utils import RESULTS_DIR


st.set_page_config(page_title="AQI Forecast Studio", page_icon="🌫️", layout="wide")


def inject_style() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
        .hero {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            color: #ffffff; border-radius: 18px; padding: 1.4rem 1.6rem; margin-bottom: 1rem;
        }
        .metric-card {
            background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px;
            padding: 0.9rem 1rem; min-height: 100px;
        }
        .forecast-chip {
            border-radius: 12px; padding: 0.7rem 0.9rem; margin-bottom: 0.6rem; color: #0f172a;
            border: 1px solid rgba(15,23,42,.08);
        }
        .small-label {font-size: 0.8rem; color:#475569; margin-bottom: 0.15rem;}
        .big-value {font-size: 1.5rem; font-weight: 700; line-height: 1.2;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def load_prediction_summary() -> dict | None:
    path = RESULTS_DIR / "prediction_summary.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def band_color(value: float, bands: list[dict]) -> str:
    iv = int(round(float(value)))
    for b in bands:
        if b["min"] <= iv <= b["max"]:
            return b["color"]
    return "#7F1D1D"


def build_forecast_chart(summary: dict) -> go.Figure:
    history = pd.DataFrame(summary["recent_history"])
    preds = pd.DataFrame(summary["next_predictions"])
    rmse = summary["validation_metrics"]["RMSE"]
    bands = summary["aqi_bands"]

    fig = go.Figure()

    # AQI background bands
    min_x = pd.to_datetime(history["date"]).min()
    max_x = pd.to_datetime(preds["date"]).max()
    for b in bands:
        fig.add_hrect(
            y0=b["min"],
            y1=b["max"],
            fillcolor=b["color"],
            opacity=0.08,
            line_width=0,
            layer="below",
        )

    fig.add_trace(
        go.Scatter(
            x=history["date"],
            y=history["aqi"],
            mode="lines",
            name="최근 실제 AQI",
            line=dict(color="#1f2937", width=2),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=preds["date"],
            y=preds["predicted_aqi"],
            mode="lines+markers",
            name="예측 AQI",
            line=dict(color="#2563eb", width=3),
            marker=dict(size=7),
        )
    )
    upper = preds["predicted_aqi"] + rmse
    lower = preds["predicted_aqi"] - rmse
    fig.add_trace(
        go.Scatter(
            x=pd.concat([preds["date"], preds["date"][::-1]]),
            y=pd.concat([upper, lower[::-1]]),
            fill="toself",
            fillcolor="rgba(37,99,235,0.17)",
            line=dict(color="rgba(0,0,0,0)"),
            hoverinfo="skip",
            name=f"불확실성 밴드 (±{rmse:.1f})",
        )
    )

    fig.update_layout(
        title=f"{summary['city']} AQI 예측 ({summary['forecast_horizon_days']}일)",
        xaxis_title="날짜",
        yaxis_title="AQI",
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(orientation="h", y=1.06, x=0),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_yaxes(gridcolor="#e5e7eb")
    fig.update_xaxes(gridcolor="#f1f5f9", range=[min_x, max_x])
    return fig


inject_style()

st.markdown(
    """
    <div class="hero">
      <h2 style="margin:0;">AQI Forecast Studio</h2>
      <p style="margin:0.35rem 0 0 0; opacity:0.92;">
      AQI 추세와 향후 예측값을 대시보드 형태로 확인할 수 있습니다.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("예측 설정")
    city = st.selectbox("도시", ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"], index=0)
    lookback = st.slider("모델 입력 구간(일)", min_value=7, max_value=45, value=21, step=1)
    horizon = st.slider("예측 기간(일)", min_value=1, max_value=14, value=7, step=1)
    run = st.button("예측 갱신", width="stretch")
    st.caption("※ lookback을 늘리면 더 긴 패턴을 반영하지만 과적합 가능성도 있습니다.")

if run:
    with st.spinner("예측 계산 중..."):
        st.session_state["prediction_summary"] = run_prediction(city=city, lookback=lookback, horizon=horizon)
    st.success("예측이 갱신되었습니다.")

summary = st.session_state.get("prediction_summary") or load_prediction_summary()

if summary is None:
    st.info("왼쪽 설정 후 '예측 갱신'을 눌러주세요.")
    st.stop()

nowcast = summary["nowcast"]
stats = summary["forecast_stats"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("내일 예측 AQI", f"{nowcast['next_day_aqi']:.1f}", f"{nowcast['delta_next_day']:+.1f}")
c2.metric("예측 등급", nowcast["current_grade"])
c3.metric("검증 RMSE", f"{summary['validation_metrics']['RMSE']:.1f}")
c4.metric("예측 기간 최고 AQI", f"{stats['max']:.1f}")

st.markdown(
    f"""
    <div class="metric-card">
      <div class="small-label">현재 건강 권고</div>
      <div class="big-value" style="color:{nowcast['current_grade_color']};">{nowcast['current_grade']}</div>
      <div style="margin-top:.35rem;">{nowcast['current_health_advice']}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([2.3, 1.2])

with left:
    st.subheader("예측 트렌드")
    st.plotly_chart(build_forecast_chart(summary), width="stretch")
    st.markdown(f"**해석:** {summary['interpretation']}")

with right:
    st.subheader("예측 카드")
    for row in summary["next_predictions"]:
        st.markdown(
            f"""
            <div class="forecast-chip" style="background:{row['grade_color']}22;">
              <div class="small-label">{row['date']}</div>
              <div class="big-value">{row['predicted_aqi']:.1f} <span style="font-size:1rem;">({row['grade']})</span></div>
              <div style="font-size:0.9rem; margin-top:0.3rem;">{row['health_advice']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.subheader("상세 예측 데이터")
pred_df = pd.DataFrame(summary["next_predictions"])[["date", "predicted_aqi", "grade", "health_advice"]]
st.dataframe(pred_df, width="stretch", hide_index=True)

csv_path = Path(summary["artifacts"]["forecast_csv"])
if csv_path.exists():
    st.download_button(
        "예측 CSV 다운로드",
        data=csv_path.read_bytes(),
        file_name=csv_path.name,
        mime="text/csv",
        width="content",
    )

with st.expander("모델/지표 설명"):
    st.markdown(
        """
        - **모델**: XGBoost 기반 단변량 시계열 예측(최근 AQI 패턴 사용)  
        - **MAE**: 평균 오차 크기(작을수록 좋음)  
        - **RMSE**: 큰 오차에 더 민감한 지표(작을수록 좋음)  
        - **불확실성 밴드**: 예측선 ± RMSE 구간  
        """
    )
