"""설정 - 코스피200(KODEX200) + 코스피 시총 상위 200 (총 201종목)"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

BENCHMARK_CODE = "069500"          # KODEX 200 ETF (코스피200 추종)
BENCHMARK_NAME = "KODEX 200 (코스피200)"
TOP_N = 200                        # 코스피 시총 상위 N
LOOKBACK_DAYS = int(os.getenv("LOOKBACK_DAYS", "180"))  # 분석 기간(달력일 여유 포함)

# 그룹화: 정규화 초과수익률(norm_score) 기준
UP_THRESHOLD = 0.5
DOWN_THRESHOLD = -0.5
SMOOTH_WINDOW = 5                  # 5일 평균으로 단기 노이즈 완화
VOL_WINDOW = 20                    # 정규화용 변동성 윈도우

# 영향력: 시총 가중 70% + 거래대금 가중 30%
MCAP_WEIGHT = 0.7
VOLUME_WEIGHT = 0.3

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
