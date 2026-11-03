# OpenCV로 카메라 영상과 창을 다룰 수 있게 도구를 불러온다
import cv2
# ultralytics에서 사물인식 AI인 YOLO를 불러온다
from ultralytics import YOLO

# 사용할 YOLO 모델 파일을 읽어 AI를 준비한다
model = YOLO("yolo26n.pt")
# 노트북의 기본 웹캠인 0번 카메라를 연다
camera = cv2.VideoCapture(0)

# 카메라가 정상적으로 열려 있는 동안 계속 반복한다
while camera.isOpened():
    # 카메라에서 영상 한 장을 읽는다
    success, frame = camera.read()
    # 영상 읽기에 실패하면 반복을 멈춘다
    if not success:
        break
    # 읽은 영상으로 사물을 인식한다
    results = model(frame)
    # 인식 결과를 네모 상자와 함께 영상 위에 그린다
    annotated = results[0].plot()
    # 결과 화면을 YOLO라는 창에 표시한다
    cv2.imshow("YOLO", annotated)
    # q 키를 누르면 반복을 멈춘다
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 사용이 끝난 카메라를 닫는다
camera.release()
# 열려 있는 모든 OpenCV 창을 닫는다
cv2.destroyAllWindows()

# 종료버튼 : 창을 누른 뒤 q 키
