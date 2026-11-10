# 분석기법별 데이터 활용 & 코드 의미 정리

## A. 공통 데이터 흐름

1. `prepare_dataset.py` 또는 `main.py` 실행  
2. `utils.build_processed_bundle()`에서 도시별 CSV 다운로드  
3. `utils.clean_air_quality_dataframe()`으로 컬럼 정리/형 변환  
4. `utils.preprocess_city_data()`에서 결측치 선형 보간 후 저장  
5. 분석 스크립트에서 `utils.load_prepared_city_data("Delhi")` 로드

---

## B. 어떤 데이터가 어디에 쓰이는가

### 1) 예측 (project1_multivariate_forecasting.py)
- 입력 데이터(X): 과거 7일의 `PM2.5, PM10, NO2, SO2, CO, O3, AQI`
- 타깃(y): 8일차 `AQI`
- 분할: 시간순 80%(학습), 20%(검증)
- 모델: LSTM, XGBoost
- 출력: `results/project1_predictions.png`

### 2) 이상치 탐지 (project2_anomaly_detection.py)
- 입력 데이터: 7일 윈도우 시계열(정규화)
- Autoencoder: 재구성오차(MSE)가 큰 구간을 이상치로 판정
- IsolationForest: 희소/고립 샘플을 이상치로 판정
- 출력: `results/project2_anomalies.png`

### 3) 결측치 보간 (project3_imputation.py)
- 기준 데이터: Delhi 정제 데이터
- 실험 데이터: 기준 데이터에 인위적으로 결측치(10%) 주입
- 기법: Forward Fill, Linear, Polynomial, KNN, Spline
- 평가: 결측치가 주입된 위치에서 MAE/RMSE 계산
- 출력: `results/project3_imputation.png`, `results/project3_errors.png`

---

## C. 핵심 코드 함수 의미

## `utils.py`
- `download_city_datasets(...)`  
  도시별 원본 CSV를 `data/raw/`에 저장.

- `clean_air_quality_dataframe(df, city)`  
  BOM/불필요 컬럼 제거, 날짜 파싱, 숫자 컬럼 변환, 날짜 중복 제거.

- `preprocess_city_data(city)`  
  선형보간으로 결측치 처리 후 `data/processed/{city}_clean.csv` 저장.

- `build_processed_bundle(...)`  
  여러 도시를 한 번에 다운로드/정제하고 메타데이터 JSON 생성.

- `load_prepared_city_data(city)`  
  정제된 CSV를 읽어 Date 인덱스 + 모델 피처 순서로 반환.

- `create_timeseries_windows(data, lookback=7)`  
  슬라이딩 윈도우로 `X(과거 7일)`와 `y(다음날 AQI)` 생성.

- `train_test_split_timeseries(...)`  
  셔플 없이 시간순 분할.

- `normalize_data(...)`  
  학습 데이터 기준 표준화 후 학습/검증 데이터 모두 변환.

## `main.py`
- 전체 실행 오케스트레이터.
- 데이터 준비 후 3개 프로젝트를 순차 실행.

## `project1_multivariate_forecasting.py`
- `build_lstm_model(...)`: LSTM 회귀 모델 구조 정의
- `train_lstm_model(...)`: LSTM 학습/예측
- `train_xgboost_model(...)`: XGBoost 학습/예측
- `evaluate_model(...)`: MAE/RMSE 계산

## `project2_anomaly_detection.py`
- `build_autoencoder(...)`: 입력 재구성 네트워크
- `detect_anomalies_autoencoder(...)`: 재구성오차 percentile 기준 이상치 탐지
- `detect_anomalies_isolation_forest(...)`: IF 기반 이상치 탐지

## `project3_imputation.py`
- `create_synthetic_missing_values(...)`: 결측치 주입
- `impute_*`: 각 보간기법 실행
- `calculate_imputation_error(...)`: 주입된 위치 기준 MAE/RMSE 계산

---

## D. 실행 순서 추천

1. `python test_setup.py` (환경/데이터 파이프라인 확인)  
2. `python prepare_dataset.py` (데이터만 먼저 준비)  
3. `python main.py` (전체 분석 실행)

