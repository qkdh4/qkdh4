"""GitHub Pages용 단일 HTML(docs/index.html) 생성 - 데이터(JSON)를 파일에 내장하므로
GitHub에 push 후 Settings>Pages에서 /docs 배포하면 https://<user>.github.io/<repo>/ 로 접속 가능"""
import json, config, analysis

if __name__=="__main__":
    if not (config.DATA_DIR/"ohlcv.csv").exists():
        import data_collector; data_collector.collect()
    r=analysis.run_from_files()
    g=r["group_ts"].copy(); g["Date"]=g["Date"].astype(str)
    payload={"summary":{**r["summary"]},"stocks":r["latest"].fillna(0).to_dict("records"),
             "group_ts":g.to_dict("records")}
    try: payload["summary"]["meta"]=json.loads((config.DATA_DIR/"meta.json").read_text(encoding="utf-8"))
    except Exception: payload["summary"]["meta"]={}
    html=(config.BASE_DIR/"templates"/"index.html").read_text(encoding="utf-8")
    html=html.replace("/*__STATIC_DATA__*/", "window.STATIC_DATA="+json.dumps(payload,ensure_ascii=False)+";")
    out=config.BASE_DIR/"docs"/"index.html"; out.parent.mkdir(exist_ok=True)
    out.write_text(html,encoding="utf-8"); print("생성:",out)
