from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from prediction_program import run_prediction
from utils import CITY_DATASET_URLS, RESULTS_DIR, ensure_directories


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
SUMMARY_PATH = RESULTS_DIR / "prediction_summary.json"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="/static")


def _load_summary() -> dict | None:
    if not SUMMARY_PATH.exists():
        return None
    return json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.get("/api/options")
def options():
    return jsonify(
        {
            "cities": list(CITY_DATASET_URLS.keys()),
            "defaults": {"city": "Delhi", "lookback": 21, "horizon": 7},
        }
    )


@app.get("/api/latest")
def latest():
    summary = _load_summary()
    if summary is None:
        summary = run_prediction(city="Delhi", lookback=21, horizon=7)
    return jsonify(summary)


@app.post("/api/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    city = payload.get("city", "Delhi")
    lookback = int(payload.get("lookback", 21))
    horizon = int(payload.get("horizon", 7))

    if city not in CITY_DATASET_URLS:
        return jsonify({"error": f"지원하지 않는 도시: {city}"}), 400
    if not (7 <= lookback <= 45):
        return jsonify({"error": "lookback은 7~45 사이여야 합니다."}), 400
    if not (1 <= horizon <= 14):
        return jsonify({"error": "horizon은 1~14 사이여야 합니다."}), 400

    summary = run_prediction(city=city, lookback=lookback, horizon=horizon)
    return jsonify(summary)


@app.get("/")
def index():
    return send_from_directory(str(FRONTEND_DIR), "index.html")


@app.get("/learning")
def learning():
    return send_from_directory(str(FRONTEND_DIR), "learning.html")


@app.get("/results/<path:filename>")
def results_file(filename: str):
    return send_from_directory(str(RESULTS_DIR), filename)


@app.get("/<path:path>")
def assets(path: str):
    return send_from_directory(str(FRONTEND_DIR), path)


if __name__ == "__main__":
    ensure_directories()
    app.run(host="127.0.0.1", port=8600, debug=False)
