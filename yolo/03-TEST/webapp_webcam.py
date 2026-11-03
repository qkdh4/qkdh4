from pathlib import Path

import cv2
from flask import Flask, Response, render_template_string
from ultralytics import YOLO


app = Flask(__name__)

model_path = Path(__file__).resolve().parents[1] / "yolo26n.pt"
if not model_path.is_file():
    raise FileNotFoundError(f"YOLO 모델 파일을 찾을 수 없습니다: {model_path}")

model = YOLO(str(model_path))
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    raise RuntimeError("0번 웹캠을 열 수 없습니다.")


PAGE = """
<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>웹캠 사물인식</title>
    <style>
        body {
            margin: 0;
            padding: 24px;
            font-family: sans-serif;
            text-align: center;
            background: #111;
            color: #fff;
        }
        img {
            max-width: 90vw;
            height: auto;
            border-radius: 8px;
            background: #000;
        }
    </style>
</head>
<body>
    <h1>웹캠 사물인식</h1>
    <img src="/video" width="640" alt="웹캠 실시간 영상">
</body>
</html>
"""


def video_frames():
    while camera.isOpened():
        success, frame = camera.read()
        if not success:
            break

        results = model(frame)
        annotated = results[0].plot()
        encoded, jpeg = cv2.imencode(".jpg", annotated)
        if not encoded:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + jpeg.tobytes()
            + b"\r\n"
        )


@app.route("/")
def index():
    return render_template_string(PAGE)


@app.route("/video")
def video():
    return Response(
        video_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    try:
        app.run(host="127.0.0.1", port=5000)
    finally:
        camera.release()
