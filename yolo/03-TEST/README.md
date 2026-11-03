# YOLO 웹캠 사물인식 2가지 프로그램

이 폴더에는 YOLO와 OpenCV를 사용하여 웹캠 영상을 실시간으로 분석하는 두 프로그램이 있습니다.
두 프로그램 모두 한 단계 위 폴더의 `yolo26n.pt` 모델 파일을 사용합니다.

## 준비 사항

- Windows
- Python 환경
- YOLO가 설치된 Conda 환경 또는 가상 환경
- 웹캠
- 아래 패키지:
  - `opencv-python`
  - `ultralytics`

YOLO 전용 환경을 사용하는 경우 다음 형식으로 실행할 수 있습니다.

```powershell
C:\Users\504\miniconda3\envs\yolo\python.exe 프로그램파일.py
```

## 1. 기본 GUI 프로그램

파일: [gui_webcam.py](./gui_webcam.py)

웹캠 화면을 실시간으로 분석하고, 인식된 객체에 네모 상자와 객체 이름을 표시하는 기본 프로그램입니다.

### 실행

```powershell
cd "C:\Users\504\3D Objects\yolo\03-TEST"
C:\Users\504\miniconda3\envs\yolo\python.exe gui_webcam.py
```

### 기능

- 0번 웹캠으로 영상 열기
- YOLO로 실시간 객체 인식
- 인식 결과를 `YOLO` 창에 표시
- `q` 키를 눌러 종료

### 종료 방법

실행 중인 창을 선택한 뒤 키보드의 `q`를 누릅니다.

## 2. 확장 GUI 프로그램

파일: [gui_webcam_v2.py](./gui_webcam_v2.py)

카메라 번호, 신뢰도, 강조할 객체를 직접 선택하고 결과를 사진으로 저장할 수 있는 확장 프로그램입니다.

### 실행

```powershell
cd "C:\Users\504\3D Objects\yolo\03-TEST"
C:\Users\504\miniconda3\envs\yolo\python.exe gui_webcam_v2.py
```

실행 후 순서대로 다음 값을 입력합니다.

1. 카메라 번호: 기본값 `0`
2. 신뢰도: 기본값 `0.25`, 권장 범위 `0.1~0.9`
3. 강조할 객체: 예) `person, cell phone, cup`

강조할 객체를 입력하지 않으면 모든 객체를 일반 이름표로 표시합니다.

### 기능

- 사용할 카메라 번호 선택
- 신뢰도 기준 설정
- 특정 객체 이름을 입력하여 노란 테두리로 강조
- 화면 상단에 총 감지 객체 수 표시
- 각 객체의 종류별 개수 계산
- `s` 키로 감지 결과와 요약이 포함된 스냅샷 저장
- `q` 키로 종료

### 키 조작

| 키 | 동작 |
|---|---|
| `s` | 스냅샷 저장 |
| `q` | 프로그램 종료 |

### 스냅샷 저장 위치

확장 프로그램은 스냅샷을 Windows 기본 다운로드 폴더에 저장합니다.

예:

```text
C:\Users\<사용자>\Downloads\yolo_snapshot_YYYYMMDD_HHMMSS.jpg
```