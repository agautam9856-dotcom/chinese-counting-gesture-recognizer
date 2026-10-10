"""Chinese Counting Gesture Recognizer."""
import sys
import time
import urllib.request
from pathlib import Path

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from gesture_logic import Smoother, classify, finger_states
from ui import UI
from audio import NumberSpeaker

BASE = Path(__file__).resolve().parent
FONT_DIR = BASE / "assets" / "fonts"
MODEL_DIR = BASE / "assets" / "models"
MODEL_PATH = MODEL_DIR / "hand_landmarker.task"
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

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
        cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
    
    for connection in HAND_CONNECTIONS:
        pt1 = points[connection[0]]
        pt2 = points[connection[1]]
        cv2.line(image, pt1, pt2, (0, 255, 0), 2)

def download_model_if_missing():
    if not MODEL_PATH.exists():
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        print("Downloading MediaPipe model, this might take a moment...")
        try:
            urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
            print("Model downloaded successfully.")
        except Exception as e:
            sys.exit(f"Failed to download model: {e}\nPlease check your internet connection or download it manually.")

def main():
    font_candidates = sorted(FONT_DIR.glob("*.ttf"))
    if not font_candidates:
        sys.exit("Chinese font not found. Put a Noto Sans SC .ttf file in assets/fonts/.")
    FONT_PATH = font_candidates[0]
    
    download_model_if_missing()

    try:
        base_options = python.BaseOptions(model_asset_path=str(MODEL_PATH))
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.7,
            min_hand_presence_confidence=0.7,
            min_tracking_confidence=0.7
        )
        detector = vision.HandLandmarker.create_from_options(options)
    except Exception as e:
        sys.exit(f"Failed to initialize MediaPipe HandLandmarker: {e}")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open the webcam. Please check your camera permissions.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    WINDOW = "Chinese Counting Gestures"
    cv2.namedWindow(WINDOW, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW, 1280, 720)

    smoother = Smoother(window=15, needed=8)
    show_skeleton = True
    debug = False
    audio_enabled = True
    last_number = None
    ui_mgr = None

    try:
        speaker = NumberSpeaker(BASE / "assets" / "audio")
        speaker.prepare()
    except Exception as exc:
        print(f"Audio disabled: {exc}")
        speaker = None

    prev_time = 0
    start_time = time.time()

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
                
            timestamp_ms = int((time.time() - start_time) * 1000)

            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time else 0
            prev_time = curr_time

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            if ui_mgr is None:
                ui_mgr = UI(FONT_PATH, w, h)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            
            try:
                results = detector.detect_for_video(mp_image, timestamp_ms)
            except Exception as e:
                print(f"Error processing frame: {e}")
                continue

            raw = None
            debug_info = []
            state_text = "Hand detected ✓" if results.hand_landmarks else "Show your hand to the camera"

            if results.hand_landmarks:
                landmarks = results.hand_landmarks[0]
                handedness = results.handedness[0][0].category_name if results.handedness else "Unknown"
                
                raw = classify(landmarks)
                
                if show_skeleton:
                    draw_landmarks(frame, landmarks, w, h)

                if debug:
                    states = finger_states(landmarks)
                    debug_info.append(f"FPS: {int(fps)}")
                    debug_info.append(f"Hand: {handedness}")
                    debug_info.append(f"Raw: {raw}")
                    for name, val in states.items():
                        debug_info.append(f"{name}: {val}")

            number, confidence = smoother.update(raw)
            
            if number is not None:
                state_text += "     Gesture stable ✓"
                if audio_enabled and speaker:
                    state_text += "     Audio ready 🔊"
                    
            frame = ui_mgr.render_overlay(frame, state_text, number, confidence, debug_info if debug else None)

            if audio_enabled and number != last_number:
                if number is not None and speaker is not None:
                    speaker.say(number)
                last_number = number

            cv2.imshow(WINDOW, frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
            elif key == ord("l"):
                show_skeleton = not show_skeleton
            elif key == ord("d"):
                debug = not debug
            elif key == ord("a"):
                audio_enabled = not audio_enabled

    finally:
        detector.close()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
