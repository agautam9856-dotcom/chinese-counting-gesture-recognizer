import cv2
import json
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from flask import Flask, render_template, Response, jsonify, send_from_directory
from gesture_logic import Smoother, classify
import time
import urllib.request
from pathlib import Path
import webbrowser
from threading import Timer

app = Flask(__name__)

MODEL_DIR = Path("assets/models")
MODEL_PATH = MODEL_DIR / "hand_landmarker.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

if not MODEL_PATH.exists():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

base_options = python.BaseOptions(model_asset_path=str(MODEL_PATH))
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1
)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
smoother = Smoother(window=15, needed=8)

global_state = {
    "number": None,
    "confidence": 0,
    "hand_detected": False,
    "stable": False
}

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]

def draw_landmarks(image, landmarks, w, h):
    points = []
    for lm in landmarks:
        x, y = int(lm.x * w), int(lm.y * h)
        points.append((x, y))
        cv2.circle(image, (x, y), 6, (0, 71, 255), -1)
        cv2.circle(image, (x, y), 3, (255, 255, 255), -1)
    
    for connection in HAND_CONNECTIONS:
        pt1 = points[connection[0]]
        pt2 = points[connection[1]]
        cv2.line(image, pt1, pt2, (255, 255, 255), 2)

def generate_frames():
    global global_state
    start_time = time.time()
    
    while True:
        success, frame = cap.read()
        if not success:
            break
            
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        timestamp_ms = int((time.time() - start_time) * 1000)
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        
        try:
            results = detector.detect_for_video(mp_image, timestamp_ms)
            
            raw = None
            if results.hand_landmarks:
                landmarks = results.hand_landmarks[0]
                raw = classify(landmarks)
                draw_landmarks(frame, landmarks, w, h)
                global_state["hand_detected"] = True
            else:
                global_state["hand_detected"] = False

            number, confidence = smoother.update(raw)
            global_state["number"] = number
            global_state["confidence"] = confidence
            global_state["stable"] = (number is not None and confidence > 50)
            
        except Exception as e:
            pass
            
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets/gestures/<path:filename>')
def serve_gesture(filename):
    return send_from_directory(Path(__file__).resolve().parent / 'demo' / 'gestures', filename)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/state')
def state():
    return jsonify(global_state)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5050/")

if __name__ == '__main__':
    # Validate development assets
    for i in range(1, 11):
        if not (Path(__file__).resolve().parent / 'demo' / 'gestures' / f'{i}.png').exists():
            print(f"WARNING: demo/gestures/{i}.png is missing.")
            
    Timer(1.5, open_browser).start()
    app.run(debug=False, port=5050, threaded=True)
