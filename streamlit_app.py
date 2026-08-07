import streamlit as st
import cv2
import av

from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
    RTCConfiguration
)

from utils.hand_detector import HandDetector
from utils.brightness_controller import BrightnessController


# -----------------------------------
# Page Configuration
# -----------------------------------

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


# -----------------------------------
# Sidebar Settings
# -----------------------------------

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


# -----------------------------------
# WebRTC Configuration
# -----------------------------------

RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": [
                    "stun:stun.l.google.com:19302",
                    "stun:stun1.l.google.com:19302",
                    "stun:stun2.l.google.com:19302"
                ]
            },
            {
                "urls": [
                    "stun:stun.cloudflare.com:3478"
                ]
            }
        ]
    }
)


# -----------------------------------
# Video Processor
# -----------------------------------

class VideoProcessor(VideoProcessorBase):

    def __init__(self):

        self.detector = HandDetector(
            detectionCon=detection_confidence,
            trackCon=tracking_confidence
        )

        self.brightness_controller = BrightnessController()

        self.current_brightness = 50


    def recv(self, frame):

        try:

            img = frame.to_ndarray(
                format="bgr24"
            )


            # Hand Detection

            img, level = self.detector.findHands(
                img
            )


            # Update brightness value

            if level is not None:

                self.current_brightness = level


                # Enable only on local computer
                # self.brightness_controller.set_brightness(level)



            # Display brightness

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


        except Exception:

            return frame



# -----------------------------------
# Start Webcam
# -----------------------------------

webrtc_streamer(
    key="brightness-control",

    video_processor_factory=VideoProcessor,

    rtc_configuration=RTC_CONFIGURATION,

    media_stream_constraints={
        "video": True,
        "audio": False
    },

    async_processing=True
)