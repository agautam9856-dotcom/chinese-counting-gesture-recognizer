"""Mandarin audio generation and playback for numbers 1-10."""

import os
import subprocess
from pathlib import Path
from gtts import gTTS

CHARS = {
    1: "一", 2: "二", 3: "三", 4: "四", 5: "五",
    6: "六", 7: "七", 8: "八", 9: "九", 10: "十",
}

class NumberSpeaker:
    """Generate/cache Mandarin audio and play it using native macOS tools."""

    def __init__(self, audio_dir):
        self.dir = Path(audio_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.sounds = {}
        self._current_process = None

    def prepare(self):
        for number, character in CHARS.items():
            path = self.dir / f"{number}.mp3"

            if not path.exists():
                try:
                    print(f"Generating Mandarin audio for {number} ({character})...")
                    gTTS(text=character, lang="zh-CN").save(str(path))
                except Exception as exc:
                    print(f"Audio generation skipped for {number}: {exc}")
                    continue
            
            if path.exists():
                self.sounds[number] = str(path)

    def say(self, number):
        path = self.sounds.get(number)
        if path is None:
            return

        # Stop previous audio if still playing
        if self._current_process and self._current_process.poll() is None:
            self._current_process.kill()

        try:
            self._current_process = subprocess.Popen(["afplay", path])
        except Exception as exc:
            print(f"Could not play audio for {number}: {exc}")
