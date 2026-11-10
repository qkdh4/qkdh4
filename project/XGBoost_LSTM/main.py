"""
메인 실행 파일: AQI 다음값 예측 프로그램
"""

import os
from prediction_program import run_prediction
from utils import build_processed_bundle, ensure_directories

def main():
    ensure_directories()
    print("\n" + "="*70)
    print(" AQI 예측 프로그램")
    print("="*70 + "\n")

    print(">>> 데이터 다운로드 및 정제 중...\n")
    metadata = build_processed_bundle()
    print(f"  처리된 도시: {', '.join(metadata['cities'].keys())}")
    print("  저장 위치: data/raw, data/processed\n")

    print(">>> AQI 다음값 예측 실행 중...\n")
    summary = run_prediction(city="Delhi", lookback=14, horizon=7)

    print("\n" + "="*70)
    print("예측 실행 완료!")
    print("="*70)
    print(f"\n도시: {summary['city']}")
    print(f"검증 MAE: {summary['validation_metrics']['MAE']:.4f}")
    print(f"검증 RMSE: {summary['validation_metrics']['RMSE']:.4f}")
    print("\n다음 7일 AQI 예측")
    for row in summary["next_predictions"]:
        print(f"  - {row['date']}: {row['predicted_aqi']:.2f}")
    print("\n[생성된 파일]")
    print("  - results/next_aqi_forecast.png")
    print("  - results/next_aqi_forecast.csv")
    print("  - results/prediction_summary.json")

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
