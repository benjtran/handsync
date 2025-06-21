import cv2
import numpy as np
import serial.tools.list_ports
import hand_detecting as htm

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for one in ports:
    portsList.append(str(one))
    print(str(one))

com = input("Select Com Port for Arduino #: ")

for i in range(len(portsList)):
    if portsList[i].startswith("COM" + str(com)):
        use = "COM" + str(com)
        print(use)

serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

while True:
    #command = angle of rotation. This will hold your calculated angle
    #serialInst.write(command.encode('utf-8')). This will send ur angle to arduino

    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    palm_angle = 0
    wrist_angle = 0

    if len(lmList) != 0:
        print(lmList)

        # ----------------------WRIST DETECTION------------------------

        # LINE 5-17: A
        cv2.line(img, (lmList[5][1], lmList[5][2]), (lmList[17][1], lmList[17][2]), (255, 0, 0), 3)
        a_wrist = np.hypot(lmList[5][1] - lmList[17][1], lmList[5][2] - lmList[17][2])

        #LINE 0 - 5: B
        cv2.line(img, (lmList[0][1], lmList[0][2]), (lmList[5][1], lmList[5][2]), (255, 0, 0), 3)
        b_wrist = np.hypot(lmList[0][1] - lmList[5][1], lmList[0][2] - lmList[5][2])

        #LINE 17-0: C
        cv2.line(img, (lmList[17][1], lmList[17][2]), (lmList[0][1], lmList[0][2]), (255, 0, 0), 3)
        c_wrist = np.hypot(lmList[0][1] - lmList[17][1], lmList[0][2] - lmList[17][2])

        #PALM ANGLE: BETWEEN 5 AND 17
        palm_angle = round((np.arccos((b_wrist * b_wrist + c_wrist * c_wrist - a_wrist * a_wrist)/(2 * b_wrist * c_wrist)) * 180 / np.pi) /49 * 90, 0)
        if palm_angle > 90:
            palm_angle = 90

        #WRIST ANGLE
        if lmList[17][1] < lmList[5][1] :
            wrist_angle = 90 - palm_angle
        else:
            wrist_angle = 90 + palm_angle

        print(wrist_angle)

        # ----------------------POINTER DETECTION------------------------

        # LINE 8-5: A
        cv2.line(img, (lmList[8][1], lmList[8][2]), (lmList[5][1], lmList[5][2]), (0, 255, 0), 3)
        a_point = np.hypot(lmList[8][1] - lmList[5][1], lmList[8][2] - lmList[5][2])

        # LINE 6-8: B
        cv2.line(img, (lmList[6][1], lmList[6][2]), (lmList[8][1], lmList[8][2]), (0, 255, 0), 3)
        b_point = np.hypot(lmList[6][1] - lmList[8][1], lmList[6][2] - lmList[8][2])

        # LINE 8-5: C
        cv2.line(img, (lmList[5][1], lmList[5][2]), (lmList[6][1], lmList[6][2]), (0, 255, 0), 3)
        c_point = np.hypot(lmList[5][1] - lmList[6][1], lmList[5][2] - lmList[6][2])

        # POINTER ANGLE: BETWEEN 5 AND 8
        pointer_angle = round((np.arccos((b_point * b_point + c_point * c_point - a_point * a_point) / (2 * b_point * c_point)) * 180 / np.pi), 0)

        print(pointer_angle)

        # ----------------------MIDDLE DETECTION------------------------

        # LINE 9-12: A
        cv2.line(img, (lmList[9][1], lmList[9][2]), (lmList[12][1], lmList[12][2]), (0, 255, 0), 3)
        a_middle = np.hypot(lmList[9][1] - lmList[12][1], lmList[9][2] - lmList[12][2])

        # LINE 12-10: B
        cv2.line(img, (lmList[12][1], lmList[12][2]), (lmList[10][1], lmList[10][2]), (0, 255, 0), 3)
        b_middle = np.hypot(lmList[12][1] - lmList[10][1], lmList[12][2] - lmList[10][2])

        # LINE 10-9: C
        cv2.line(img, (lmList[10][1], lmList[10][2]), (lmList[9][1], lmList[9][2]), (0, 255, 0), 3)
        c_middle = np.hypot(lmList[10][1] - lmList[9][1], lmList[10][2] - lmList[9][2])

        # POINTER ANGLE: BETWEEN 9 AND 12
        middle_angle = round((np.arccos((b_middle * b_middle + c_middle * c_middle - a_middle * a_middle) / (2 * b_middle * c_middle)) * 180 / np.pi), 0)

        print(middle_angle)

        # ----------------------RING DETECTION------------------------

        # LINE 13-16: A
        cv2.line(img, (lmList[13][1], lmList[13][2]), (lmList[16][1], lmList[16][2]), (0, 255, 0), 3)
        a_ring = np.hypot(lmList[13][1] - lmList[16][1], lmList[13][2] - lmList[16][2])

        # LINE 16-14: B
        cv2.line(img, (lmList[16][1], lmList[16][2]), (lmList[14][1], lmList[14][2]), (0, 255, 0), 3)
        b_ring = np.hypot(lmList[16][1] - lmList[14][1], lmList[16][2] - lmList[14][2])

        # LINE 14-13: C
        cv2.line(img, (lmList[14][1], lmList[14][2]), (lmList[13][1], lmList[13][2]), (0, 255, 0), 3)
        c_ring = np.hypot(lmList[14][1] - lmList[13][1], lmList[14][2] - lmList[13][2])

        # POINTER ANGLE: BETWEEN 13 AND 16
        ring_angle = round((np.arccos((b_ring * b_ring + c_ring * c_ring - a_ring * a_ring) / (
                    2 * b_ring * c_ring)) * 180 / np.pi), 0)

        print(ring_angle)

        # ----------------------PINKY DETECTION------------------------

        # LINE 17-20: A
        cv2.line(img, (lmList[17][1], lmList[17][2]), (lmList[20][1], lmList[20][2]), (0, 255, 0), 3)
        a_pinky = np.hypot(lmList[17][1] - lmList[20][1], lmList[17][2] - lmList[20][2])

        # LINE 20-18: B
        cv2.line(img, (lmList[20][1], lmList[20][2]), (lmList[18][1], lmList[18][2]), (0, 255, 0), 3)
        b_pinky = np.hypot(lmList[20][1] - lmList[18][1], lmList[20][2] - lmList[18][2])

        # LINE 18-17: C
        cv2.line(img, (lmList[18][1], lmList[18][2]), (lmList[17][1], lmList[17][2]), (0, 255, 0), 3)
        c_pinky = np.hypot(lmList[18][1] - lmList[17][1], lmList[18][2] - lmList[17][2])

        # POINTER ANGLE: BETWEEN 17 AND 20
        pinky_angle = round((np.arccos((b_pinky * b_pinky + c_pinky * c_pinky - a_pinky * a_pinky) / (
                2 * b_pinky * c_pinky)) * 180 / np.pi), 0)

        print(pinky_angle)

        # ----------------------THUMB DETECTION------------------------

        # LINE 2-4: A
        cv2.line(img, (lmList[2][1], lmList[2][2]), (lmList[4][1], lmList[4][2]), (0, 255, 0), 3)
        a_thumb = np.hypot(lmList[2][1] - lmList[4][1], lmList[2][2] - lmList[4][2])

        # LINE 4-3: B
        cv2.line(img, (lmList[4][1], lmList[4][2]), (lmList[3][1], lmList[3][2]), (0, 255, 0), 3)
        b_thumb = np.hypot(lmList[4][1] - lmList[3][1], lmList[4][2] - lmList[3][2])

        # LINE 3-2: C
        cv2.line(img, (lmList[3][1], lmList[3][2]), (lmList[2][1], lmList[2][2]), (0, 255, 0), 3)
        c_thumb = np.hypot(lmList[3][1] - lmList[2][1], lmList[3][2] - lmList[2][2])

        # POINTER ANGLE: BETWEEN 17 AND 20
        thumb_angle = round((np.arccos((b_thumb * b_thumb + c_thumb * c_thumb - a_thumb * a_thumb) / (
                2 * b_thumb * c_thumb)) * 180 / np.pi), 0)

        print(thumb_angle)


        data = f"{wrist_angle},{pointer_angle},{middle_angle},{ring_angle},{pinky_angle},{thumb_angle}\n"
        serialInst.write(data.encode('utf-8'))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow("Img", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
serialInst.close()