# 시계열 머신러닝 실습 프로젝트 (test 폴더)

이 폴더는 **실제 데이터 다운로드 → 정제 → 다음 AQI 예측**을 수행하는 프로그램과,
학습용 분석 설명 웹앱을 함께 제공합니다.

## 1) 폴더 구조

```text
test/
├─ main.py
├─ prediction_program.py
├─ prediction_webapp.py
├─ learning_webapp.py
├─ prepare_dataset.py
├─ utils.py
├─ project1_multivariate_forecasting.py
├─ project2_anomaly_detection.py
├─ project3_imputation.py
├─ test_setup.py
├─ data/
│  ├─ raw/
│  └─ processed/
└─ results/
```

## 2) 데이터셋 다운로드/정제

```bash
python prepare_dataset.py
```

실행 후 생성:
- `data/raw/*_raw.csv`: 원본 다운로드 파일
- `data/processed/*_clean.csv`: 도시별 정제 완료 데이터
- `data/processed/all_cities_clean.csv`: 도시 통합 데이터
- `data/processed/dataset_metadata.json`: 데이터 설명/통계

## 3) 예측 프로그램 실행

```bash
python main.py
```

`main.py`는 다음 순서로 실행됩니다.
1. 데이터 다운로드 및 정제
2. Delhi AQI 예측 모델 학습
3. 다음 7일 AQI 예측 결과 저장

생성 결과:
- `results/next_aqi_forecast.png`
- `results/next_aqi_forecast.csv`
- `results/prediction_summary.json`

## 4) 개별 실행

```bash
python prediction_program.py
python project1_multivariate_forecasting.py
python project2_anomaly_detection.py
python project3_imputation.py
```

> `project1~3`는 학습용 분석 스크립트이며, 예측 프로그램 본체는 `prediction_program.py`입니다.

## 5) 코드 이해 가이드

분석기법별로 어떤 데이터를 어떻게 쓰는지, 함수별 의미를 문서로 정리했습니다.

- `ANALYSIS_GUIDE.md` 확인

## 6) 웹앱

```bash
pip install -r requirements.txt
python web_server.py
```

### 웹앱 구성 (HTML/CSS/JavaScript + Flask API)
- 메인 예측 대시보드: `http://127.0.0.1:8600/`
- 학습 설명 페이지: `http://127.0.0.1:8600/learning`

### 메인 예측 대시보드
- 도시/입력 윈도우/예측 기간 설정 후 예측 실행
- KPI 카드(내일 AQI/등급/RMSE/최고 위험), 예측 카드, 인터랙티브 트렌드 차트 제공
- AQI 등급/건강 권고/CSV 다운로드 제공

### 학습 설명 페이지
- 예측/이상치탐지/결측치보간의 상세 설명 학습
- 각 분석 결과 이미지와 해석 확인
