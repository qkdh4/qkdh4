"""
시계열 분석
1) 당일 등락률: ret = Close/전일Close - 1
2) 정규화: 초과수익률 excess = 종목ret - 벤치마크(KODEX200)ret
           norm = excess 의 20일 롤링 z-score 성격 지표 = smooth(5일평균 excess) / (20일 std of excess)
3) 그룹화: norm >= 0.5 상향(UP), <= -0.5 하향(DOWN), 그 외 횡보(SIDE)
4) 영향력: 시총비중 w_m, 거래대금비중 w_v
           contribution(지수기여도, bp) = w_m * 종목수익률 * 10000
           influence_score = (0.7*w_m + 0.3*w_v) * |excess| 를 0~100 정규화
5) 그룹 전이: 5거래일 전 그룹 -> 현재 그룹 (예: 상향->하향) 변화 종목 추적
"""
from __future__ import annotations
import numpy as np, pandas as pd
import config

GROUPS={"UP":"상향","SIDE":"횡보","DOWN":"하향"}

def _group(x):
    return "UP" if x>=config.UP_THRESHOLD else ("DOWN" if x<=config.DOWN_THRESHOLD else "SIDE")

def analyze(ohlcv: pd.DataFrame, universe: pd.DataFrame) -> dict:
    df=ohlcv.copy(); df["Date"]=pd.to_datetime(df["Date"])
    df["Code"]=df["Code"].astype(str).str.zfill(6)
    df=df.sort_values(["Code","Date"])
    df["ret"]=df.groupby("Code")["Close"].pct_change()
    df["amount"]=df["Close"]*df["Volume"]
    bench=df[df["Code"]==config.BENCHMARK_CODE][["Date","ret"]].rename(columns={"ret":"bench_ret"})
    df=df.merge(bench,on="Date",how="left")
    df["excess"]=df["ret"]-df["bench_ret"]
    # 종목별 롤링 정규화
    def _norm(g):
        e=g["excess"]
        smooth=e.rolling(config.SMOOTH_WINDOW).mean()
        vol=e.rolling(config.VOL_WINDOW).std()
        vol=vol.where(vol>1e-12)
        g["norm_score"]=smooth/vol
        g["cum_excess"]=(1+e.fillna(0)).cumprod()-1
        return g
    df=df.groupby("Code",group_keys=False).apply(_norm)
    stocks=df[df["Code"]!=config.BENCHMARK_CODE].copy()
    latest_date=stocks["Date"].max()
    latest=stocks[stocks["Date"]==latest_date].copy()
    # 유니버스 결합 (시총)
    uni=universe.copy(); uni["Code"]=uni["Code"].astype(str)
    latest["Code"]=latest["Code"].astype(str)
    latest=latest.merge(uni[["Code","Name","Marcap"]+(["Sector"] if "Sector" in uni else [])],
                        on="Code",how="left",suffixes=("","_u"))
    if "Name" not in latest or latest["Name"].isna().all():
        latest["Name"]=latest["Code"]
    total_mcap=latest["Marcap"].sum(); total_amt=latest["amount"].sum()
    latest["w_mcap"]=latest["Marcap"]/total_mcap
    latest["w_volume"]=latest["amount"]/total_amt
    latest["contribution_bp"]=latest["w_mcap"]*latest["ret"]*10000
    raw=(config.MCAP_WEIGHT*latest["w_mcap"]+config.VOLUME_WEIGHT*latest["w_volume"])*latest["excess"].abs()
    latest["influence_score"]=(raw/raw.max()*100 if raw.max() else raw)
    latest["group"]=latest["norm_score"].fillna(0).map(_group)
    latest["group_kr"]=latest["group"].map(GROUPS)

    # 전이: 5거래일 전 그룹과 비교
    dates=sorted(stocks["Date"].dropna().unique())
    prev_date=dates[-6] if len(dates)>=6 else dates[0]
    prev=stocks[stocks["Date"]==prev_date][["Code","norm_score"]].copy()
    prev["prev_group"]=prev["norm_score"].fillna(0).map(_group)
    latest=latest.merge(prev[["Code","prev_group"]],on="Code",how="left")
    latest["transition"]=latest["prev_group"].fillna(latest["group"])+"->"+latest["group"]
    latest["changed"]=latest["prev_group"]!=latest["group"]
    matrix=(latest.groupby(["prev_group","group"]).size().unstack(fill_value=0)
            .reindex(index=["UP","SIDE","DOWN"],columns=["UP","SIDE","DOWN"],fill_value=0))

    summary={
        "latest_date":str(latest_date.date()), "prev_date":str(pd.Timestamp(prev_date).date()),
        "benchmark":config.BENCHMARK_NAME,
        "group_counts":{GROUPS[k]:int(v) for k,v in latest["group"].value_counts().items()},
        "avg_norm":float(latest["norm_score"].mean()),
        "total_contribution_bp":float(latest["contribution_bp"].sum()),
        "changed_count":int(latest["changed"].sum()),
        "transition_matrix":{r:{c:int(matrix.loc[r,c]) for c in matrix.columns} for r in matrix.index},
    }
    cols=["Code","Name","Close","ret","bench_ret","excess","norm_score","cum_excess","group","group_kr",
          "prev_group","transition","changed","Marcap","w_mcap","w_volume","amount","contribution_bp","influence_score"]
    latest_out=latest[cols].sort_values("influence_score",ascending=False)
    # 시계열 (차트용)
    stocks["group_ts"]=stocks["norm_score"].fillna(0).map(_group)
    gts=stocks.groupby(["Date","group_ts"]).size().unstack(fill_value=0)
    for c in ["UP","SIDE","DOWN"]:
        if c not in gts: gts[c]=0
    return {"summary":summary,"latest":latest_out,"ohlcv":df,
            "group_ts":gts.reset_index(),"prev_date":prev_date,"latest_date":latest_date}

def run_from_files() -> dict:
    ohlcv=pd.read_csv(config.DATA_DIR/"ohlcv.csv")
    universe=pd.read_csv(config.DATA_DIR/"universe.csv", dtype={"Code":str})
    universe["Code"]=universe["Code"].str.zfill(6)
    result=analyze(ohlcv, universe)
    result["latest"].to_csv(config.DATA_DIR/"latest_analysis.csv",index=False,encoding="utf-8-sig")
    return result

if __name__=="__main__":
    r=run_from_files(); print(r["summary"])
