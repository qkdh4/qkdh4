# AutoGluon(TimeSeries) 활용 모델 전체 정리 (최신 결과)

## 1. 기준 파일

- [prediction_summary.json](./results/prediction_summary.json)
- [model_leaderboard.csv](./results/model_leaderboard.csv)

## 2. 최신 실행 설정 요약

- presets: **best_quality**
- hyperparameters: **uniform_model_budget**
- time_limit_seconds: **1800**
- num_val_windows: **5**
- num_hpo_trials: **0**
- uniform_model_budget: **True**
- uniform_family_count: **10**
- uniform_variants_per_family: **3**

## 3. 전체 규모

- 전체 학습 모델 수: **31개**
- 베스트 모델: **RecursiveTabularU03**
- 앙상블 모델: **WeightedEnsemble**
- 실제 학습된 모델 계열 수(앙상블 제외): **10개**

## 4. 모델 계열별 요약

| 모델 계열 | 모델 수 | 최고 score_test | 최고 score_val | 평균 fit_time_marginal(초) |
|---|---:|---:|---:|---:|
| RecursiveTabular | 3 | -89.994605 | -85.168893 | 3.53 |
| NPTS | 3 | -98.111860 | -128.462279 | 0.53 |
| DirectTabular | 3 | -99.213514 | -79.743251 | 3.20 |
| DeepAR | 3 | -130.802738 | -72.147861 | 121.17 |
| DynamicOptimizedTheta | 3 | -135.052695 | -70.122884 | 3.62 |
| Theta | 3 | -135.074997 | -70.130969 | 1.93 |
| TemporalFusionTransformer | 3 | -136.275255 | -47.258673 | 235.33 |
| AutoETS | 3 | -137.292565 | -70.568691 | 3.84 |
| ETS | 3 | -137.292565 | -70.568691 | 5.67 |
| SeasonalNaive | 3 | -159.371534 | -107.567571 | 4.15 |
| WeightedEnsemble | 1 | -128.131856 | -46.563322 | 5.91 |

## 5. 최신 실행에서 학습된 전체 모델 목록

| # | 모델명 | 계열 | score_test | score_val | fit_time_marginal(초) | fit_order |
|---:|---|---|---:|---:|---:|---:|
| 1 | SeasonalNaiveU01 | SeasonalNaive | -159.371534 | -107.567571 | 9.96 | 1 |
| 2 | SeasonalNaiveU02 | SeasonalNaive | -159.371534 | -107.567571 | 2.39 | 2 |
| 3 | SeasonalNaiveU03 | SeasonalNaive | -159.371534 | -107.567571 | 0.10 | 3 |
| 4 | RecursiveTabularU01 | RecursiveTabular | -89.994605 | -85.168893 | 3.56 | 4 |
| 5 | RecursiveTabularU02 | RecursiveTabular | -89.994605 | -85.168893 | 3.45 | 5 |
| 6 | RecursiveTabularU03 | RecursiveTabular | -89.994605 | -85.168893 | 3.57 | 6 |
| 7 | DirectTabularU01 | DirectTabular | -99.213514 | -79.743251 | 3.18 | 7 |
| 8 | DirectTabularU02 | DirectTabular | -99.213514 | -79.743251 | 3.19 | 8 |
| 9 | DirectTabularU03 | DirectTabular | -99.213514 | -79.743251 | 3.22 | 9 |
| 10 | ETSU01 | ETS | -137.292565 | -70.568691 | 8.17 | 10 |
| 11 | ETSU02 | ETS | -137.292565 | -70.568691 | 4.98 | 11 |
| 12 | ETSU03 | ETS | -137.292565 | -70.568691 | 3.87 | 12 |
| 13 | NPTSU01 | NPTS | -98.111860 | -128.462279 | 0.56 | 13 |
| 14 | NPTSU02 | NPTS | -98.111860 | -128.462279 | 0.51 | 14 |
| 15 | NPTSU03 | NPTS | -98.111860 | -128.462279 | 0.53 | 15 |
| 16 | DynamicOptimizedThetaU01 | DynamicOptimizedTheta | -135.052695 | -70.122884 | 3.61 | 16 |
| 17 | DynamicOptimizedThetaU02 | DynamicOptimizedTheta | -135.052695 | -70.122884 | 3.66 | 17 |
| 18 | DynamicOptimizedThetaU03 | DynamicOptimizedTheta | -135.052695 | -70.122884 | 3.60 | 18 |
| 19 | ThetaU01 | Theta | -135.074997 | -70.130969 | 1.93 | 19 |
| 20 | ThetaU02 | Theta | -135.074997 | -70.130969 | 1.93 | 20 |
| 21 | ThetaU03 | Theta | -135.074997 | -70.130969 | 1.94 | 21 |
| 22 | AutoETSU01 | AutoETS | -137.292565 | -70.568691 | 3.83 | 22 |
| 23 | AutoETSU02 | AutoETS | -137.292565 | -70.568691 | 3.85 | 23 |
| 24 | AutoETSU03 | AutoETS | -137.292565 | -70.568691 | 3.84 | 24 |
| 25 | TemporalFusionTransformerU01 | TemporalFusionTransformer | -164.573981 | -53.759909 | 234.07 | 25 |
| 26 | TemporalFusionTransformerU02 | TemporalFusionTransformer | -136.275255 | -47.258673 | 235.08 | 26 |
| 27 | TemporalFusionTransformerU03 | TemporalFusionTransformer | -145.713355 | -51.039796 | 236.84 | 27 |
| 28 | DeepARU01 | DeepAR | -132.284043 | -81.921335 | 110.66 | 28 |
| 29 | DeepARU02 | DeepAR | -155.639475 | -72.147861 | 140.91 | 29 |
| 30 | DeepARU03 | DeepAR | -130.802738 | -81.807523 | 111.94 | 30 |
| 31 | WeightedEnsemble | WeightedEnsemble | -128.131856 | -46.563322 | 5.91 | 31 |

## 6. 해석

- 이번 실행은 균일 모델수 모드(10개 모델군 × 3변형)를 기준으로 학습되었습니다.
- 이번에는 각 모델군이 계획된 변형 수를 모두 학습해, 모델 수 분배가 사실상 균등하게 달성되었습니다.
- 최종적으로 WeightedEnsemble이 추가되어 총 모델 수는 31개입니다.