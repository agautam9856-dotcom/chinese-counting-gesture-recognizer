"""Turns MediaPipe hand landmarks into a Chinese-style number (1-10)."""
import math
from collections import Counter, deque

THUMB_OUT_RATIO = 1.2
PINCH_RATIO = 0.40
HOOK_RATIO = 1.3

FINGERS = {
    "index": (5, 6, 8),
    "middle": (9, 10, 12),
    "ring": (13, 14, 16),
    "pinky": (17, 18, 20),
}

def _d(lm, a, b):
    return math.hypot(lm[a].x - lm[b].x, lm[a].y - lm[b].y)

def finger_states(lm):
    states = {}
    for name, (_, pip, tip) in FINGERS.items():
        states[name] = _d(lm, tip, 0) > _d(lm, pip, 0)
    states["thumb"] = _d(lm, 4, 17) > THUMB_OUT_RATIO * _d(lm, 2, 17)
    return states

def classify(lm):
    s = finger_states(lm)
    t, i, m, r, p = (s["thumb"], s["index"], s["middle"], s["ring"], s["pinky"])
    palm = _d(lm, 0, 9)

    if (not r and not p
            and _d(lm, 4, 8) < PINCH_RATIO * palm
            and _d(lm, 4, 12) < PINCH_RATIO * palm
            and _d(lm, 8, 0) > 1.1 * palm):
        return 7

    # 9 (Hook): Index finger is hooked (tip folded, but PIP lifted high).
    # To differentiate from 10 (Fist) where all PIPs are folded down,
    # we check if the index PIP (6) is significantly further from the wrist 
    # than the middle PIP (10).
    hooked = (not i) and _d(lm, 6, 0) > 1.15 * _d(lm, 10, 0)
    if hooked and not t and not m and not r and not p:
        return 9

    pattern = (t, i, m, r, p)
    table = {
        (False, True, False, False, False): 1,
        (False, True, True, False, False): 2,
        (False, True, True, True, False): 3,
        (False, True, True, True, True): 4,
        (True, True, True, True, True): 5,
        (True, False, False, False, True): 6,
        (True, True, False, False, False): 8,
        (False, False, False, False, False): 10,
    }
    return table.get(pattern)

class Smoother:
    def __init__(self, window=15, needed=8):
        self.buf = deque(maxlen=window)
        self.needed = needed
        self.current = None
        self.confidence = 0.0

    def update(self, value):
        self.buf.append(value)
        valid_vals = [v for v in self.buf if v is not None]
        if not valid_vals:
            self.confidence = 0.0
            if self.buf.count(None) > self.needed:
                self.current = None
            return self.current, self.confidence
            
        top, count = Counter(valid_vals).most_common(1)[0]
        self.confidence = (count / len(self.buf)) * 100
        
        if count >= self.needed:
            self.current = top
        elif value is None and self.buf.count(None) > self.needed:
            self.current = None
            
        return self.current, self.confidence
