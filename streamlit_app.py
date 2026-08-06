import streamlit as st
import cv2
import av
import numpy as np

from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
    RTCConfiguration
)

from utils.hand_detector import HandDetector
from utils.brightness_controller import BrightnessController


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Hand Gesture Brightness Control",
    page_icon="🖐",
    layout="wide"
)


st.title("🖐 Hand Gesture Based Screen Brightness Control")

st.write(
    "Control brightness using hand gestures "
    "using OpenCV and MediaPipe."
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.header("Project Settings")

detection_confidence = st.sidebar.slider(
    "Detection Confidence",
    0.1,
    1.0,
    0.7
)

tracking_confidence = st.sidebar.slider(
    "Tracking Confidence",
    0.1,
    1.0,
    0.7
)


# -----------------------------
# WebRTC Configuration
# -----------------------------

RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": [
                    "stun:stun.l.google.com:19302"
                ]
            }
        ]
    }
)


# -----------------------------
# Video Processor
# -----------------------------

class VideoProcessor(VideoProcessorBase):

    def __init__(self):

        self.detector = HandDetector(
            detectionCon=detection_confidence,
            trackCon=tracking_confidence
        )

        self.brightness = BrightnessController()

        self.current_brightness = 50


    def recv(self, frame):

        img = frame.to_ndarray(
            format="bgr24"
        )


        # Detect hands

        img, level = self.detector.findHands(
            img
        )


        # Display brightness

        if level is not None:

            self.current_brightness = level


            # For local machine only
            # self.brightness.set_brightness(level)


        cv2.putText(
            img,
            f"Brightness: {self.current_brightness}%",
            (20,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )


        return av.VideoFrame.from_ndarray(
            img,
            format="bgr24"
        )



# -----------------------------
# Start Camera
# -----------------------------

webrtc_streamer(
    key="brightness-control",
    video_processor_factory=VideoProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={
        "video": True,
        "audio": False
    }
)