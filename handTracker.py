
from cvzone.HandTrackingModule import HandDetector


class HandTracker:

    def __init__(self):
        self.detector = HandDetector(
            staticMode=False,
            maxHands=1,
            modelComplexity=1,
            detectionCon=0.7,
            minTrackCon=0.6
        )

    def findHands(self, img):
        hands, img = self.detector.findHands(
            img,
            draw=True,
            flipType=False
        )
        return hands, img
