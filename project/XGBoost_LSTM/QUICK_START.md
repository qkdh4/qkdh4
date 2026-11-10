# 시계열 머신러닝 프로젝트 - 빠른 시작 가이드

## 📋 프로젝트 개요

이 프로젝트는 **인도 도시의 대기질 데이터**를 활용한 시계열 머신러닝 연습 프로젝트입니다.

**3개의 주요 프로젝트로 구성:**
1. **다변량 시계열 예측** (LSTM, XGBoost)
2. **시계열 이상 징후 감지** (Autoencoder, Isolation Forest)
3. **시계열 결측치 보간** (KNN Imputer, Polynomial 등)

---

## 🚀 설치 및 실행

### 1️⃣ 의존성 설치
```bash
pip install -r requirements.txt
```

### 2️⃣ 테스트 (선택사항)
```bash
python test_setup.py
```

### 3️⃣ 메인 프로그램 실행
```bash
# 모든 프로젝트 실행
python main.py

# 또는 개별 프로젝트 실행
python project1_multivariate_forecasting.py
python project2_anomaly_detection.py
python project3_imputation.py
```

---

## 📁 파일 구조

```
project/
├── main.py                              # 메인 실행 파일
├── utils.py                             # 공용 유틸리티 함수
├── requirements.txt                     # 의존성 패키지
│
├── project1_multivariate_forecasting.py # 프로젝트 1: 시계열 예측
├── project2_anomaly_detection.py        # 프로젝트 2: 이상 징후 감지
├── project3_imputation.py               # 프로젝트 3: 결측치 보간
│
├── test_setup.py                        # 설정 테스트 스크립트
├── README.md                            # 자세한 가이드 (이 파일)
│
└── results/                             # 결과 그래프 저장 폴더
    ├── project1_predictions.png
    ├── project2_anomalies.png
    ├── project3_imputation.png
    └── project3_errors.png
```

---

## 🎯 프로젝트 상세 설명

### 📊 프로젝트 1: 다변량 시계열 예측

**목표**: 과거 7일의 미세먼지, 이산화질소 데이터로 다음날의 대기질 지수(AQI) 예측

**사용 기법**:
- **LSTM** (Long Short-Term Memory): 심화 시계열 모델
- **XGBoost**: 부스팅 기반 회귀 모델

**평가 지표**:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)

**출력**:
- 실제값 vs 예측값 비교 그래프 (2개 모델 나열)

---

### 🔍 프로젝트 2: 시계열 이상 징후 감지

**목표**: 일반적인 대기질 패턴과 다른 비정상 데이터 자동 탐지

**사용 기법**:
- **Autoencoder**: 신경망 기반 재구성 오차 이용
- **Isolation Forest**: 앙상블 기반 이상치 탐지

**출력**:
- 각 방법의 이상도 점수 그래프
- 실제값에 표시된 이상치 시각화
- 공통 이상치 (두 방법 모두 감지)
- 요약 통계

---

### 🔧 프로젝트 3: 시계열 결측치 보간

**목표**: 센서 미작동으로 인한 결측치를 자연스럽게 채워 넣기

**사용 기법**:
- Forward Fill / Backward Fill
- Linear / Polynomial / Spline 보간
- KNN Imputer (K-최근 이웃 기반)

**평가 지표**:
- MAE, RMSE (결측치가 있던 위치의 오차)

**출력**:
- 각 방법의 보간 결과 비교
- 방법별 오차 막대 그래프 (MAE, RMSE)

---

## 🔑 핵심 함수 (utils.py)

### 데이터 처리
```python
# 데이터 로드 (샘플 데이터 생성 또는 URL에서)
df = load_air_quality_data(url=None, city='Delhi')

# 결측치 처리 (선형 보간)
df_clean = handle_missing_values(df, method='linear')

# 시계열 윈도우 생성 (lookback=7일)
X, y = create_timeseries_windows(df_clean, lookback=7)

# 시간 기반 분할 (셔플 없음)
X_train, X_test, y_train, y_test = train_test_split_timeseries(X, y, test_size=0.2)

# 특성 정규화
X_train_norm, X_test_norm, scaler = normalize_data(X_train, X_test)
```

---

## 📈 데이터 정보

### 특징
- **기간**: 약 2.7년 (1000일)
- **피처**: PM2.5, PM10, NO2, CO, AQI
- **샘플링**: 일일(Daily)
- **크기**: 약 1000 레코드 × 5 컬럼

