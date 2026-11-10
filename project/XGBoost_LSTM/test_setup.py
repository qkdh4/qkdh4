"""
환경/데이터/핵심 파이프라인 스모크 테스트
"""

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("Time Series ML Project - Setup Test")
print("=" * 70)

try:
    from utils import (
        MODEL_FEATURES,
        build_processed_bundle,
        create_timeseries_windows,
        load_prepared_city_data,
        normalize_data,
        train_test_split_timeseries,
    )
except Exception as exc:
    print(f"[ERROR] utils import failed: {exc}")
    sys.exit(1)

print("\n[1] 데이터 다운로드/정제 테스트")
metadata = build_processed_bundle(cities=["Delhi", "Mumbai"], force_download=False)
print(f"  [OK] cities: {', '.join(metadata['cities'].keys())}")

print("\n[2] 정제 데이터 로드 테스트")
df = load_prepared_city_data("Delhi")
print(f"  [OK] Delhi shape: {df.shape}")
print(f"  [OK] columns: {', '.join(df.columns.tolist())}")

print("\n[3] 시계열 윈도우 생성 테스트")
X, y = create_timeseries_windows(df, lookback=7)
print(f"  [OK] X shape={X.shape}, y shape={y.shape}")

print("\n[4] 시간 분할 + 정규화 테스트")
X_train, X_test, y_train, y_test = train_test_split_timeseries(X, y, test_size=0.2)
X_train_norm, X_test_norm, _ = normalize_data(X_train, X_test)
print(f"  [OK] train={X_train_norm.shape}, test={X_test_norm.shape}")

if list(df.columns) != MODEL_FEATURES:
    print("[ERROR] feature order mismatch")
    sys.exit(1)

print("\n[SUCCESS] All checks passed.")
