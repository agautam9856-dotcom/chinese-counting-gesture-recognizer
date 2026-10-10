import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

NUMBERS = {
    1: ("一", "yī"),
    2: ("二", "èr"),
    3: ("三", "sān"),
    4: ("四", "sì"),
    5: ("五", "wǔ"),
    6: ("六", "liù"),
    7: ("七", "qī"),
    8: ("八", "bā"),
    9: ("九", "jiǔ"),
    10: ("十", "shí"),
}

TEXT_DARK = (30, 30, 30)
ACCENT = (200, 30, 30)
MUTED = (110, 110, 110)

class UI:
    def __init__(self, font_path, frame_width, frame_height):
        self.w = frame_width
        self.h = frame_height
        self.f_title = ImageFont.truetype(str(font_path), 28)
        self.f_sub = ImageFont.truetype(str(font_path), 16)
        self.f_status = ImageFont.truetype(str(font_path), 18)
        
        self.f_num_large = ImageFont.truetype(str(font_path), 60)
        self.f_char_large = ImageFont.truetype(str(font_path), 100)
        self.f_pin_large = ImageFont.truetype(str(font_path), 40)
        self.f_conf = ImageFont.truetype(str(font_path), 20)
        
        self.f_ref_small = ImageFont.truetype(str(font_path), 20)
        self.f_ref_title = ImageFont.truetype(str(font_path), 24)

    def draw_rounded_rect(self, img, pt1, pt2, color, thickness, r):
        x1, y1 = pt1
        x2, y2 = pt2
        cv2.line(img, (x1 + r, y1), (x2 - r, y1), color, thickness)
        cv2.line(img, (x1 + r, y2), (x2 - r, y2), color, thickness)
        cv2.line(img, (x1, y1 + r), (x1, y2 - r), color, thickness)
        cv2.line(img, (x2, y1 + r), (x2, y2 - r), color, thickness)
        cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
        cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
        cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)
        cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    def render_overlay(self, frame, state, number, confidence, debug_info=None):
        overlay = frame.copy()
        
        # Top bar
        cv2.rectangle(overlay, (0, 0), (self.w, 80), (30, 30, 30), -1)
        
        # Bottom status bar
        cv2.rectangle(overlay, (0, self.h - 40), (self.w, self.h), (40, 40, 40), -1)
        
        # Detection Card
        card_w, card_h = 300, 450
        card_x = self.w - card_w - 30
        card_y = 110
        cv2.rectangle(overlay, (card_x, card_y), (card_x + card_w, card_y + card_h), (255, 255, 255), -1)
        self.draw_rounded_rect(overlay, (card_x, card_y), (card_x + card_w, card_y + card_h), (200, 200, 200), 2, 15)

        # Gesture Reference Panel
        ref_w, ref_h = 250, 450
        ref_x = 30
        ref_y = 110
        cv2.rectangle(overlay, (ref_x, ref_y), (ref_x + ref_w, ref_y + ref_h), (240, 240, 240), -1)
        cv2.rectangle(overlay, (ref_x, ref_y), (ref_x + ref_w, ref_y + ref_h), (200, 200, 200), 2)
        
        # Apply alpha
        cv2.addWeighted(overlay, 0.9, frame, 0.1, 0, frame)

        # Draw Text using PIL
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        # Top Bar Text
        draw.text((20, 10), "Chinese Counting", font=self.f_title, fill=(255, 255, 255))
        draw.text((20, 45), "Real-time Mandarin Hand Gesture Recognition", font=self.f_sub, fill=(180, 180, 180))
        draw.text((self.w - 200, 25), "● CAMERA ACTIVE", font=self.f_status, fill=(50, 255, 50))

        # Bottom status text
        draw.text((20, self.h - 30), state, font=self.f_status, fill=(200, 200, 200))

        # Reference Panel Text
        draw.text((ref_x + 20, ref_y + 15), "Gesture Reference", font=self.f_ref_title, fill=(50, 50, 50))
        for i in range(1, 11):
            y_offset = ref_y + 50 + (i-1)*38
            char, pin = NUMBERS[i]
            draw.text((ref_x + 30, y_offset), f"{i:2d}   {char}   {pin}", font=self.f_ref_small, fill=(50, 50, 50))

        # Detection Card Text
        if number is not None:
            draw.text((card_x + card_w//2, card_y + 40), "DETECTED NUMBER", font=self.f_status, fill=(100, 100, 100), anchor="mm")
            
            draw.text((card_x + card_w//2, card_y + 110), str(number), font=self.f_num_large, fill=(50, 50, 50), anchor="mm")
            
            char, pinyin = NUMBERS[number]
            draw.text((card_x + card_w//2, card_y + 220), char, font=self.f_char_large, fill=(200, 30, 30), anchor="mm")
            draw.text((card_x + card_w//2, card_y + 320), pinyin, font=self.f_pin_large, fill=(50, 50, 50), anchor="mm")
            
            # Confidence bar
            conf_y = card_y + 380
            draw.text((card_x + card_w//2, conf_y), "Confidence", font=self.f_conf, fill=(100, 100, 100), anchor="mm")
            
            bar_w = 200
            bar_x = card_x + (card_w - bar_w)//2
            bar_y = conf_y + 20
            draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + 10], fill=(220, 220, 220))
            draw.rectangle([bar_x, bar_y, bar_x + (bar_w * confidence / 100), bar_y + 10], fill=(50, 200, 50))
            draw.text((bar_x + bar_w + 10, bar_y - 5), f"{int(confidence)}%", font=self.f_conf, fill=(50, 50, 50))
        else:
            draw.text((card_x + card_w//2, card_y + 200), "SHOW YOUR HAND", font=self.f_title, fill=(50, 50, 50), anchor="mm")
            draw.text((card_x + card_w//2, card_y + 240), "Place your hand\ninside the camera view", font=self.f_sub, fill=(100, 100, 100), anchor="mm", align="center")

        # Debug Info
        if debug_info:
            y = 120
            for line in debug_info:
                draw.text((self.w // 2 - 50, y), line, font=self.f_status, fill=(255, 0, 255))
                y += 25

        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

