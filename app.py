import cv2
import time

from utils.hand_detector import HandDetector
from utils.brightness_controller import BrightnessController

cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector()
brightness = BrightnessController()

previousTime = 0

while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    img = detector.findHands(img)

    lmList = detector.findPosition(img)

    brightnessValue = 0
    distance = 0

    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(img, (x1, y1), 12, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 12, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

        distance = brightness.calculateDistance((x1, y1), (x2, y2))

        brightnessValue = brightness.distanceToBrightness(distance)

        brightness.setBrightness(brightnessValue)

        # Brightness Bar

        bar = int(
            400 - ((brightnessValue / 100) * 300)
        )

        cv2.rectangle(img, (50, 150), (85, 450), (255, 255, 255), 3)

        cv2.rectangle(
            img,
            (50, bar),
            (85, 450),
            (0, 255, 0),
            cv2.FILLED
        )

        cv2.putText(
            img,
            f"{brightnessValue} %",
            (25, 500),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        status = "Hand Detected"

    else:
        status = "No Hand"

    currentTime = time.time()

    fps = 1 / (currentTime - previousTime) if previousTime != 0 else 0

    previousTime = currentTime

    # Top Panel

    cv2.rectangle(img, (0, 0), (1280, 90), (30, 30, 30), -1)

    cv2.putText(
        img,
        "Hand Gesture Brightness Control",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.putText(
        img,
        f"FPS : {int(fps)}",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        img,
        f"Distance : {int(distance)} px",
        (250, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        img,
        f"Brightness : {brightnessValue} %",
        (520, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        img,
        f"Status : {status}",
        (850, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.imshow("Hand Gesture Brightness Control", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()