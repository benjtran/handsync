'''
============================================================================
   HandSync - hand_control.py
   Author: Benjamin Tran
   Description: Creating meaning from inputs derived from hand detection
============================================================================
'''



''' ============================
   1. Serial Communication Setup
============================ '''

import cv2
import numpy as np
import serial.tools.list_ports
import hand_detecting as htm

# Instatiates camera feed for camera 0
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Searches for available ports on computer
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

# Adds each port to the list and prints out to user for selection
for one in ports:
    portsList.append(str(one))
    print(str(one))

com = input("Select Com Port for Arduino #: ")

# Confirms that selected port matches one in the list
for i in range(len(portsList)):
    if portsList[i].startswith("COM" + str(com)):
        use = "COM" + str(com)
        print(use)

# Opens serial port for communication
serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()

# Initialize the hand detector object w/ 70% confidence and 1 hand detected max
detector = htm.handDetector(detectionCon=0.7, maxHands=1)



''' ============================
   2. Reading and Sending Hands
============================ '''

while True:
    # Read a new frame from the webcam
    success, img = cap.read()

    # Detect hands in the image
    img = detector.findHands(img)

    # Get list of landmarks (21 points per detected hand)
    lmList = detector.findPosition(img, draw=False)

    # Initialize angles
    palm_angle = 0
    wrist_angle = 0

    # Proceed if any landmarks were found
    if len(lmList) != 0:
        print(lmList)

        # ----------- WRIST ANGLE DETECTION (using landmarks 0, 5, 17) -----------

        # Draw line between landmarks 5 and 17 (side of the palm)
        cv2.line(img, (lmList[5][1], lmList[5][2]), (lmList[17][1], lmList[17][2]), (255, 0, 0), 3)
        a_wrist = np.hypot(lmList[5][1] - lmList[17][1], lmList[5][2] - lmList[17][2])  # side A

        # Draw line between wrist center and base of index finger
        cv2.line(img, (lmList[0][1], lmList[0][2]), (lmList[5][1], lmList[5][2]), (255, 0, 0), 3)
        b_wrist = np.hypot(lmList[0][1] - lmList[5][1], lmList[0][2] - lmList[5][2])  # side B

        # Draw line between wrist center and base of pinky
        cv2.line(img, (lmList[17][1], lmList[17][2]), (lmList[0][1], lmList[0][2]), (255, 0, 0), 3)
        c_wrist = np.hypot(lmList[0][1] - lmList[17][1], lmList[0][2] - lmList[17][2])  # side C

        # Use cosine law to calculate angle at landmark 0 (wrist)
        palm_angle = round(
            (np.arccos((b_wrist**2 + c_wrist**2 - a_wrist**2) / (2 * b_wrist * c_wrist)) * 180 / np.pi) / 49 * 90, 0)
        palm_angle = min(palm_angle, 90)  # clamp to 90

        # Adjust based on hand orientation
        if lmList[17][1] < lmList[5][1]:
            wrist_angle = 90 - palm_angle
        else:
            wrist_angle = 90 + palm_angle

        print(wrist_angle)

        # ----------- INDEX FINGER ANGLE DETECTION (landmarks 5, 6, 8) -----------

        # Finger bent angle at knuckle
        cv2.line(img, (lmList[8][1], lmList[8][2]), (lmList[5][1], lmList[5][2]), (0, 255, 0), 3)
        a_point = np.hypot(lmList[8][1] - lmList[5][1], lmList[8][2] - lmList[5][2])

        cv2.line(img, (lmList[6][1], lmList[6][2]), (lmList[8][1], lmList[8][2]), (0, 255, 0), 3)
        b_point = np.hypot(lmList[6][1] - lmList[8][1], lmList[6][2] - lmList[8][2])

        cv2.line(img, (lmList[5][1], lmList[5][2]), (lmList[6][1], lmList[6][2]), (0, 255, 0), 3)
        c_point = np.hypot(lmList[5][1] - lmList[6][1], lmList[5][2] - lmList[6][2])

        pointer_angle = round(
            np.arccos((b_point**2 + c_point**2 - a_point**2) / (2 * b_point * c_point)) * 180 / np.pi, 0)
        print(pointer_angle)

        # ----------- MIDDLE FINGER ANGLE (landmarks 9, 10, 12) -----------

        cv2.line(img, (lmList[9][1], lmList[9][2]), (lmList[12][1], lmList[12][2]), (0, 255, 0), 3)
        a_middle = np.hypot(lmList[9][1] - lmList[12][1], lmList[9][2] - lmList[12][2])

        cv2.line(img, (lmList[12][1], lmList[12][2]), (lmList[10][1], lmList[10][2]), (0, 255, 0), 3)
        b_middle = np.hypot(lmList[12][1] - lmList[10][1], lmList[12][2] - lmList[10][2])

        cv2.line(img, (lmList[10][1], lmList[10][2]), (lmList[9][1], lmList[9][2]), (0, 255, 0), 3)
        c_middle = np.hypot(lmList[10][1] - lmList[9][1], lmList[10][2] - lmList[9][2])

        middle_angle = round(
            np.arccos((b_middle**2 + c_middle**2 - a_middle**2) / (2 * b_middle * c_middle)) * 180 / np.pi, 0)
        print(middle_angle)

        # ----------- RING FINGER ANGLE (landmarks 13, 14, 16) -----------

        cv2.line(img, (lmList[13][1], lmList[13][2]), (lmList[16][1], lmList[16][2]), (0, 255, 0), 3)
        a_ring = np.hypot(lmList[13][1] - lmList[16][1], lmList[13][2] - lmList[16][2])

        cv2.line(img, (lmList[16][1], lmList[16][2]), (lmList[14][1], lmList[14][2]), (0, 255, 0), 3)
        b_ring = np.hypot(lmList[16][1] - lmList[14][1], lmList[16][2] - lmList[14][2])

        cv2.line(img, (lmList[14][1], lmList[14][2]), (lmList[13][1], lmList[13][2]), (0, 255, 0), 3)
        c_ring = np.hypot(lmList[14][1] - lmList[13][1], lmList[14][2] - lmList[13][2])

        ring_angle = round(
            np.arccos((b_ring**2 + c_ring**2 - a_ring**2) / (2 * b_ring * c_ring)) * 180 / np.pi, 0)
        print(ring_angle)

        # ----------- PINKY FINGER ANGLE (landmarks 17, 18, 20) -----------

        cv2.line(img, (lmList[17][1], lmList[17][2]), (lmList[20][1], lmList[20][2]), (0, 255, 0), 3)
        a_pinky = np.hypot(lmList[17][1] - lmList[20][1], lmList[17][2] - lmList[20][2])

        cv2.line(img, (lmList[20][1], lmList[20][2]), (lmList[18][1], lmList[18][2]), (0, 255, 0), 3)
        b_pinky = np.hypot(lmList[20][1] - lmList[18][1], lmList[20][2] - lmList[18][2])

        cv2.line(img, (lmList[18][1], lmList[18][2]), (lmList[17][1], lmList[17][2]), (0, 255, 0), 3)
        c_pinky = np.hypot(lmList[18][1] - lmList[17][1], lmList[18][2] - lmList[17][2])

        pinky_angle = round(
            np.arccos((b_pinky**2 + c_pinky**2 - a_pinky**2) / (2 * b_pinky * c_pinky)) * 180 / np.pi, 0)
        print(pinky_angle)

        # ----------- THUMB ANGLE (landmarks 2, 3, 4) -----------

        cv2.line(img, (lmList[2][1], lmList[2][2]), (lmList[4][1], lmList[4][2]), (0, 255, 0), 3)
        a_thumb = np.hypot(lmList[2][1] - lmList[4][1], lmList[2][2] - lmList[4][2])

        cv2.line(img, (lmList[4][1], lmList[4][2]), (lmList[3][1], lmList[3][2]), (0, 255, 0), 3)
        b_thumb = np.hypot(lmList[4][1] - lmList[3][1], lmList[4][2] - lmList[3][2])

        cv2.line(img, (lmList[3][1], lmList[3][2]), (lmList[2][1], lmList[2][2]), (0, 255, 0), 3)
        c_thumb = np.hypot(lmList[3][1] - lmList[2][1], lmList[3][2] - lmList[2][2])

        thumb_angle = round(
            np.arccos((b_thumb**2 + c_thumb**2 - a_thumb**2) / (2 * b_thumb * c_thumb)) * 180 / np.pi, 0)
        print(thumb_angle)

        # ----------- SEND ANGLES TO ARDUINO -----------

        # Format all angles into a single comma-separated string
        data = f"{wrist_angle},{pointer_angle},{middle_angle},{ring_angle},{pinky_angle},{thumb_angle}\n"

        # Send over serial to Arduino
        serialInst.write(data.encode('utf-8'))

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the processed image
    cv2.imshow("Img", img)
    cv2.waitKey(1)

# Clean up when loop ends
cap.release()
cv2.destroyAllWindows()
serialInst.close()