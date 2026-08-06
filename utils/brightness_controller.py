import math
import numpy as np
import screen_brightness_control as sbc


class BrightnessController:

    def __init__(self):
        self.minDistance = 30
        self.maxDistance = 220

    def calculateDistance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        distance = math.hypot(x2 - x1, y2 - y1)

        return distance

    def distanceToBrightness(self, distance):

        brightness = np.interp(
            distance,
            [self.minDistance, self.maxDistance],
            [0, 100]
        )

        return int(brightness)

    def setBrightness(self, brightness):

        brightness = max(0, min(100, brightness))

        try:
            sbc.set_brightness(brightness)
        except Exception:
            pass

        return brightness