# Chinese Counting Gesture Recognizer

Real-time Mandarin hand gesture recognition using the modern **MediaPipe Tasks Vision API** and OpenCV. Learn how to count from 1 to 10 in Chinese using traditional hand gestures!

## Features

- **Real-time Gesture Recognition**: Uses the latest `mediapipe.tasks.vision.HandLandmarker` API to track hand landmarks.
- **Robust Smoothing**: Temporal smoothing and stability confidence to prevent flickering.
- **Mandarin Audio**: Automatically pronounces the detected number in Mandarin (uses macOS native `afplay`).
- **Modern UI**: Polished, responsive user interface with gesture references and visual feedback.
- **Educational**: Displays Chinese character and Pinyin for each number.

## Demo

*(Add demo.gif here)*

## Architecture

The system uses Google's latest MediaPipe Tasks Vision API to extract 21 3D hand landmarks. A custom rule-based classification algorithm uses normalized distance ratios from the wrist to the fingertips to determine finger extension and flexion. 

The application architecture:
- `main.py`: Entry point handling webcam loop, model loading, and UI compositing.
- `gesture_logic.py`: Mathematics and heuristic mapping of landmarks to numbers.
- `ui.py`: Pillow-based rendering engine to flawlessly display custom Chinese typography over OpenCV streams.
- `audio.py`: Asynchronous text-to-speech implementation using `gTTS` and macOS `afplay`.

## Installation

### Prerequisites

- macOS (Audio playback leverages built-in `afplay`)
- Supported Python Version: **Python 3.10 - 3.14** 
- Webcam

### Setup

1. Clone the repository or download the source code.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The `hand_landmarker.task` model will be automatically downloaded into `assets/models/` when you run the app for the first time).*

## Usage

Run the application:

```bash
python main.py
```

*Note for macOS users: You must grant Terminal/iTerm access to your Camera in System Settings > Privacy & Security > Camera.*

### Controls

- **Q**: Quit application
- **L**: Toggle hand skeleton visualization
- **D**: Toggle debug mode
- **A**: Toggle audio pronunciation

## Known Limitations

- macOS Specific: Audio is built on `afplay`. Running this on Windows or Linux will require modifying `audio.py` to use a cross-platform player (like `playsound`).
- Lighting: Extreme lighting conditions or motion blur will reduce MediaPipe's underlying hand detection accuracy.

## License

MIT License
