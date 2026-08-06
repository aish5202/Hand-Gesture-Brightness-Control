import streamlit as st
import cv2
import numpy as np
import time
import os

from utils.hand_detector import HandDetector
from utils.brightness_controller import BrightnessController


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


# ----------------------------
# Dashboard Layout
# ----------------------------

col1, col2 = st.columns([3, 1])


frame_placeholder = col1.empty()


status = col2.empty()

brightness_text = col2.empty()

distance_text = col2.empty()


fps_text = col2.empty()


progress = col2.progress(0)



# ----------------------------
# Camera Input
# ----------------------------

st.subheader("📷 Camera")

image = st.camera_input(
    "Capture your hand"
)



# ----------------------------
# Processing
# ----------------------------

if image is not None:


    start_time = time.time()


    detector = HandDetector(
        detectionCon=detect_conf,
        trackCon=track_conf
    )


    brightness = BrightnessController()



    # Convert image

    bytes_data = image.getvalue()


    img = cv2.imdecode(
        np.frombuffer(
            bytes_data,
            np.uint8
        ),
        cv2.IMREAD_COLOR
    )



    # Mirror image

    img = cv2.flip(
        img,
        1
    )



    # Detect hands

    img = detector.findHands(
        img
    )


    lmList = detector.findPosition(
        img
    )


    brightnessValue = 0

    distance = 0



    # ----------------------------
    # Finger Distance
    # ----------------------------

    if len(lmList) != 0:


        x1 = lmList[4][1]
        y1 = lmList[4][2]


        x2 = lmList[8][1]
        y2 = lmList[8][2]



        cv2.circle(
            img,
            (x1,y1),
            10,
            (255,0,255),
            cv2.FILLED
        )


        cv2.circle(
            img,
            (x2,y2),
            10,
            (255,0,255),
            cv2.FILLED
        )



        cv2.line(
            img,
            (x1,y1),
            (x2,y2),
            (0,255,0),
            3
        )



        distance = brightness.calculateDistance(
            (x1,y1),
            (x2,y2)
        )



        brightnessValue = brightness.distanceToBrightness(
            distance
        )



        status.success(
            "🟢 Hand Detected"
        )



    else:


        status.error(
            "🔴 No Hand Detected"
        )



    # ----------------------------
    # Display Values
    # ----------------------------


    brightness_text.metric(
        "Brightness Level",
        f"{brightnessValue}%"
    )



    distance_text.metric(
        "Finger Distance",
        f"{int(distance)} px"
    )



    progress.progress(
        int(brightnessValue)
    )



    fps = 1 / (time.time() - start_time)



    fps_text.metric(
        "FPS",
        f"{int(fps)}"
    )



    # Convert color

    img = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )



    frame_placeholder.image(
        img,
        channels="RGB",
        use_container_width=True
    )



# ----------------------------
# Information
# ----------------------------

st.markdown("---")

st.info(
    """
    ### How it works

    🖐 Hand is detected using MediaPipe.

    👍 Thumb and index finger distance is calculated.

    📏 Distance is converted into brightness percentage.

    ⚠️ Streamlit Cloud can show gesture detection,
    but cannot control your laptop brightness.

    Run locally for actual screen brightness control.
    """
)