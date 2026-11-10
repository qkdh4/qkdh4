const citySelect = document.getElementById("citySelect");
const lookbackInput = document.getElementById("lookbackInput");
const horizonInput = document.getElementById("horizonInput");
const lookbackVal = document.getElementById("lookbackVal");
const horizonVal = document.getElementById("horizonVal");
const predictBtn = document.getElementById("predictBtn");
const statusBox = document.getElementById("statusBox");

const kpiNextAqi = document.getElementById("kpiNextAqi");
const kpiGrade = document.getElementById("kpiGrade");
const kpiRmse = document.getElementById("kpiRmse");
const kpiPeak = document.getElementById("kpiPeak");
const trendSummary = document.getElementById("trendSummary");

const forecastTableBody = document.querySelector("#forecastTable tbody");
const forecastCards = document.getElementById("forecastCards");

let chart;

function setStatus(text, ok = true) {
  statusBox.textContent = text;
  statusBox.style.background = ok ? "#0b3a74" : "#7f1d1d";
}

function bandColor(value, bands) {
  const iv = Math.round(value);
  for (const b of bands) {
    if (iv >= b.min && iv <= b.max) return b.color;
  }
  return "#7f1d1d";
}

function renderChart(summary) {
  const ctx = document.getElementById("forecastChart").getContext("2d");
  const history = summary.recent_history || [];
  const preds = summary.next_predictions || [];
  const rmse = summary.validation_metrics.RMSE;
  const bands = summary.aqi_bands || [];

  const historyLabels = history.map((r) => r.date);
  const predLabels = preds.map((r) => r.date);
  const labels = [...historyLabels, ...predLabels];

  const historyData = [...history.map((r) => r.aqi), ...Array(preds.length).fill(null)];
  const predData = [...Array(history.length - 1).fill(null), history[history.length - 1]?.aqi ?? null, ...preds.map((r) => r.predicted_aqi)];

  const upper = [...Array(history.length).fill(null), ...preds.map((r) => r.predicted_aqi + rmse)];
  const lower = [...Array(history.length).fill(null), ...preds.map((r) => r.predicted_aqi - rmse)];

  if (chart) chart.destroy();

  const bandPlugin = {
    id: "aqiBands",
    beforeDraw(c) {
      const { ctx, chartArea, scales } = c;
      if (!chartArea || !scales?.y) return;
      const { left, right, top, bottom } = chartArea;
      for (const b of bands) {
        const yTop = scales.y.getPixelForValue(b.max);
        const yBottom = scales.y.getPixelForValue(b.min);
        ctx.save();
        ctx.globalAlpha = 0.1;
        ctx.fillStyle = b.color;
        ctx.fillRect(left, yTop, right - left, yBottom - yTop);
        ctx.restore();
      }
      ctx.save();
      ctx.strokeStyle = "#e5e7eb";
      ctx.strokeRect(left, top, right - left, bottom - top);
      ctx.restore();
    },
  };

  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "최근 실제 AQI",
          data: historyData,
          borderColor: "#1f2937",
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.2,
        },
        {
          label: "예측 AQI",
          data: predData,
          borderColor: "#2563eb",
          borderWidth: 2.5,
          pointRadius: 3,
          tension: 0.25,
        },
        {
          label: `불확실성 상한 (+${rmse.toFixed(1)})`,
          data: upper,
          borderColor: "rgba(96,165,250,.2)",
          pointRadius: 0,
          borderWidth: 1,
        },
        {
          label: `불확실성 하한 (-${rmse.toFixed(1)})`,
          data: lower,
          borderColor: "rgba(96,165,250,.2)",
          pointRadius: 0,
          borderWidth: 1,
          fill: "-1",
          backgroundColor: "rgba(96,165,250,.2)",
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          ticks: { maxRotation: 0, autoSkip: true, maxTicksLimit: 12 },
          grid: { color: "#f1f5f9" },
        },
        y: {
          beginAtZero: true,
          title: { display: true, text: "AQI" },
          grid: { color: "#e5e7eb" },
        },
      },
      plugins: {
        legend: { position: "top" },
      },
    },
    plugins: [bandPlugin],
  });
}

function renderTable(summary) {
  forecastTableBody.innerHTML = "";
  for (const row of summary.next_predictions) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.date}</td>
      <td>${row.predicted_aqi.toFixed(1)}</td>
      <td><span style="font-weight:700;color:${row.grade_color};">${row.grade}</span></td>
      <td>${row.health_advice}</td>
    `;
    forecastTableBody.appendChild(tr);
  }
}

function renderCards(summary) {
  forecastCards.innerHTML = "";
  for (const row of summary.next_predictions) {
    const card = document.createElement("article");
    card.className = "forecast-card";
    card.style.background = `${row.grade_color}22`;
    card.innerHTML = `
      <div class="date">${row.date}</div>
      <div class="aqi">${row.predicted_aqi.toFixed(1)} (${row.grade})</div>
      <div class="advice">${row.health_advice}</div>
    `;
    forecastCards.appendChild(card);
  }
}

function renderSummary(summary) {
  const now = summary.nowcast;
  const stats = summary.forecast_stats;
  const bands = summary.aqi_bands;

  kpiNextAqi.textContent = `${now.next_day_aqi.toFixed(1)} (${now.delta_next_day >= 0 ? "+" : ""}${now.delta_next_day.toFixed(1)})`;
  kpiGrade.textContent = now.current_grade;
  kpiGrade.style.color = now.current_grade_color;
  kpiRmse.textContent = summary.validation_metrics.RMSE.toFixed(1);
  kpiPeak.textContent = `${stats.max.toFixed(1)} (${stats.peak_grade})`;

  trendSummary.textContent = summary.interpretation;

  renderTable(summary);
  renderCards(summary);
  renderChart(summary);
}

async function fetchJSON(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || `${res.status} ${res.statusText}`);
  }
  return res.json();
}

async function init() {
  try {
    setStatus("초기화 중...");
    const optionData = await fetchJSON("/api/options");
    citySelect.innerHTML = optionData.cities.map((c) => `<option value="${c}">${c}</option>`).join("");
    citySelect.value = optionData.defaults.city;
    lookbackInput.value = optionData.defaults.lookback;
    horizonInput.value = optionData.defaults.horizon;
    lookbackVal.textContent = lookbackInput.value;
    horizonVal.textContent = horizonInput.value;

    const summary = await fetchJSON("/api/latest");
    renderSummary(summary);
    setStatus("최신 예측 로드 완료");
  } catch (err) {
    setStatus(`초기화 실패: ${err.message}`, false);
  }
}

predictBtn.addEventListener("click", async () => {
  try {
    setStatus("예측 계산 중...");
    const payload = {
      city: citySelect.value,
      lookback: Number(lookbackInput.value),
      horizon: Number(horizonInput.value),
    };
    const summary = await fetchJSON("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    renderSummary(summary);
    setStatus("예측 갱신 완료");
  } catch (err) {
    setStatus(`예측 실패: ${err.message}`, false);
  }
});

lookbackInput.addEventListener("input", () => {
  lookbackVal.textContent = lookbackInput.value;
});
horizonInput.addEventListener("input", () => {
  horizonVal.textContent = horizonInput.value;
});

init();
