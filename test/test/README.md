# 코스피200 상대강도 · 영향력 시계열 분석 웹앱

코스피200(KODEX 200, 069500)을 기준으로 코스피 시가총액 상위 200종목(총 201종목)의
일봉(OHLCV)을 FinanceDataReader로 수집하고, 상대적 강세/약세와 지수 영향력을 분석하는 웹앱입니다.

## 분석 방법
| 항목 | 정의 |
|---|---|
| 당일 등락률 | `종가 / 전일종가 - 1` |
| 초과수익률 | 종목 등락률 − KODEX200 등락률 |
| 정규화 점수 | 5일 평균 초과수익률 ÷ 20일 초과수익률 표준편차 (z-score 성격) |
| 그룹화 | `≥ 0.5` 상향 / `≤ -0.5` 하향 / 그 외 횡보 |
| 지수 기여도(bp) | 시총비중 × 종목수익률 × 10000 |
| 영향력 점수 | `(0.7×시총비중 + 0.3×거래대금비중) × |초과수익률|` 을 0~100 정규화 |
| 그룹 전이 | 5거래일 전 그룹 → 현재 그룹 (예: `상향->하향`), 전이 행렬·변화 종목 목록 제공 |

## 실행 (VSCode)
```bash
cd py311/test
python -m venv .venv
# Windows: .venv\Scripts\activate / mac·Linux: source .venv/bin/activate
pip install -r requirements.txt
python test/test/run_pipeline.py   # 1) 수집+분석 (data/ 에 CSV 저장)
python app.py            # 2) 서버 구동 -> http://localhost:8000
```
> FinanceDataReader/네트워크가 없으면 샘플 데이터로 자동 대체되어 화면이 먼저 동작합니다(상단 경고 표시). 실데이터 환경에서는 자동으로 교체됩니다.

## GitHub와 연결해 https 웹앱으로 보기 (GitHub Pages)
파일 안에 데이터를 내장한 정적 페이지라 서버 없이 https로 볼 수 있습니다.
```bash
python export_static.py  # docs/index.html 생성
```
1. 이 `py311` 폴더를 GitHub 리포지터리에 push
2. GitHub 리포 → **Settings → Pages → Source: Deploy from a branch → Branch: main, 폴더: /(root)** 가 아닌 경우,
   `test/docs`를 배포하려면 리포 루트에 docs를 두거나 Actions 배포를 사용하세요. 가장 간단한 방법: `test/docs/index.html`을 리포 루트 `docs/`로 복사해 push하고 Pages 폴더를 `/docs`로 지정
3. 접속: `https://<GitHub아이디>.github.io/<리포이름>/`
4. 자동 갱신: `.github/workflows/update-data.yml`이 평일 장마감 후(17:30 KST) 수집→정적페이지 재생성→commit 합니다.

### 대안: 상시 서버 (Render/Railway 등)
`python app.py`를 실행 커맨드로 지정하고 포트 환경변수 `PORT`를 쓰면 됩니다(Flask 서버가 `PORT`를 읽음).

## 구조
```
test/
├─ app.py              # Flask 웹서버 (API + 대시보드)
├─ data_collector.py   # fdr 수집 (069500 + 시총상위 200), 샘플 폴백
├─ analysis.py         # 정규화·그룹화·영향력·전이 분석
├─ run_pipeline.py     # 수집→분석 일괄 실행
├─ export_static.py    # GitHub Pages용 docs/index.html 생성
├─ config.py           # 임계값/가중치/기간 설정
├─ templates/index.html
├─ tests/test_analysis.py
└─ data/               # ohlcv.csv, latest_analysis.csv, summary.json
```

## 테스트
```bash
cd tests && python test_analysis.py
```
