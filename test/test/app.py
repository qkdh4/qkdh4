"""웹앱 서버 (Flask) - VSCode에서 실행: python app.py -> http://localhost:8000
GitHub Pages용 정적본: python export_static.py 로 docs/index.html 생성 후 Pages 배포"""
import json
from pathlib import Path
import pandas as pd
from flask import Flask, jsonify, render_template, request
import config

app = Flask(__name__)
_cache = {}

def load():
    if "r" not in _cache:
        if not (config.DATA_DIR/"ohlcv.csv").exists():
            import data_collector; data_collector.collect()
        import analysis; _cache["r"]=analysis.run_from_files()
        try: _cache["meta"]=json.loads((config.DATA_DIR/"meta.json").read_text(encoding="utf-8"))
        except Exception: _cache["meta"]={}
    return _cache["r"], _cache["meta"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/summary")
def api_summary():
    r,meta=load(); return jsonify({**r["summary"],"meta":meta})

@app.route("/api/stocks")
def api_stocks():
    r,_=load(); q=request.args.get("group",""); s=request.args.get("q","")
    df=r["latest"]
    if q in ("UP","SIDE","DOWN"): df=df[df["group"]==q]
    if s: df=df[df["Name"].astype(str).str.contains(s,na=False)|df["Code"].astype(str).str.contains(s)]
    return jsonify(df.fillna(0).to_dict("records"))

@app.route("/api/influence")
def api_influence():
    r,_=load()
    return jsonify(r["latest"].nlargest(15,"influence_score").fillna(0).to_dict("records"))

@app.route("/api/transitions")
def api_transitions():
    r,_=load()
    changed=r["latest"][r["latest"]["changed"]].sort_values("influence_score",ascending=False)
    return jsonify({"matrix":r["summary"]["transition_matrix"],"changed":changed.fillna(0).to_dict("records")})

@app.route("/api/group_timeseries")
def api_gts():
    r,_=load(); g=r["group_ts"].copy(); g["Date"]=g["Date"].astype(str)
    return jsonify(g.to_dict("records"))

@app.route("/api/stock/<code>")
def api_stock(code):
    r,_=load(); d=r["ohlcv"][r["ohlcv"]["Code"].astype(str)==code.zfill(6)].copy()
    d["Date"]=d["Date"].astype(str)
    return jsonify(d[["Date","Open","High","Low","Close","Volume","ret","excess","norm_score","cum_excess"]].fillna(0).to_dict("records"))

@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    import data_collector, analysis
    meta=data_collector.collect(); _cache.clear(); _cache["r"]=analysis.run_from_files(); _cache["meta"]=meta
    return jsonify({"ok":True,"meta":meta})

if __name__=="__main__":
    print(f"서버 시작: http://localhost:{config.PORT}  (종료: Ctrl+C)")
    app.run(host=config.HOST, port=config.PORT, debug=False)
