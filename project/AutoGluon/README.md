# AutoGluon TimeSeries AQI Forecast

`project/AutoGluon` 폴더에서 대기질(AQI) 데이터를 사용해 AutoGluon(TimeSeries) 기반 예측/자동 앙상블을 수행합니다.

## 특징

- 기존 `project/XGBoost_LSTM/data` 데이터를 우선 재사용
- 없으면 원본 공개 데이터셋을 자동 다운로드 후 정제
- `presets="best_quality"` + HPO 기반으로 많은 시계열 조합 탐색
- `ray` 기반 HPO 스케줄링 지원(가능한 환경에서 더 안정적 튜닝)
- 성능 상위 모델 자동 앙상블
- 웹앱에서 실행 과정 로그 + 리더보드 + 예측 결과 확인
- `python main.py` 한 번으로 웹앱 실행 및 전체 분석 자동 시작
- 모델 폴더 자동 정리(도시별 최근 5개 실행만 유지)

## 설치

AutoGluon TimeSeries는 Python 3.11 환경에서 실행하세요.

```bash
pip install -r requirements.txt
```

현재 Python이 3.12+라면(예: 3.14), 아래처럼 3.11 환경을 먼저 준비하세요.

```bash
C:\Users\504\miniconda3\Scripts\conda.exe create -y -n autogluon-ts311 python=3.11
C:\Users\504\miniconda3\Scripts\conda.exe run -n autogluon-ts311 python -m pip install -r requirements.txt
```

## 실행

```bash
python main.py
```

실행하면 Streamlit 웹앱이 열리고 전체 분석이 자동 시작됩니다.

3.12+ Python에서 실행 중이라면 `main.py`가 자동으로 `autogluon-ts311`(존재 시) Python을 사용해 웹앱을 실행합니다.

## 결과물

- `results/next_aqi_forecast.csv`
- `results/next_aqi_forecast.png`
- `results/model_leaderboard.csv`
- `results/prediction_summary.json`
- `results/training_run.log`
- `models/autogluon_timeseries_<city>_<YYYYMMDD_HHMMSS>/`

## 고강도 탐색 설정

웹앱 좌측 사이드바에서 탐색 강도를 조절할 수 있습니다.

- `최대 학습 시간(시간)`: 전체 학습 시간
- `HPO 시도 횟수`: 하이퍼파라미터 탐색 횟수
- `검증 윈도우 수`: 백테스트 윈도우 수

값이 클수록 더 많은 조합을 검사하지만 실행 시간도 크게 증가합니다.

참고: 시간 제한이 매우 짧은 실행(15분 미만)에서는 다운로드/초기화 비용이 큰 모델(예: 대형 사전학습 모델)을 자동 제외하고 경량 모델셋으로 실행합니다.
