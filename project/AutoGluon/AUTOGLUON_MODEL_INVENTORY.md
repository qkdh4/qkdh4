# AutoGluon(TimeSeries) 활용 모델 전체 정리

## 1. 기준 파일

- [model_leaderboard.csv](./results/model_leaderboard.csv)
- [prediction_summary.json](./results/prediction_summary.json)

## 2. 전체 규모

- 전체 학습 모델 수: **313개**
- 베스트 모델: **DeepAR\63106_00066**
- 앙상블 모델: **WeightedEnsemble**

## 3. 모델 계열별 요약

| 모델 계열 | 모델 수 | 최고 score_test | 최고 score_val | 평균 fit_time_marginal(초) |
|---|---:|---:|---:|---:|
| DeepAR | 217 | -71.365734 | -58.257357 | 753.45 |
| TemporalFusionTransformer | 90 | -102.747049 | -47.124612 | 1721.65 |
| DirectTabular | 1 | -99.213514 | -79.743251 | 3.16 |
| AutoETS | 1 | -137.292565 | -70.568691 | 5.82 |
| DynamicOptimizedTheta | 1 | -135.052695 | -70.122884 | 10.21 |
| RecursiveTabular | 1 | -89.994605 | -85.168893 | 3.44 |
| SeasonalNaive | 1 | -159.371534 | -107.567571 | 9.89 |
| WeightedEnsemble | 1 | -189.911396 | -43.853070 | 60.00 |

## 4. 활용된 전체 모델 목록 (전부)

아래 목록은 `model_leaderboard.csv`의 전체 행(313개)을 `fit_order` 기준으로 정렬한 것입니다.

