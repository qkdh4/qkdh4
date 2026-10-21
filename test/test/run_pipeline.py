"""수집 -> 분석 -> 결과 CSV/JSON 저장 (한 번에 실행)"""
import data_collector, analysis, json, config
if __name__=="__main__":
    meta=data_collector.collect()
    r=analysis.run_from_files()
    (config.DATA_DIR/"summary.json").write_text(json.dumps({**r["summary"],"meta":meta},ensure_ascii=False,indent=2),encoding="utf-8")
    print("요약:", r["summary"])
    print("저장:", config.DATA_DIR/"latest_analysis.csv")
