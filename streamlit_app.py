import streamlit as st
import cv2
import av
import time
import numpy as np
import os

from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase
)

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


st.title(
    "🖐 Hand Gesture Based Screen Brightness Control"
)

st.markdown("---")


# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.title(
    "Project Settings"
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



# ----------------------------
# Dashboard
# ----------------------------

col1, col2 = st.columns(
    [3,1]
)


status_box = col2.empty()

brightness_box = col2.empty()

distance_box = col2.empty()

fps_box = col2.empty()

progress = col2.progress(0)



# ----------------------------
# Video Processor
# ----------------------------

class HandGestureProcessor(
    VideoProcessorBase
):

    def __init__(self):

        self.detector = HandDetector(
            detectionCon=detect_conf,
            trackCon=track_conf
        )

        self.brightness = BrightnessController()

        self.brightnessValue = 0
        self.distance = 0
        self.fps = 0

        self.prev_time = time.time()



    def recv(self, frame):

        img = frame.to_ndarray(
            format="bgr24"
        )


        img = cv2.flip(
            img,
            1
        )


        img = self.detector.findHands(
            img
        )


        lmList = self.detector.findPosition(
            img
        )



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


            self.distance = self.brightness.calculateDistance(
                (x1,y1),
                (x2,y2)
            )


            self.brightnessValue = self.brightness.distanceToBrightness(
                self.distance
            )


        else:

            self.brightnessValue = 0
            self.distance = 0



        current = time.time()


        self.fps = 1/(current-self.prev_time)


        self.prev_time = current



        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )



# ----------------------------
# Start Webcam
# ----------------------------

ctx = webrtc_streamer(
    key="hand-control",
    video_processor_factory=HandGestureProcessor,
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    async_processing=True
)



# ----------------------------
# Display Stats
# ----------------------------

if ctx.video_processor:


    processor = ctx.video_processor


    status_box.success(
        "🟢 Camera Running"
    )


    brightness_box.metric(
        "Brightness",
        f"{processor.brightnessValue}%"
    )


    distance_box.metric(
        "Distance",
        f"{int(processor.distance)} px"
    )


    fps_box.metric(
        "FPS",
        int(processor.fps)
    )


    progress.progress(
        int(processor.brightnessValue)
    )


else:

    status_box.warning(
        "Camera not started"
    )



# ----------------------------
# Information
# ----------------------------

st.markdown("---")


