# Hand Gesture Based Screen Brightness Control using OpenCV and MediaPipe

## Project Overview

Hand Gesture Based Screen Brightness Control is a Computer Vision project that allows users to control their system screen brightness using hand gestures.

The system uses a webcam to detect hand landmarks in real-time using **MediaPipe**, calculates the distance between fingers, and maps the gesture movement to screen brightness levels.

This project provides a touch-free method for controlling screen brightness using Artificial Intelligence and Computer Vision techniques.

---

## Features

- Real-time hand detection using webcam
- Finger landmark tracking
- Gesture-based brightness adjustment
- Automatic brightness control based on finger distance
- Streamlit-based user interface
- Live camera feed visualization
- Cross-platform Python implementation

---

## Technologies Used

### Programming Language
- Python

### Computer Vision
- OpenCV
- MediaPipe

### Data Processing
- NumPy

### User Interface
- Streamlit

### Other Tools
- Git & GitHub
- Webcam

---

## Project Structure

```
Hand-Gesture-Brightness-Control
│
├── assets/
│
├── models/
│
├── output/
│
├── utils/
│   ├── brightness_controller.py
│   └── hand_detector.py
│
├── app.py
├── streamlit_app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## How It Works

1. The webcam captures live video frames.
2. OpenCV processes the video input.
3. MediaPipe detects hand landmarks.
4. The distance between selected finger points is calculated.
5. The distance value is converted into a brightness percentage.
6. The system updates the screen brightness automatically.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Hand-Gesture-Brightness-Control.git
```

### 2. Navigate to Project Folder

```bash
cd Hand-Gesture-Brightness-Control
```

### 3. Create Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

---

### 4. Install Required Libraries

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Run Python Application

```bash
python app.py
```

### Run Streamlit Application

```bash
streamlit run streamlit_app.py
```

The application will open in your browser.

---

## Requirements

The main dependencies include:

```
opencv-python
mediapipe
numpy
streamlit
screen-brightness-control
```

---

## Applications

- Touch-free computer control
- Accessibility solutions
- Smart Human Computer Interaction
- AI-based gesture control systems

---

## Future Enhancements

- Add support for multiple hand gestures
- Control volume using gestures
- Add voice command integration
- Deploy as a desktop application
- Improve gesture recognition accuracy using deep learning models

---

## Author

**Aiswarya**

MSc Computer Science (Data Analytics)

---

## License

This project is created for educational purposes.