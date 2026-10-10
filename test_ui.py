import cv2
import numpy as np
from ui import UI
import config
from pathlib import Path

BASE = Path(__file__).resolve().parent
FONT_DIR = BASE / "assets" / "fonts"
font_candidates = sorted(FONT_DIR.glob("*.ttf"))
if font_candidates:
    ui = UI(font_candidates[0], 1280, 720)
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    frame = ui.render_overlay(frame, "Hand detected", 5, 85.5, ["FPS: 30"])
    cv2.imwrite("chinese-counting-ges./test_ui_output.png", frame)
    print("UI rendered successfully")
else:
    print("Font not found")
