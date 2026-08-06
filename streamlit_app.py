import streamlit as st
import cv2
import time

from utils.hand_detector import HandDetector
from utils.brightness_controller import BrightnessController

import sys
import mediapipe as mp
import os
os.environ["MEDIAPIPE_DISABLE_GPU"] = "1"

# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="Hand Gesture Brightness Control",
    page_icon="🖐",
    layout="wide"
)

st.title("🖐 Hand Gesture Based Screen Brightness Control")
st.markdown("---")

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.title("Project Settings")

camera = st.sidebar.selectbox(
    "Camera",
    [0]
)

detect_conf = st.sidebar.slider(
    "Detection Confidence",
    0.1,
    1.0,
    0.7
)

track_conf = st.sidebar.slider(
    "Tracking Confidence",
    0.1,
    1.0,
    0.7
)

start = st.sidebar.button("▶ Start Camera")
stop = st.sidebar.button("⏹ Stop Camera")

# ----------------------------
# Dashboard
# ----------------------------

col1, col2 = st.columns([3,1])

frame_placeholder = col1.empty()

status = col2.empty()
brightness_text = col2.empty()
distance_text = col2.empty()
fps_text = col2.empty()
progress = col2.progress(0)

# ----------------------------
# Camera
# ----------------------------

if start:

    cap = cv2.VideoCapture(camera)

    detector = HandDetector(
        detectionCon=detect_conf,
        trackCon=track_conf
    )

    brightness = BrightnessController()

    prev = time.time()

    while cap.isOpened():

        if stop:
            break

        success, img = cap.read()

        if not success:
            break

        img = cv2.flip(img,1)

        img = detector.findHands(img)

        lmList = detector.findPosition(img)

        brightnessValue = 0
        distance = 0

        if len(lmList) != 0:

            x1,y1 = lmList[4][1],lmList[4][2]
            x2,y2 = lmList[8][1],lmList[8][2]

            cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)

            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),3)

            distance = brightness.calculateDistance(
                (x1,y1),
                (x2,y2)
            )

            brightnessValue = brightness.distanceToBrightness(
                distance
            )

            brightness.setBrightness(brightnessValue)

            status.success("🟢 Hand Detected")

        else:

            status.error("🔴 No Hand")

        progress.progress(brightnessValue)

        brightness_text.metric(
            "Brightness",
            f"{brightnessValue}%"
        )

        distance_text.metric(
            "Distance",
            f"{int(distance)} px"
        )

        now = time.time()

        fps = 1/(now-prev)

        prev = now

        fps_text.metric(
            "FPS",
            int(fps)
        )

        img = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        frame_placeholder.image(
            img,
            channels="RGB",
            use_container_width=True
        )

    cap.release()