# MIWS-Project
MediaPipe Interactive Web Suite Project For AI Lab
# 🎮 Gesture-Based Interactive System (Snake Game, Quiz & Air Canvas)

## 📌 Overview

This project is a **gesture-controlled interactive system** built using **Python, OpenCV, and Pygame**, integrated with a **Flask web interface**.

Users can control applications using **hand gestures** detected via webcam. The system includes:

* 🎨 Air Canvas (virtual drawing using hand tracking)
* 🐍 Snake Game (gesture-controlled)
* 🧠 Quiz Game (gesture-based selection)

---

## 🚀 Features

* ✋ Real-time hand gesture recognition using OpenCV
* 🧠 AI-based interaction (via MediaPipe hand tracking)
* 🎮 Multiple applications in one platform
* 🌐 Web dashboard using Flask
* 🔄 Subprocess-based app launching
* 📷 Webcam integration

---

## 🛠️ Technologies & AI Concepts Used

### 💻 Technologies

* Python 3.x
* OpenCV (Computer Vision processing)
* MediaPipe (Hand Tracking framework)
* Pygame (Game development)
* Flask (Web framework)
* Threading & Subprocess (Parallel execution)

---

### 🤖 AI & Computer Vision Concepts

This project applies multiple **Artificial Intelligence and Computer Vision concepts**:

#### 🖐️ Hand Tracking & Detection

* Real-time hand landmark detection using **MediaPipe**
* Extraction of 21 key points (fingers, joints, palm)
* Tracking hand movement across frames

#### 🧠 Gesture Recognition

* Rule-based gesture classification using landmark positions
* Mapping finger states → system commands
* Temporal consistency using **gesture progress tracking**

#### 👁️ Computer Vision

* Frame capturing via webcam (OpenCV)
* Image processing and feature extraction
* Real-time video stream analysis

#### 📊 Pattern Recognition

* Recognizing finger patterns (0-4 fingers)
* Translating patterns into game actions
* Decision-making based on gesture input

#### ⏱️ Real-Time Processing

* Continuous frame processing loop
* Low-latency interaction system
* Synchronization between gesture detection and game logic

#### 🔄 Human-Computer Interaction (HCI)

* Gesture-based input instead of keyboard/mouse
* Natural user interface (NUI)
* Interactive feedback system (hover, selection, confirmation)

---

### 🎯 AI Application in This Project

* Replacing traditional input devices with **gesture-based control**
* Creating an **intelligent interaction system**
* Enabling **touchless gaming and drawing environment**


## 📂 Project Structure

```
project/
│
├── app.py                  # Flask backend
├── AI_VirtualPainter.py    # Air Canvas
├── snakeGameUI.py          # Snake Game UI
├── snakeGameLogic.py       # Snake Game Logic
├── quizGameUI.py           # Quiz Game UI
├── quizGameLogic.py        # Quiz Logic
├── HandTrackingModule.py   # Gesture Detection
├── requirements.txt
|
├── images/
│   └── 1.png
│   └── 2.png
│   └── 3.png
│   └── 4.png
|
├── templates/
│   └── index.html          # Frontend UI
├── static/                 
│   └── css/
|       └── canvas.css
|       └── index.css
|   └── scripts/
|       └── index.jss   
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### If requirements.txt not available:

```bash
pip install opencv-python mediapipe pygame flask
```

---

## ▶️ How to Run

### Run the Flask server:

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000/
```

---

## 🕹️ How to Use

### 🎯 Menu Controls (Gesture-Based)

| Gesture      | Action            |
| ------------ | ----------------- |
| ☝️ 1 Finger  | Select / Start    |
| ✌️ 2 Fingers | Quit / Exit       |
| ✊ Hold gesture | Confirm selection |

---

### 🐍 Snake Game

* Control snake using hand gestures:
  * ☝ Up / ✊ Down / 👈 Left / 👉 Right
* No walls → snake wraps around screen
* Eat food to increase score
* Avoid hitting yourself

---

### 🧠 Quiz Game

* Questions appear with 4 options
* Use fingers (1–4) to select options
* Hold gesture to confirm
* Score shown at the end

---

### 🎨 Air Canvas

* Draw in air using your index finger
* Use gestures to:

  * 👆 Draw
  * ✌️ Change color
  * ✌️ Erase

---

## ⚠️ Important Notes

* Ensure your **webcam is working**
* Run in a **well-lit environment** for better gesture detection
* Close previous apps before launching new ones
* Windows users may see app windows open in background (OS limitation)

---

## 🐞 Troubleshooting

### Camera not opening

* Check if another app is using the webcam

### Gesture not working

* Improve lighting
* Keep hand clearly visible

### App not launching

* Ensure correct Python path
* Check file names

---

## 📈 Future Improvements

* Browser-based game rendering (no popups)
* Improved gesture accuracy
* UI/UX enhancements
* Multiplayer support
* Sound effects & animations

---

## 👨‍💻 Author

**Adnan Hatim**
FAST University – AI Lab Project

**Murtaza Hunaid**
FAST University – AI Lab Project

---

## 📜 License

This project is for educational purposes.

```
```
