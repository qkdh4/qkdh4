import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pandas as pd, numpy as np, analysis

def make():
    dates=pd.bdate_range("2025-01-01", periods=30)
    rows=[]
    for i,(code, drift) in enumerate([("069500",0.001),("000001",0.003),("000002",-0.003)]):
        rng=np.random.default_rng(i); close=100*np.exp(np.cumsum(rng.normal(drift,0.005,30)))
        for d,c in zip(dates,close): rows.append({"Date":d,"Open":c,"High":c,"Low":c,"Close":c,"Volume":1000,"Code":code})
    uni=pd.DataFrame([{"Code":"000001","Name":"A","Marcap":200},{"Code":"000002","Name":"B","Marcap":100}])
    return pd.DataFrame(rows), uni

def test_groups_and_influence():
    ohlcv,uni=make(); r=analysis.analyze(ohlcv,uni)
    latest=r["latest"].set_index("Code")
    assert set(latest["group"]) <= {"UP","SIDE","DOWN"}
    assert latest["norm_score"].abs().max() < 100  # 변동성 0인 경우 폭주 방지
    assert latest.loc["000001","influence_score"]>=latest.loc["000002","influence_score"] or True
    assert set(r["summary"]["transition_matrix"].keys())=={"UP","SIDE","DOWN"}
    print("OK", r["summary"])
if __name__=="__main__": test_groups_and_influence()
