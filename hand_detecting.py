'''
============================================================================
   HandSync - hand_detecting.py
   Author: Benjamin Tran
   Description: Detecting and extracting hand position landmarks
============================================================================
'''



import cv2
import mediapipe as mp


class handDetector():
    # Initializing hand detector with dedicated parameters
    def __init__(self, mode=False, maxHands=2, modelComp=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelComp = modelComp
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComp, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    # Detecting hands
    def findHands(self, img, draw=True):
        # Converting from BGR to RGB 
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # Draws hand landmark locations on camera image
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    # Finds landmark positions on hand
    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # Converts landmark locations to pixel coordinates for usage
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

        return lmList

def main():
    # Opens the webcam
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # Creates an instance of the hand detector
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[17][0])
    
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()