# 날짜와 시간으로 스냅샷 이름을 만들기 위한 도구를 불러온다
from datetime import datetime
# 다운로드 폴더 경로를 쉽게 찾기 위한 도구를 불러온다
from pathlib import Path
# 카메라 영상과 화면 표시를 위한 OpenCV를 불러온다
import cv2
# 사물인식 AI인 YOLO를 불러온다
from ultralytics import YOLO

# 스크립트 위치를 기준으로 위쪽 폴더에서 모델 파일을 찾는다
model_path = Path(__file__).resolve().parents[1] / "yolo26n.pt"
# 사용할 YOLO 모델을 읽는다
model = YOLO(str(model_path))

# 시작할 때 사용할 카메라 번호를 입력받는다
camera_number = input("카메라 번호를 입력하세요 [기본값 0]: ") or "0"
# 입력받은 카메라 번호를 숫자로 바꾼다
camera_number = int(camera_number)
# 시작할 때 사용할 신뢰도 값을 입력받는다
confidence_text = input("신뢰도(0.1~0.9)를 입력하세요 [기본값 0.25]: ") or "0.25"
# 입력받은 신뢰도 값을 소수로 바꾼다
confidence = float(confidence_text)
# 강조할 클래스를 쉼표로 입력받는다
highlight_text = input("강조할 클래스(예: person, cell phone, cup)를 입력하세요 [강조 없음: Enter]: ")
# 입력한 클래스를 쉼표 기준으로 나누어 목록을 만든다
highlight_classes = [name.strip() for name in highlight_text.split(",") if name.strip()]

# 기본 다운로드 폴더를 스냅샷 저장 위치로 만든다
snapshot_folder = Path.home() / "Downloads"
# 다운로드 폴더가 없으면 새로 만든다
snapshot_folder.mkdir(parents=True, exist_ok=True)
# 선택한 카메라 번호로 웹캠을 연다
camera = cv2.VideoCapture(camera_number)

# 카메라가 열리지 않았으면 상태를 표시하고 종료한다
if not camera.isOpened():
    print(f"웹캠 상태: {camera_number}번 카메라를 열 수 없습니다.")
    camera.release()
    raise SystemExit

# 카메라 연결 상태를 사용자에게 표시한다
print("웹캠 상태: 연결됨")
print("q: 종료, s: 스냅샷 저장")

# 카메라가 정상적으로 열려 있는 동안 계속 반복한다
while camera.isOpened():
    # 카메라에서 영상 한 장을 읽는다
    success, frame = camera.read()
    # 영상 읽기에 실패하면 상태를 표시하고 반복을 멈춘다
    if not success:
        print("웹캠 상태: 영상 읽기에 실패했습니다.")
        break
    # 설정한 신뢰도 이상인 객체만 인식한다
    results = model(frame, conf=confidence)
    # YOLO 결과에서 첫 번째 화면과 객체 상자를 가져온다
    result = results[0]
    # 인식 결과를 네모 상자와 이름표가 있는 화면으로 만든다
    annotated = result.plot()

    # 현재 화면에서 감지된 클래스별 개수를 센다
    object_counts = {}
    # 감지된 각 객체의 클래스 번호를 차례로 확인한다
    for class_id in result.boxes.cls:
        # 클래스 번호에 해당하는 영어 이름을 가져온다
        class_name = result.names[int(class_id)]
        # 같은 이름이 있으면 개수를 하나 늘린다
        object_counts[class_name] = object_counts.get(class_name, 0) + 1
    # 화면 위쪽에 객체 수를 표시한다
    cv2.rectangle(annotated, (10, 10), (220, 55), (0, 0, 0), -1)
    cv2.putText(annotated, f"Objects: {len(result.boxes)}", (20, 43), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # 특정 클래스를 강조하도록 설정한 경우
    if highlight_classes:
        # 감지된 모든 객체 상자를 확인한다
        for box, class_id in zip(result.boxes.xyxy.cpu().numpy(), result.boxes.cls.cpu().numpy()):
            # 강조할 클래스인지 확인한다
            if result.names[int(class_id)] in highlight_classes:
                # 강조할 객체를 두꺼운 노란색 테두리로 다시 그린다
                x1, y1, x2, y2 = map(int, box)
                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 255), 4)

    # YOLO라는 창에 웹캠 결과를 표시한다
    cv2.imshow("YOLO", annotated)
    # 키 입력을 확인한다
    key = cv2.waitKey(1) & 0xFF
    # s 키를 누르면 스냅샷을 저장한다
    if key == ord("s"):
        # 현재 시간으로 파일 이름을 만든다
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = snapshot_folder / f"yolo_snapshot_{timestamp}.jpg"
        # 카메라 화면보다 오른쪽에 요약을 위한 공간을 넓힌다
        camera_height, camera_width = annotated.shape[:2]
        summary_width = 320
        # 카메라 화면과 오른쪽 요약 공간을 가진 검은색 스냅샷을 만든다
        snapshot = cv2.copyMakeBorder(annotated, 0, 0, 0, summary_width, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        # 요약 영역의 시작 위치를 설정한다
        summary_x = camera_width + 20
        summary_y = 45
        cv2.putText(snapshot, "Detection summary:", (summary_x, summary_y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
        # 감지된 클래스와 개수를 오른쪽 영역에 한 줄씩 표시한다
        for class_name, count in object_counts.items():
            summary_y += 35
            cv2.putText(snapshot, f"- {class_name}: {count}", (summary_x, summary_y), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        # 감지된 객체가 없으면 오른쪽 영역에 없다고 표시한다
        if not object_counts:
            cv2.putText(snapshot, "- no objects", (summary_x, summary_y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        # 카메라 화면과 요약이 모두 포함된 큰 사진을 저장한다
        cv2.imwrite(str(snapshot_path), snapshot)
        print(f"스냅샷 저장됨: {snapshot_path}")
    # q 키를 누르면 반복을 멈춘다
    if key == ord("q"):
        break

# 사용이 끝난 카메라를 닫는다
camera.release()
# 열려 있는 모든 OpenCV 창을 닫는다
cv2.destroyAllWindows()
# 종료 상태를 사용자에게 표시한다
print("웹캠 상태: 종료됨")