### 피처 설명
| 피처 | 설명 | 단위 |
|------|------|------|
| PM2.5 | 초미세먼지 (지름 2.5μm 이하) | μg/m³ |
| PM10 | 미세먼지 (지름 10μm 이하) | μg/m³ |
| NO2 | 이산화질소 | ppb |
| CO | 일산화탄소 | ppm |
| AQI | 대기질 지수 (종합 지표) | - |

---

## 🛠️ 기술 스택

| 카테고리 | 라이브러리 |
|----------|-----------|
| **데이터 처리** | pandas, numpy |
| **머신러닝** | scikit-learn, xgboost |
| **딥러닝** | tensorflow, keras |
| **시각화** | matplotlib, seaborn |

---

## 💡 학습 포인트

이 프로젝트를 통해 다음을 학습할 수 있습니다:

### 🔹 데이터 처리
- 실제 센서 데이터의 결측치 처리
- 이상치 감지 및 처리
- 특성 정규화

### 🔹 시계열 전문화 기법
- 윈도우 생성 (Sliding Window)
- 시간 기반 분할 (Temporal Split)
- 셔플 없는 분할의 중요성

### 🔹 머신러닝/딥러닝 모델
- LSTM 신경망 구현
- XGBoost 하이퍼파라미터 튜닝
- Autoencoder 구현
- Isolation Forest 적용

### 🔹 모델 평가
- MAE, RMSE 등 회귀 평가지표
- 이상치 탐지 평가
- 모델 비교

### 🔹 결과 시각화
- matplotlib/seaborn 활용
- 시계열 데이터 시각화
- 모델 비교 그래프

---

## 🔧 커스터마이징 팁

### 1️⃣ 다른 도시 데이터 사용
```python
df = load_air_quality_data(url=None, city='Mumbai')  # 도시명 변경
```

### 2️⃣ Lookback 윈도우 크기 변경
```python
X, y = create_timeseries_windows(df_clean, lookback=14)  # 14일로 변경
```

### 3️⃣ 테스트 비율 조정
```python
X_train, X_test, y_train, y_test = train_test_split_timeseries(X, y, test_size=0.3)  # 70:30으로 분할
```

### 4️⃣ 모델 하이퍼파라미터 튜닝
```python
# project1_multivariate_forecasting.py에서:
model = xgb.XGBRegressor(n_estimators=200, max_depth=8, learning_rate=0.05)
```

---

## ⚠️ 주의사항

1. **첫 실행 시** 모델 학습에 시간이 걸릴 수 있습니다 (특히 프로젝트 1, 2)
2. **GPU 미보유 시** CPU 계산으로 진행되므로 더 오래 걸립니다
3. **메모리 부족 시** batch_size를 줄이거나 데이터 크기를 감소시키세요
4. **Windows 콘솔에서** 한글 인코딩 문제가 있을 수 있으니 `utf-8` 사용 권장

---

## 📚 참고 자료

- **LSTM**: [Keras LSTM 공식 문서](https://keras.io/api/layers/recurrent_layers/lstm/)
- **XGBoost**: [XGBoost 튜토리얼](https://xgboost.readthedocs.io/)
- **Autoencoder**: [TensorFlow Autoencoder](https://www.tensorflow.org/tutorials/generative/autoencoder)
- **Isolation Forest**: [scikit-learn 공식 문서](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)

---

## 📞 문제 해결

### Q: "ModuleNotFoundError: No module named 'tensorflow'"
**A**: `pip install -r requirements.txt` 를 다시 실행하세요

### Q: "shape mismatch" 오류
**A**: 데이터가 비어 있을 가능성이 있습니다. URL 데이터 다운로드 실패 시 샘플 데이터가 자동 생성됩니다

### Q: 결과 그래프가 생성되지 않음
**A**: `results/` 폴더가 존재하는지 확인하세요. 자동 생성되어야 하지만, 수동으로 생성할 수도 있습니다

---

## 📝 라이선스

이 프로젝트는 교육 목적으로 작성되었습니다.

**작성**: AI Assistant (Copilot)  
**작성일**: 2024년 11월  
**Python 버전**: 3.8+

---

**행운을 빕니다! 즐거운 시계열 머신러닝 학습이 되세요! 🎓**
