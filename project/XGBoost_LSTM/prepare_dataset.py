"""
데이터 다운로드 및 정제 전용 스크립트
"""

from utils import build_processed_bundle


def main():
    print("[데이터셋 준비 시작]")
    metadata = build_processed_bundle()
    print("\n[완료] 처리 요약")
    for city, info in metadata["cities"].items():
        print(
            f"- {city}: {info['rows']} rows "
            f"({info['start_date']} ~ {info['end_date']})"
        )
    print("\n저장 위치")
    print("- data/raw/*.csv")
    print("- data/processed/*_clean.csv")
    print("- data/processed/all_cities_clean.csv")
    print("- data/processed/dataset_metadata.json")


if __name__ == "__main__":
    main()