| # | 모델명 | 계열 | score_test | score_val | fit_time_marginal(초) | fit_order |
|---:|---|---|---:|---:|---:|---:|
| 1 | SeasonalNaive | SeasonalNaive | -159.371534 | -107.567571 | 9.89 | 1 |
| 2 | RecursiveTabular | RecursiveTabular | -89.994605 | -85.168893 | 3.44 | 2 |
| 3 | DirectTabular | DirectTabular | -99.213514 | -79.743251 | 3.16 | 3 |
| 4 | DynamicOptimizedTheta | DynamicOptimizedTheta | -135.052695 | -70.122884 | 10.21 | 4 |
| 5 | AutoETS | AutoETS | -137.292565 | -70.568691 | 5.82 | 5 |
| 6 | TemporalFusionTransformer\8ac13_00000 | TemporalFusionTransformer | -153.611521 | -53.512613 | 1797.51 | 6 |
| 7 | TemporalFusionTransformer\8ac13_00004 | TemporalFusionTransformer | -147.382750 | -58.217581 | 1857.31 | 7 |
| 8 | TemporalFusionTransformer\8ac13_00006 | TemporalFusionTransformer | -129.726631 | -53.032942 | 1793.58 | 8 |
| 9 | TemporalFusionTransformer\8ac13_00009 | TemporalFusionTransformer | -195.833076 | -58.942404 | 1197.35 | 9 |
| 10 | TemporalFusionTransformer\8ac13_00016 | TemporalFusionTransformer | -138.552393 | -70.580597 | 1789.34 | 10 |
| 11 | TemporalFusionTransformer\8ac13_00018 | TemporalFusionTransformer | -149.490372 | -54.933486 | 1799.71 | 11 |
| 12 | TemporalFusionTransformer\8ac13_00020 | TemporalFusionTransformer | -133.913437 | -74.976047 | 2246.41 | 12 |
| 13 | TemporalFusionTransformer\8ac13_00022 | TemporalFusionTransformer | -147.094374 | -53.017942 | 2353.84 | 13 |
| 14 | TemporalFusionTransformer\8ac13_00026 | TemporalFusionTransformer | -121.018463 | -59.280437 | 1622.97 | 14 |
| 15 | TemporalFusionTransformer\8ac13_00028 | TemporalFusionTransformer | -147.190302 | -67.179405 | 1676.96 | 15 |
| 16 | TemporalFusionTransformer\8ac13_00029 | TemporalFusionTransformer | -122.390768 | -67.277143 | 2022.12 | 16 |
| 17 | TemporalFusionTransformer\8ac13_00037 | TemporalFusionTransformer | -157.609868 | -50.581813 | 1643.06 | 17 |
| 18 | TemporalFusionTransformer\8ac13_00039 | TemporalFusionTransformer | -143.384212 | -53.274011 | 1489.28 | 18 |
| 19 | TemporalFusionTransformer\8ac13_00049 | TemporalFusionTransformer | -140.722962 | -55.178376 | 1494.19 | 19 |
| 20 | TemporalFusionTransformer\8ac13_00050 | TemporalFusionTransformer | -145.744219 | -52.679405 | 1682.89 | 20 |
| 21 | TemporalFusionTransformer\8ac13_00056 | TemporalFusionTransformer | -174.051859 | -63.977710 | 1639.17 | 21 |
| 22 | TemporalFusionTransformer\8ac13_00059 | TemporalFusionTransformer | -124.071405 | -53.763331 | 1802.05 | 22 |
| 23 | TemporalFusionTransformer\8ac13_00062 | TemporalFusionTransformer | -150.123196 | -60.597772 | 1500.85 | 23 |
| 24 | TemporalFusionTransformer\8ac13_00063 | TemporalFusionTransformer | -104.981292 | -52.888008 | 1707.11 | 24 |
| 25 | TemporalFusionTransformer\8ac13_00067 | TemporalFusionTransformer | -144.194644 | -61.742427 | 1913.49 | 25 |
| 26 | TemporalFusionTransformer\8ac13_00072 | TemporalFusionTransformer | -160.664107 | -61.375778 | 1791.41 | 26 |
| 27 | TemporalFusionTransformer\8ac13_00073 | TemporalFusionTransformer | -142.381234 | -55.995256 | 1924.65 | 27 |
| 28 | TemporalFusionTransformer\8ac13_00075 | TemporalFusionTransformer | -158.945633 | -53.268355 | 1692.36 | 28 |
| 29 | TemporalFusionTransformer\8ac13_00082 | TemporalFusionTransformer | -185.464298 | -52.047685 | 1978.29 | 29 |
| 30 | TemporalFusionTransformer\8ac13_00084 | TemporalFusionTransformer | -136.767501 | -55.535568 | 1945.90 | 30 |
| 31 | TemporalFusionTransformer\8ac13_00086 | TemporalFusionTransformer | -119.140791 | -50.011669 | 1292.90 | 31 |
| 32 | TemporalFusionTransformer\8ac13_00090 | TemporalFusionTransformer | -131.836528 | -54.917131 | 1897.87 | 32 |
| 33 | TemporalFusionTransformer\8ac13_00091 | TemporalFusionTransformer | -152.520652 | -56.814838 | 1712.90 | 33 |
| 34 | TemporalFusionTransformer\8ac13_00094 | TemporalFusionTransformer | -124.020437 | -53.871908 | 2034.01 | 34 |
| 35 | TemporalFusionTransformer\8ac13_00101 | TemporalFusionTransformer | -152.855953 | -63.564629 | 1842.22 | 35 |
| 36 | TemporalFusionTransformer\8ac13_00105 | TemporalFusionTransformer | -154.153804 | -53.030804 | 1656.90 | 36 |
| 37 | TemporalFusionTransformer\8ac13_00106 | TemporalFusionTransformer | -140.784623 | -65.901900 | 2206.46 | 37 |
| 38 | TemporalFusionTransformer\8ac13_00108 | TemporalFusionTransformer | -182.044295 | -56.876349 | 1448.72 | 38 |
| 39 | TemporalFusionTransformer\8ac13_00109 | TemporalFusionTransformer | -146.447321 | -54.766167 | 1952.77 | 39 |
| 40 | TemporalFusionTransformer\8ac13_00111 | TemporalFusionTransformer | -150.099514 | -70.146190 | 1642.93 | 40 |
| 41 | TemporalFusionTransformer\8ac13_00116 | TemporalFusionTransformer | -157.101446 | -56.877100 | 1604.90 | 41 |
| 42 | TemporalFusionTransformer\8ac13_00122 | TemporalFusionTransformer | -106.045232 | -54.452639 | 2036.00 | 42 |
| 43 | TemporalFusionTransformer\8ac13_00125 | TemporalFusionTransformer | -155.888585 | -74.029630 | 2063.21 | 43 |
| 44 | TemporalFusionTransformer\8ac13_00126 | TemporalFusionTransformer | -153.926880 | -69.397793 | 2469.50 | 44 |
| 45 | TemporalFusionTransformer\8ac13_00130 | TemporalFusionTransformer | -153.886134 | -57.170823 | 1366.29 | 45 |
| 46 | TemporalFusionTransformer\8ac13_00135 | TemporalFusionTransformer | -144.327888 | -61.139142 | 2071.64 | 46 |
| 47 | TemporalFusionTransformer\8ac13_00137 | TemporalFusionTransformer | -176.127588 | -50.542270 | 1161.76 | 47 |
| 48 | TemporalFusionTransformer\8ac13_00139 | TemporalFusionTransformer | -137.075095 | -54.744770 | 1953.61 | 48 |
| 49 | TemporalFusionTransformer\8ac13_00142 | TemporalFusionTransformer | -150.907829 | -66.261188 | 2000.14 | 49 |
| 50 | TemporalFusionTransformer\8ac13_00146 | TemporalFusionTransformer | -162.409523 | -56.749679 | 1633.77 | 50 |
| 51 | TemporalFusionTransformer\8ac13_00149 | TemporalFusionTransformer | -102.747049 | -56.166558 | 1509.99 | 51 |
| 52 | TemporalFusionTransformer\8ac13_00154 | TemporalFusionTransformer | -144.407045 | -52.816738 | 1647.86 | 52 |
| 53 | TemporalFusionTransformer\8ac13_00155 | TemporalFusionTransformer | -166.496868 | -52.261429 | 1715.24 | 53 |
| 54 | TemporalFusionTransformer\8ac13_00157 | TemporalFusionTransformer | -112.764756 | -65.421259 | 1928.77 | 54 |
| 55 | TemporalFusionTransformer\8ac13_00163 | TemporalFusionTransformer | -137.303896 | -60.728682 | 1749.51 | 55 |
| 56 | TemporalFusionTransformer\8ac13_00169 | TemporalFusionTransformer | -148.230685 | -52.219547 | 1936.16 | 56 |
| 57 | TemporalFusionTransformer\8ac13_00174 | TemporalFusionTransformer | -132.315085 | -58.195103 | 2199.62 | 57 |
| 58 | TemporalFusionTransformer\8ac13_00175 | TemporalFusionTransformer | -138.532351 | -52.184596 | 1681.96 | 58 |
| 59 | TemporalFusionTransformer\8ac13_00176 | TemporalFusionTransformer | -184.204663 | -51.282149 | 2443.62 | 59 |
| 60 | TemporalFusionTransformer\8ac13_00178 | TemporalFusionTransformer | -145.510692 | -48.293767 | 2254.16 | 60 |
| 61 | TemporalFusionTransformer\8ac13_00181 | TemporalFusionTransformer | -131.063512 | -57.619836 | 2268.05 | 61 |
| 62 | TemporalFusionTransformer\8ac13_00186 | TemporalFusionTransformer | -184.647801 | -62.397834 | 1429.92 | 62 |
| 63 | TemporalFusionTransformer\8ac13_00188 | TemporalFusionTransformer | -167.893509 | -47.663997 | 1308.40 | 63 |
| 64 | TemporalFusionTransformer\8ac13_00190 | TemporalFusionTransformer | -141.712689 | -61.743896 | 1633.56 | 64 |
| 65 | TemporalFusionTransformer\8ac13_00199 | TemporalFusionTransformer | -166.774287 | -51.203161 | 1749.19 | 65 |
| 66 | TemporalFusionTransformer\8ac13_00206 | TemporalFusionTransformer | -202.706762 | -55.155395 | 1793.48 | 66 |
| 67 | TemporalFusionTransformer\8ac13_00211 | TemporalFusionTransformer | -148.289254 | -57.432937 | 1618.72 | 67 |
| 68 | TemporalFusionTransformer\8ac13_00219 | TemporalFusionTransformer | -150.305604 | -49.221875 | 1322.75 | 68 |
| 69 | TemporalFusionTransformer\8ac13_00220 | TemporalFusionTransformer | -141.451731 | -69.537837 | 2466.13 | 69 |
| 70 | TemporalFusionTransformer\8ac13_00224 | TemporalFusionTransformer | -151.907116 | -66.460567 | 1808.80 | 70 |
| 71 | TemporalFusionTransformer\8ac13_00232 | TemporalFusionTransformer | -164.205908 | -57.140326 | 2125.22 | 71 |
| 72 | TemporalFusionTransformer\8ac13_00235 | TemporalFusionTransformer | -181.276391 | -51.356144 | 2888.48 | 72 |
| 73 | TemporalFusionTransformer\8ac13_00241 | TemporalFusionTransformer | -148.157386 | -58.433518 | 2196.79 | 73 |
| 74 | TemporalFusionTransformer\8ac13_00246 | TemporalFusionTransformer | -179.196656 | -53.225989 | 2153.01 | 74 |
| 75 | TemporalFusionTransformer\8ac13_00247 | TemporalFusionTransformer | -132.674523 | -60.956459 | 1763.89 | 75 |
| 76 | TemporalFusionTransformer\8ac13_00249 | TemporalFusionTransformer | -130.484564 | -60.803097 | 1580.87 | 76 |
| 77 | TemporalFusionTransformer\8ac13_00250 | TemporalFusionTransformer | -151.645448 | -50.779699 | 1805.91 | 77 |
| 78 | TemporalFusionTransformer\8ac13_00255 | TemporalFusionTransformer | -161.509247 | -52.542595 | 1681.28 | 78 |
| 79 | TemporalFusionTransformer\8ac13_00256 | TemporalFusionTransformer | -130.037943 | -68.815840 | 2009.46 | 79 |
| 80 | TemporalFusionTransformer\8ac13_00257 | TemporalFusionTransformer | -145.289016 | -60.580999 | 2317.33 | 80 |
| 81 | TemporalFusionTransformer\8ac13_00263 | TemporalFusionTransformer | -156.682735 | -88.632555 | 1841.27 | 81 |
| 82 | TemporalFusionTransformer\8ac13_00266 | TemporalFusionTransformer | -161.433606 | -65.200440 | 1837.16 | 82 |
| 83 | TemporalFusionTransformer\8ac13_00268 | TemporalFusionTransformer | -150.708518 | -59.119800 | 1921.40 | 83 |
| 84 | TemporalFusionTransformer\8ac13_00276 | TemporalFusionTransformer | -142.641783 | -56.450591 | 1664.97 | 84 |
| 85 | TemporalFusionTransformer\8ac13_00278 | TemporalFusionTransformer | -159.561843 | -51.204227 | 1680.95 | 85 |
| 86 | TemporalFusionTransformer\8ac13_00280 | TemporalFusionTransformer | -172.477374 | -60.520689 | 1683.94 | 86 |
| 87 | TemporalFusionTransformer\8ac13_00284 | TemporalFusionTransformer | -150.192682 | -53.765742 | 1567.01 | 87 |
| 88 | TemporalFusionTransformer\8ac13_00295 | TemporalFusionTransformer | -163.815672 | -52.495405 | 1233.60 | 88 |
| 89 | TemporalFusionTransformer\8ac13_00300 | TemporalFusionTransformer | -136.410022 | -67.182815 | 1109.34 | 89 |
| 90 | TemporalFusionTransformer\8ac13_00310 | TemporalFusionTransformer | -154.126158 | -47.124612 | 886.40 | 90 |
| 91 | TemporalFusionTransformer\8ac13_00312 | TemporalFusionTransformer | -144.194409 | -59.659408 | 790.45 | 91 |
| 92 | TemporalFusionTransformer\8ac13_00313 | TemporalFusionTransformer | -161.687077 | -55.367069 | 776.50 | 92 |
| 93 | TemporalFusionTransformer\8ac13_00316 | TemporalFusionTransformer | -153.134427 | -51.833319 | 400.88 | 93 |
| 94 | TemporalFusionTransformer\8ac13_00321 | TemporalFusionTransformer | -173.357901 | -75.877770 | 124.64 | 94 |
| 95 | TemporalFusionTransformer\8ac13_00330 | TemporalFusionTransformer | -107.330562 | -75.461104 | 31.68 | 95 |
| 96 | DeepAR\63106_00000 | DeepAR | -149.980872 | -95.042418 | 283.10 | 96 |
| 97 | DeepAR\63106_00001 | DeepAR | -165.125137 | -97.820398 | 857.58 | 97 |
| 98 | DeepAR\63106_00002 | DeepAR | -141.087981 | -67.896507 | 1437.11 | 98 |
| 99 | DeepAR\63106_00003 | DeepAR | -151.327359 | -89.368214 | 1107.43 | 99 |
| 100 | DeepAR\63106_00004 | DeepAR | -101.228125 | -83.263539 | 505.14 | 100 |
| 101 | DeepAR\63106_00005 | DeepAR | -187.834844 | -70.388495 | 654.69 | 101 |
| 102 | DeepAR\63106_00006 | DeepAR | -156.783479 | -84.783839 | 274.84 | 102 |
| 103 | DeepAR\63106_00007 | DeepAR | -127.824807 | -63.422345 | 921.01 | 103 |
| 104 | DeepAR\63106_00008 | DeepAR | -120.766061 | -69.976357 | 836.07 | 104 |
| 105 | DeepAR\63106_00009 | DeepAR | -204.600562 | -79.053199 | 476.66 | 105 |
| 106 | DeepAR\63106_00010 | DeepAR | -155.860721 | -75.608968 | 1977.50 | 106 |
| 107 | DeepAR\63106_00011 | DeepAR | -143.352883 | -84.824042 | 296.71 | 107 |
| 108 | DeepAR\63106_00012 | DeepAR | -190.042245 | -75.755790 | 649.34 | 108 |
| 109 | DeepAR\63106_00013 | DeepAR | -161.142129 | -82.373880 | 291.49 | 109 |
| 110 | DeepAR\63106_00014 | DeepAR | -178.373770 | -74.111414 | 537.19 | 110 |
| 111 | DeepAR\63106_00015 | DeepAR | -130.961574 | -87.005426 | 385.11 | 111 |
| 112 | DeepAR\63106_00016 | DeepAR | -190.465950 | -85.357966 | 336.06 | 112 |
| 113 | DeepAR\63106_00017 | DeepAR | -151.559000 | -78.569208 | 319.76 | 113 |
| 114 | DeepAR\63106_00018 | DeepAR | -206.872849 | -82.703731 | 1286.91 | 114 |
| 115 | DeepAR\63106_00019 | DeepAR | -199.834517 | -76.160364 | 1340.53 | 115 |
| 116 | DeepAR\63106_00020 | DeepAR | -223.696755 | -69.396186 | 494.41 | 116 |
| 117 | DeepAR\63106_00021 | DeepAR | -169.338830 | -67.509745 | 795.62 | 117 |
| 118 | DeepAR\63106_00022 | DeepAR | -169.519206 | -88.047539 | 1844.68 | 118 |
| 119 | DeepAR\63106_00023 | DeepAR | -165.646637 | -73.116311 | 490.30 | 119 |
| 120 | DeepAR\63106_00024 | DeepAR | -110.662169 | -83.915151 | 389.31 | 120 |
| 121 | DeepAR\63106_00025 | DeepAR | -167.100875 | -67.106244 | 395.86 | 121 |
| 122 | DeepAR\63106_00026 | DeepAR | -178.094708 | -83.182227 | 390.37 | 122 |
| 123 | DeepAR\63106_00027 | DeepAR | -230.787849 | -77.742516 | 1348.55 | 123 |
| 124 | DeepAR\63106_00028 | DeepAR | -167.921311 | -82.498591 | 282.96 | 124 |
| 125 | DeepAR\63106_00029 | DeepAR | -159.826683 | -81.056912 | 338.02 | 125 |
| 126 | DeepAR\63106_00030 | DeepAR | -162.644843 | -73.590837 | 1817.66 | 126 |
| 127 | DeepAR\63106_00031 | DeepAR | -162.079628 | -70.542185 | 396.46 | 127 |
| 128 | DeepAR\63106_00032 | DeepAR | -158.601723 | -67.917285 | 814.12 | 128 |
| 129 | DeepAR\63106_00033 | DeepAR | -85.921076 | -94.127863 | 297.08 | 129 |
| 130 | DeepAR\63106_00034 | DeepAR | -210.895970 | -78.837915 | 529.43 | 130 |
| 131 | DeepAR\63106_00035 | DeepAR | -182.519977 | -83.715433 | 1568.40 | 131 |
| 132 | DeepAR\63106_00036 | DeepAR | -148.272432 | -82.937711 | 325.36 | 132 |
| 133 | DeepAR\63106_00037 | DeepAR | -137.121600 | -86.571729 | 285.59 | 133 |
| 134 | DeepAR\63106_00038 | DeepAR | -184.220272 | -87.879706 | 464.85 | 134 |
| 135 | DeepAR\63106_00039 | DeepAR | -182.168770 | -78.966148 | 626.32 | 135 |
| 136 | DeepAR\63106_00040 | DeepAR | -147.209271 | -95.008650 | 306.44 | 136 |
| 137 | DeepAR\63106_00041 | DeepAR | -129.838485 | -79.027611 | 698.67 | 137 |
| 138 | DeepAR\63106_00042 | DeepAR | -180.281090 | -96.342634 | 367.93 | 138 |
| 139 | DeepAR\63106_00043 | DeepAR | -118.171702 | -68.831685 | 590.48 | 139 |
| 140 | DeepAR\63106_00044 | DeepAR | -274.191352 | -64.338485 | 1870.01 | 140 |
| 141 | DeepAR\63106_00045 | DeepAR | -179.880640 | -73.517445 | 513.79 | 141 |
| 142 | DeepAR\63106_00046 | DeepAR | -139.944629 | -88.025064 | 967.86 | 142 |
| 143 | DeepAR\63106_00047 | DeepAR | -128.273430 | -71.060911 | 1202.99 | 143 |
| 144 | DeepAR\63106_00048 | DeepAR | -137.625061 | -75.537400 | 453.51 | 144 |
| 145 | DeepAR\63106_00049 | DeepAR | -170.825169 | -78.545123 | 866.85 | 145 |
| 146 | DeepAR\63106_00050 | DeepAR | -195.214732 | -74.367337 | 678.36 | 146 |
| 147 | DeepAR\63106_00051 | DeepAR | -115.855514 | -84.860562 | 744.21 | 147 |
| 148 | DeepAR\63106_00052 | DeepAR | -173.167902 | -94.801350 | 340.24 | 148 |
| 149 | DeepAR\63106_00053 | DeepAR | -114.969350 | -68.052023 | 986.28 | 149 |
| 150 | DeepAR\63106_00054 | DeepAR | -145.410004 | -81.599831 | 330.77 | 150 |
| 151 | DeepAR\63106_00055 | DeepAR | -129.842471 | -90.518752 | 1385.63 | 151 |
| 152 | DeepAR\63106_00056 | DeepAR | -100.114881 | -81.186551 | 378.31 | 152 |
| 153 | DeepAR\63106_00057 | DeepAR | -170.293180 | -84.796274 | 400.50 | 153 |
| 154 | DeepAR\63106_00058 | DeepAR | -211.318245 | -87.084825 | 907.29 | 154 |
| 155 | DeepAR\63106_00059 | DeepAR | -195.574837 | -90.843205 | 484.56 | 155 |
| 156 | DeepAR\63106_00060 | DeepAR | -174.070369 | -89.002477 | 514.80 | 156 |
| 157 | DeepAR\63106_00061 | DeepAR | -113.253640 | -65.357835 | 1194.66 | 157 |
| 158 | DeepAR\63106_00062 | DeepAR | -144.671303 | -86.715136 | 447.29 | 158 |
| 159 | DeepAR\63106_00063 | DeepAR | -93.235308 | -88.631385 | 2251.85 | 159 |
| 160 | DeepAR\63106_00064 | DeepAR | -177.206850 | -71.724787 | 418.87 | 160 |
| 161 | DeepAR\63106_00065 | DeepAR | -180.492833 | -69.058479 | 312.71 | 161 |
| 162 | DeepAR\63106_00066 | DeepAR | -71.365734 | -85.195421 | 499.83 | 162 |
| 163 | DeepAR\63106_00067 | DeepAR | -96.167650 | -76.569008 | 802.56 | 163 |
| 164 | DeepAR\63106_00068 | DeepAR | -183.882040 | -86.706907 | 719.49 | 164 |
| 165 | DeepAR\63106_00069 | DeepAR | -144.311051 | -70.181246 | 1183.75 | 165 |
| 166 | DeepAR\63106_00070 | DeepAR | -156.799184 | -81.145832 | 637.31 | 166 |
| 167 | DeepAR\63106_00071 | DeepAR | -130.678207 | -82.711186 | 440.12 | 167 |
| 168 | DeepAR\63106_00072 | DeepAR | -136.041518 | -77.586136 | 914.24 | 168 |
| 169 | DeepAR\63106_00073 | DeepAR | -189.179963 | -80.863993 | 860.84 | 169 |
| 170 | DeepAR\63106_00074 | DeepAR | -138.745544 | -68.658901 | 745.34 | 170 |
| 171 | DeepAR\63106_00075 | DeepAR | -176.817417 | -67.844292 | 762.38 | 171 |
| 172 | DeepAR\63106_00076 | DeepAR | -252.319673 | -90.635164 | 574.76 | 172 |
| 173 | DeepAR\63106_00077 | DeepAR | -177.412218 | -77.042861 | 543.95 | 173 |
| 174 | DeepAR\63106_00078 | DeepAR | -87.099716 | -78.946533 | 489.29 | 174 |
| 175 | DeepAR\63106_00079 | DeepAR | -198.523830 | -73.029441 | 745.05 | 175 |
| 176 | DeepAR\63106_00080 | DeepAR | -182.281164 | -81.795954 | 338.51 | 176 |
| 177 | DeepAR\63106_00081 | DeepAR | -178.496251 | -72.200264 | 1470.30 | 177 |
| 178 | DeepAR\63106_00082 | DeepAR | -186.357146 | -70.009708 | 242.14 | 178 |
| 179 | DeepAR\63106_00083 | DeepAR | -99.253059 | -89.787498 | 445.90 | 179 |
| 180 | DeepAR\63106_00084 | DeepAR | -219.712716 | -62.460924 | 1257.16 | 180 |
| 181 | DeepAR\63106_00085 | DeepAR | -176.823041 | -67.627262 | 588.18 | 181 |
| 182 | DeepAR\63106_00086 | DeepAR | -141.357743 | -87.708234 | 283.92 | 182 |
| 183 | DeepAR\63106_00087 | DeepAR | -87.306587 | -74.703404 | 1643.41 | 183 |
| 184 | DeepAR\63106_00088 | DeepAR | -177.875040 | -76.517333 | 595.31 | 184 |
| 185 | DeepAR\63106_00089 | DeepAR | -146.355943 | -81.522840 | 274.36 | 185 |
| 186 | DeepAR\63106_00090 | DeepAR | -137.371793 | -62.859010 | 650.08 | 186 |
| 187 | DeepAR\63106_00091 | DeepAR | -133.453630 | -61.483716 | 483.01 | 187 |
| 188 | DeepAR\63106_00092 | DeepAR | -144.548370 | -71.766102 | 738.25 | 188 |
| 189 | DeepAR\63106_00093 | DeepAR | -136.817212 | -76.564951 | 966.82 | 189 |
| 190 | DeepAR\63106_00094 | DeepAR | -170.915328 | -76.733716 | 468.73 | 190 |
| 191 | DeepAR\63106_00095 | DeepAR | -130.622138 | -86.561732 | 864.28 | 191 |
| 192 | DeepAR\63106_00096 | DeepAR | -143.717372 | -94.691352 | 471.44 | 192 |
| 193 | DeepAR\63106_00097 | DeepAR | -169.408968 | -73.538393 | 444.45 | 193 |
| 194 | DeepAR\63106_00098 | DeepAR | -130.568275 | -84.185605 | 481.01 | 194 |
| 195 | DeepAR\63106_00099 | DeepAR | -216.024430 | -86.423957 | 565.25 | 195 |
| 196 | DeepAR\63106_00100 | DeepAR | -95.869003 | -72.537310 | 572.34 | 196 |
| 197 | DeepAR\63106_00101 | DeepAR | -203.391623 | -66.731859 | 748.15 | 197 |
| 198 | DeepAR\63106_00102 | DeepAR | -202.414166 | -75.227259 | 485.47 | 198 |
| 199 | DeepAR\63106_00103 | DeepAR | -128.820323 | -73.852467 | 2213.78 | 199 |
| 200 | DeepAR\63106_00104 | DeepAR | -117.332711 | -87.826902 | 530.85 | 200 |
| 201 | DeepAR\63106_00105 | DeepAR | -155.804463 | -86.469241 | 548.71 | 201 |
| 202 | DeepAR\63106_00106 | DeepAR | -134.837598 | -60.039938 | 1278.71 | 202 |
| 203 | DeepAR\63106_00107 | DeepAR | -115.628340 | -86.137243 | 646.20 | 203 |
| 204 | DeepAR\63106_00108 | DeepAR | -153.961924 | -87.075239 | 1430.24 | 204 |
| 205 | DeepAR\63106_00109 | DeepAR | -171.674736 | -76.587575 | 303.86 | 205 |
| 206 | DeepAR\63106_00110 | DeepAR | -129.990883 | -76.591474 | 813.71 | 206 |
| 207 | DeepAR\63106_00111 | DeepAR | -180.106611 | -66.560757 | 342.20 | 207 |
| 208 | DeepAR\63106_00112 | DeepAR | -157.540037 | -79.332018 | 937.63 | 208 |
| 209 | DeepAR\63106_00113 | DeepAR | -89.529356 | -75.670497 | 482.47 | 209 |
| 210 | DeepAR\63106_00114 | DeepAR | -163.182750 | -76.273316 | 327.05 | 210 |
| 211 | DeepAR\63106_00115 | DeepAR | -96.904189 | -77.664319 | 993.02 | 211 |
| 212 | DeepAR\63106_00116 | DeepAR | -196.693315 | -61.649527 | 808.54 | 212 |
| 213 | DeepAR\63106_00117 | DeepAR | -199.694674 | -83.229377 | 663.52 | 213 |
| 214 | DeepAR\63106_00118 | DeepAR | -139.854632 | -64.004047 | 1597.23 | 214 |
| 215 | DeepAR\63106_00119 | DeepAR | -169.374615 | -61.510767 | 994.39 | 215 |
| 216 | DeepAR\63106_00120 | DeepAR | -156.943000 | -76.503486 | 687.22 | 216 |
| 217 | DeepAR\63106_00121 | DeepAR | -142.754809 | -74.951384 | 1320.51 | 217 |
| 218 | DeepAR\63106_00122 | DeepAR | -164.145229 | -86.958256 | 641.27 | 218 |
| 219 | DeepAR\63106_00123 | DeepAR | -103.889432 | -83.270275 | 604.90 | 219 |
| 220 | DeepAR\63106_00124 | DeepAR | -169.556232 | -79.019510 | 966.57 | 220 |
| 221 | DeepAR\63106_00125 | DeepAR | -144.978082 | -74.645228 | 384.02 | 221 |
| 222 | DeepAR\63106_00126 | DeepAR | -171.550444 | -76.681681 | 509.39 | 222 |
| 223 | DeepAR\63106_00127 | DeepAR | -176.656116 | -81.913486 | 506.82 | 223 |
| 224 | DeepAR\63106_00128 | DeepAR | -187.495101 | -87.928501 | 575.37 | 224 |
| 225 | DeepAR\63106_00129 | DeepAR | -182.388545 | -82.723032 | 976.75 | 225 |
| 226 | DeepAR\63106_00130 | DeepAR | -113.102926 | -87.594165 | 625.67 | 226 |
| 227 | DeepAR\63106_00131 | DeepAR | -152.558744 | -79.656614 | 864.07 | 227 |
| 228 | DeepAR\63106_00132 | DeepAR | -143.811144 | -89.523879 | 678.72 | 228 |
| 229 | DeepAR\63106_00133 | DeepAR | -112.732478 | -76.493259 | 720.31 | 229 |
| 230 | DeepAR\63106_00134 | DeepAR | -144.055721 | -79.827648 | 810.49 | 230 |
| 231 | DeepAR\63106_00135 | DeepAR | -150.093232 | -98.244781 | 593.62 | 231 |
| 232 | DeepAR\63106_00136 | DeepAR | -156.070109 | -75.037923 | 933.43 | 232 |
| 233 | DeepAR\63106_00137 | DeepAR | -179.485468 | -78.389369 | 664.86 | 233 |
| 234 | DeepAR\63106_00138 | DeepAR | -187.859051 | -71.967524 | 1859.24 | 234 |
| 235 | DeepAR\63106_00139 | DeepAR | -140.442119 | -91.625707 | 250.36 | 235 |
| 236 | DeepAR\63106_00140 | DeepAR | -120.518036 | -78.027286 | 1121.85 | 236 |
| 237 | DeepAR\63106_00141 | DeepAR | -144.908489 | -92.018867 | 275.61 | 237 |
| 238 | DeepAR\63106_00142 | DeepAR | -136.585642 | -94.709324 | 919.30 | 238 |
| 239 | DeepAR\63106_00143 | DeepAR | -174.240274 | -63.293236 | 315.77 | 239 |
| 240 | DeepAR\63106_00144 | DeepAR | -187.824379 | -68.536747 | 1000.17 | 240 |
| 241 | DeepAR\63106_00145 | DeepAR | -148.778418 | -75.574154 | 460.98 | 241 |
| 242 | DeepAR\63106_00146 | DeepAR | -126.628109 | -81.645671 | 538.06 | 242 |
| 243 | DeepAR\63106_00147 | DeepAR | -162.886906 | -85.279488 | 415.34 | 243 |
| 244 | DeepAR\63106_00148 | DeepAR | -169.955632 | -78.483941 | 981.15 | 244 |
| 245 | DeepAR\63106_00149 | DeepAR | -136.519577 | -58.398585 | 949.90 | 245 |
| 246 | DeepAR\63106_00150 | DeepAR | -192.491600 | -84.547750 | 742.48 | 246 |
| 247 | DeepAR\63106_00151 | DeepAR | -111.728510 | -86.307014 | 2271.71 | 247 |
| 248 | DeepAR\63106_00152 | DeepAR | -251.464165 | -85.329386 | 1297.01 | 248 |
| 249 | DeepAR\63106_00153 | DeepAR | -193.853828 | -81.096275 | 1704.07 | 249 |
| 250 | DeepAR\63106_00154 | DeepAR | -201.236599 | -75.474104 | 1267.70 | 250 |
| 251 | DeepAR\63106_00155 | DeepAR | -157.388367 | -87.616427 | 1209.37 | 251 |
| 252 | DeepAR\63106_00156 | DeepAR | -164.986220 | -107.900274 | 592.30 | 252 |
| 253 | DeepAR\63106_00157 | DeepAR | -200.178940 | -89.597532 | 364.15 | 253 |
| 254 | DeepAR\63106_00158 | DeepAR | -82.734229 | -69.151358 | 937.36 | 254 |
| 255 | DeepAR\63106_00159 | DeepAR | -192.638761 | -72.891473 | 1269.33 | 255 |
| 256 | DeepAR\63106_00160 | DeepAR | -135.664498 | -67.330480 | 722.68 | 256 |
| 257 | DeepAR\63106_00161 | DeepAR | -162.499416 | -73.602768 | 676.83 | 257 |
| 258 | DeepAR\63106_00162 | DeepAR | -156.348144 | -82.776589 | 736.81 | 258 |
| 259 | DeepAR\63106_00163 | DeepAR | -130.856833 | -86.807510 | 561.90 | 259 |
| 260 | DeepAR\63106_00164 | DeepAR | -140.400030 | -87.004949 | 723.61 | 260 |
| 261 | DeepAR\63106_00165 | DeepAR | -163.446918 | -77.535739 | 812.95 | 261 |
| 262 | DeepAR\63106_00166 | DeepAR | -164.741112 | -76.627997 | 1514.04 | 262 |
| 263 | DeepAR\63106_00167 | DeepAR | -109.424766 | -70.277972 | 2141.38 | 263 |
| 264 | DeepAR\63106_00168 | DeepAR | -210.390275 | -85.339774 | 501.87 | 264 |
| 265 | DeepAR\63106_00169 | DeepAR | -165.943827 | -79.673911 | 646.34 | 265 |
| 266 | DeepAR\63106_00170 | DeepAR | -184.498272 | -70.390548 | 593.60 | 266 |
| 267 | DeepAR\63106_00171 | DeepAR | -108.242458 | -66.796596 | 307.04 | 267 |
| 268 | DeepAR\63106_00172 | DeepAR | -112.278362 | -81.674493 | 801.87 | 268 |
| 269 | DeepAR\63106_00173 | DeepAR | -147.821860 | -88.053399 | 886.73 | 269 |
| 270 | DeepAR\63106_00174 | DeepAR | -153.237401 | -80.432970 | 460.87 | 270 |
| 271 | DeepAR\63106_00175 | DeepAR | -127.428475 | -81.296395 | 569.30 | 271 |
| 272 | DeepAR\63106_00176 | DeepAR | -163.214374 | -78.999681 | 616.28 | 272 |
| 273 | DeepAR\63106_00177 | DeepAR | -181.133185 | -78.047212 | 1041.65 | 273 |
| 274 | DeepAR\63106_00178 | DeepAR | -185.770447 | -81.464654 | 518.35 | 274 |
| 275 | DeepAR\63106_00179 | DeepAR | -206.940919 | -80.490433 | 1127.96 | 275 |
| 276 | DeepAR\63106_00180 | DeepAR | -227.727471 | -82.657027 | 954.50 | 276 |
| 277 | DeepAR\63106_00181 | DeepAR | -72.471905 | -73.022791 | 456.31 | 277 |
| 278 | DeepAR\63106_00182 | DeepAR | -166.846817 | -75.473532 | 1390.73 | 278 |
| 279 | DeepAR\63106_00183 | DeepAR | -157.372841 | -81.475744 | 556.44 | 279 |
| 280 | DeepAR\63106_00184 | DeepAR | -166.308698 | -78.926590 | 1636.33 | 280 |
| 281 | DeepAR\63106_00185 | DeepAR | -136.154837 | -89.572288 | 648.47 | 281 |
| 282 | DeepAR\63106_00186 | DeepAR | -144.008157 | -76.734763 | 899.16 | 282 |
| 283 | DeepAR\63106_00187 | DeepAR | -144.733988 | -87.583878 | 265.48 | 283 |
| 284 | DeepAR\63106_00188 | DeepAR | -129.656202 | -72.583588 | 993.66 | 284 |
| 285 | DeepAR\63106_00189 | DeepAR | -134.131048 | -80.480522 | 623.26 | 285 |
| 286 | DeepAR\63106_00190 | DeepAR | -119.397598 | -83.850822 | 866.87 | 286 |
| 287 | DeepAR\63106_00191 | DeepAR | -127.219669 | -87.408332 | 1260.31 | 287 |
| 288 | DeepAR\63106_00192 | DeepAR | -171.492701 | -58.257357 | 1500.35 | 288 |
| 289 | DeepAR\63106_00193 | DeepAR | -95.179048 | -62.291258 | 657.28 | 289 |
| 290 | DeepAR\63106_00194 | DeepAR | -196.569060 | -75.487902 | 622.91 | 290 |
| 291 | DeepAR\63106_00195 | DeepAR | -146.427185 | -100.043344 | 489.22 | 291 |
| 292 | DeepAR\63106_00196 | DeepAR | -201.639305 | -73.372808 | 435.54 | 292 |
| 293 | DeepAR\63106_00197 | DeepAR | -198.648407 | -84.457921 | 612.93 | 293 |
| 294 | DeepAR\63106_00198 | DeepAR | -116.769972 | -73.763107 | 550.18 | 294 |
| 295 | DeepAR\63106_00199 | DeepAR | -208.138844 | -89.608200 | 1137.81 | 295 |
| 296 | DeepAR\63106_00200 | DeepAR | -217.650667 | -80.226982 | 420.09 | 296 |
| 297 | DeepAR\63106_00201 | DeepAR | -123.975570 | -85.053927 | 1025.50 | 297 |
| 298 | DeepAR\63106_00202 | DeepAR | -126.250106 | -94.936849 | 470.73 | 298 |
| 299 | DeepAR\63106_00203 | DeepAR | -96.187265 | -91.074492 | 388.55 | 299 |
| 300 | DeepAR\63106_00204 | DeepAR | -127.701515 | -79.427420 | 499.85 | 300 |
| 301 | DeepAR\63106_00205 | DeepAR | -168.304286 | -77.293160 | 421.52 | 301 |
| 302 | DeepAR\63106_00206 | DeepAR | -147.099135 | -80.749808 | 759.33 | 302 |
| 303 | DeepAR\63106_00207 | DeepAR | -149.823102 | -83.163717 | 732.73 | 303 |
| 304 | DeepAR\63106_00208 | DeepAR | -178.556841 | -99.276803 | 247.89 | 304 |
| 305 | DeepAR\63106_00209 | DeepAR | -150.155761 | -79.690581 | 637.69 | 305 |
| 306 | DeepAR\63106_00210 | DeepAR | -104.852849 | -68.524243 | 611.04 | 306 |
| 307 | DeepAR\63106_00211 | DeepAR | -114.360472 | -73.960385 | 623.53 | 307 |
| 308 | DeepAR\63106_00212 | DeepAR | -184.402816 | -72.522579 | 549.23 | 308 |
| 309 | DeepAR\63106_00213 | DeepAR | -139.043797 | -59.716574 | 513.20 | 309 |
| 310 | DeepAR\63106_00214 | DeepAR | -268.815224 | -73.707871 | 332.48 | 310 |
| 311 | DeepAR\63106_00215 | DeepAR | -175.223600 | -79.280342 | 373.48 | 311 |
| 312 | DeepAR\63106_00216 | DeepAR | -212.468744 | -74.823406 | 370.62 | 312 |
| 313 | WeightedEnsemble | WeightedEnsemble | -189.911396 | -43.853070 | 60.00 | 313 |

## 5. 해석 포인트

- 상위 성능권은 DeepAR 계열 변형 모델이 다수를 차지합니다.
- Tabular 계열(RecursiveTabular, DirectTabular)은 상대적으로 학습 시간이 짧고 안정적입니다.
- TemporalFusionTransformer 계열은 일부 조합에서 강한 검증 점수를 보이나 학습시간 변동이 큽니다.
- WeightedEnsemble은 단일 최상위보다 일관성을 높이는 역할로 포함됩니다.