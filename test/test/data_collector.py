"""
데이터 수집 (FinanceDataReader)
- 벤치마크: KODEX 200 (069500)
- 코스피 시가총액 상위 200: fdr.StockListing('KRX') -> Market=KOSPI, Marcap 내림차순
- 각 종목 일봉 OHLCV
fdr/네트워크가 없는 환경(VSCode 최초 실행 전 등)에서는 결정적(deterministic) 샘플 데이터로
대체하여 웹앱이 바로 동작하게 한다. 실제 환경에서는 자동으로 실데이터를 사용한다.
"""
from __future__ import annotations
import hashlib, datetime as dt
import numpy as np, pandas as pd
import config

def _seed(code: str) -> int:
    return int(hashlib.md5(code.encode()).hexdigest()[:8], 16)

def sample_universe(n: int = 200) -> pd.DataFrame:
    """실제 종목명을 흉내낸 샘플 유니버스 (폴백 전용, 실종목 아님을 meta에 명시)"""
    sectors = ["반도체","자동차","금융","바이오","인터넷","화학","철강","유통","통신","에너지"]
    rows=[]
    for i in range(n):
        code=f"{56000+i*137:06d}"
        rng=np.random.default_rng(_seed(code))
        rows.append({"Code":code,"Name":f"샘플종목{i+1:03d}","Market":"KOSPI",
                     "Sector":sectors[i%len(sectors)],"Marcap":float((n-i)*rng.uniform(0.7,1.3)*1e11)})
    return pd.DataFrame(rows).sort_values("Marcap",ascending=False).reset_index(drop=True)

def get_universe() -> tuple[pd.DataFrame, str]:
    try:
        import FinanceDataReader as fdr
        listing = fdr.StockListing("KRX")
        kospi = listing[listing["Market"]=="KOSPI"].copy()
        kospi["Marcap"] = pd.to_numeric(kospi["Marcap"], errors="coerce")
        top = kospi.sort_values("Marcap",ascending=False).head(config.TOP_N)
        cols=[c for c in ["Code","Name","Market","Marcap"] if c in top.columns]
        return top[cols].reset_index(drop=True), "FinanceDataReader(KRX)"
    except Exception as e:
        print(f"[collector] 실 유니버스 실패({e}) -> 샘플 유니버스 사용")
        return sample_universe(config.TOP_N), "SAMPLE(폴백)"

def _sample_ohlcv(code: str, days: int) -> pd.DataFrame:
    rng=np.random.default_rng(_seed(code))
    dates=pd.bdate_range(end=dt.date.today(), periods=days)
    drift=rng.uniform(-0.0005,0.0012); vol=rng.uniform(0.008,0.028)
    ret=rng.normal(drift, vol, days)
    close=10000*np.exp(np.cumsum(ret)); open_=close*(1+rng.normal(0,0.004,days))
    high=np.maximum(open_,close)*(1+np.abs(rng.normal(0,0.006,days)))
    low=np.minimum(open_,close)*(1-np.abs(rng.normal(0,0.006,days)))
    volm=rng.lognormal(12,0.5,days).astype(int)
    return pd.DataFrame({"Date":dates,"Open":open_,"High":high,"Low":low,"Close":close,"Volume":volm})

def fetch_ohlcv(code: str, start: str, end: str, source_hint: str) -> pd.DataFrame:
    if "SAMPLE" not in source_hint:
        try:
            import FinanceDataReader as fdr
            df=fdr.DataReader(code, start, end)
            if df is not None and len(df):
                df=df.reset_index().rename(columns={"index":"Date"})
                return df[["Date","Open","High","Low","Close","Volume"]]
        except Exception as e:
            print(f"[collector] {code} 실데이터 실패({e}) -> 샘플")
    days=max(30, (pd.Timestamp(end)-pd.Timestamp(start)).days)
    return _sample_ohlcv(code, min(days,260))

def collect() -> dict:
    end=dt.date.today(); start=end-dt.timedelta(days=config.LOOKBACK_DAYS+120)
    universe, src = get_universe()
    frames={}
    bench=fetch_ohlcv(config.BENCHMARK_CODE, str(start), str(end), src)
    frames[config.BENCHMARK_CODE]=bench
    for _,r in universe.iterrows():
        frames[str(r["Code"])]=fetch_ohlcv(str(r["Code"]), str(start), str(end), src)
    universe.to_csv(config.DATA_DIR/"universe.csv", index=False, encoding="utf-8-sig")
    long=[]
    for code,df in frames.items():
        d=df.copy(); d["Code"]=code; long.append(d)
    ohlcv=pd.concat(long, ignore_index=True)
    ohlcv.to_csv(config.DATA_DIR/"ohlcv.csv", index=False, encoding="utf-8-sig")
    meta={"source":src,"benchmark":config.BENCHMARK_CODE,"collected_at":str(dt.datetime.now()),
          "n_stocks":len(universe),"is_sample":"SAMPLE" in src}
    pd.Series(meta).to_json(config.DATA_DIR/"meta.json", force_ascii=False, indent=2)
    print(f"[collector] 완료: {meta}")
    return meta

if __name__=="__main__":
    collect()
