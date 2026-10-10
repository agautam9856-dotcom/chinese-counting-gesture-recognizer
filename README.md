# 🖐️ Chinese Counting Gesture Recognizer

**Learn Chinese numbers through real-time hand gestures.**

Chinese Counting Gesture Recognizer is a Python-based computer vision project designed to recognize hand gestures representing Chinese numbers from **1 to 10** using a webcam. It combines hand tracking, gesture classification, and Chinese pronunciation to create an interactive language-learning experience.

The project explores how computer vision can make language learning more visual, interactive, and accessible.

## ✨ Features

- **Real-Time Hand Tracking** — Detect hand landmarks through a webcam using MediaPipe.
- **Gesture Recognition** — Classify supported hand gestures representing Chinese numbers from 1 to 10.
- **Chinese Characters** — Display the corresponding Chinese number.
- **Pinyin Pronunciation** — Show the romanized pronunciation of each number.
- **Audio Feedback** — Play Mandarin pronunciation using text-to-speech.
- **Gesture Reference Guide** — Provide visual references for learning the hand poses.
- **Visual Feedback** — Display the recognition result and relevant hand-tracking information.
- **Python-Based Architecture** — Separate gesture recognition, interface, and audio functionality into maintainable modules.

*Feature availability depends on the current implementation and successful local testing.*

## 🔢 Chinese Numbers

| Number | Chinese | Pinyin |
|---:|:---:|---|
| 1 | 一 | yī |
| 2 | 二 | èr |
| 3 | 三 | sān |
| 4 | 四 | sì |
| 5 | 五 | wǔ |
| 6 | 六 | liù |
| 7 | 七 | qī |
| 8 | 八 | bā |
| 9 | 九 | jiǔ |
| 10 | 十 | shí |

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| OpenCV | Webcam access and image processing |
| MediaPipe | Hand landmark detection |
| Pillow | Image processing and UI assets |
| gTTS | Mandarin text-to-speech audio |
| Git & GitHub | Version control and project hosting |

## ⚙️ How It Works

The application follows a computer vision pipeline:

```text
Webcam Input
     ↓
Frame Processing
     ↓
Hand Landmark Detection
     ↓
Hand Gesture Classification
     ↓
Recognition Result
     ↓
Chinese Character + Pinyin
     ↓
Audio Feedback
```

### 1. Webcam Input
The application captures frames from the webcam.

### 2. Hand Landmark Detection
MediaPipe detects key points on the hand. These landmarks provide information about finger positions and hand geometry.

### 3. Gesture Classification
The recognition logic evaluates hand landmarks and finger positions to determine which supported number gesture is being shown.

### 4. Result Display
The application displays the recognized Chinese number and its Pinyin pronunciation.

### 5. Audio Feedback
The audio module can provide spoken pronunciation when the relevant functionality is available.

## 📁 Project Structure

```text
chinese-counting-gesture-recognizer/
│
├── main.py
├── gesture_logic.py
├── ui.py
├── audio.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── assets/
│   ├── fonts/
│   └── audio/
│
└── demo/
    └── gestures/
        ├── 1.png
        ├── 2.png
        ├── 3.png
        ├── 4.png
        ├── 5.png
        ├── 6.png
        ├── 7.png
        ├── 8.png
        ├── 9.png
        └── 10.png
```

*The structure above reflects the intended project organization. Adjust filenames and folders if your current version differs.*

## 🚀 Getting Started

### Prerequisites

Install the following before running the application:

- Python version compatible with your installed MediaPipe release
- A working webcam
- Git (optional, for cloning the repository)

**Important:** Use a Python version supported by your exact MediaPipe version. If installation or startup fails, check MediaPipe's compatibility requirements before changing the application code.

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/chinese-counting-gesture-recognizer.git
```

Enter the project directory:

```bash
cd chinese-counting-gesture-recognizer
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a Virtual Environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Application

If the application entry point is `main.py`:

```bash
python main.py
```

If your current version uses `app.py`, run:

```bash
python app.py
```

Use the entry point that actually exists in your repository.

### 5. Try the Gestures

1. Allow the application to access your webcam.
2. Position your hand clearly in front of the camera.
3. Show one of the supported Chinese number gestures.
4. Check the displayed recognition result.
5. Try different numbers and hand positions.
6. Test the pronunciation and reference guide if implemented.

## 📸 Screenshots and Demo

Screenshots and a demonstration video should be added after validating the application locally.

Suggested repository layout:

```text
demo/
├── screenshots/
│   ├── main-screen.png
│   ├── gesture-recognition.png
│   └── gesture-guide.png
└── gestures/
    ├── 1.png
    ├── 2.png
    └── ...
```

Once you have captured a real screenshot, display it here:

```markdown
![Main Application](demo/screenshots/main-screen.png)
```

You can also add a short GIF demonstrating real-time gesture recognition.

**Only include screenshots and GIFs of the actual working application.**

## 🧠 Challenges and Learning

This project provides practical experience with:

- Real-time computer vision
- Hand landmark detection
- Geometric gesture classification
- Image coordinate systems
- Webcam integration
- Recognition stability and smoothing
- Text-to-speech integration
- Modular Python development
- Debugging hardware-dependent software

One important engineering challenge is distinguishing gestures that have similar finger configurations. Camera angle, lighting, hand orientation, and landmark accuracy can affect recognition.

## 🔮 Future Improvements

Potential improvements include:

- A polished interactive gesture-learning guide
- More reliable recognition across different hand positions
- A practice mode with instant feedback
- Improved landmark visualization
- More detailed pronunciation controls
- Recognition performance testing
- Support for additional languages and gesture systems
- Recognition accuracy evaluation using a documented test dataset
- A demonstration video and complete usage guide

## 🤝 Contributing

Suggestions, bug reports, and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Submit a pull request describing your improvements.

## 📄 License

This project is distributed under the MIT License if the repository includes the corresponding `LICENSE` file. See that file for the applicable terms.

## 👨‍💻 Author

**Aman Gautam**

B.Tech Computer Engineering student interested in Python, computer vision, AI, and software development.

- GitHub: [agautam9856-dotcom](https://github.com/agautam9856-dotcom)

---

*Built as a hands-on exploration of computer vision and interactive language learning.*
