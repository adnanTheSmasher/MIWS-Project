import cv2
import time
import numpy as np
import os
import HandTrackingModule as htm

def hex_to_bgr(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (b, g, r)


folderPath = "images"
myList = os.listdir(folderPath)
overlayList = []
for imgPath in myList:
    img = cv2.imread(f"{folderPath}/{imgPath}")
    overlayList.append(img)

#print(myList)
#print(len(overlayList))

header = overlayList[0]
color1 = hex_to_bgr("#ffffff")
color2 = hex_to_bgr("#7ed957")
color3 = hex_to_bgr("#38b6ff")
eraserColor = hex_to_bgr("#0d0a0c")
drawColor = color1
brushThickness = 5
eraserThickness = 30


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 800)

detector = htm.handDetector(detectionCon=0.85, maxHands=1)
xp, yp = 0, 0
imgCanvas = None


while True:
    success, img = cap.read()
    if not success:
        print("Error opeining camera")
        break
    if imgCanvas is None:
        imgCanvas = np.zeros_like(img)

    img = cv2.flip(img, 1)
    img = detector.findHands(img, draw=True)
    lmList, _ = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        #print(lmList)
        x1, y1 = lmList[8][1], lmList[8][2] # Tip of Index Finger
        x2, y2 = lmList[12][1], lmList[12][2] # Tip of Middle Finger

        fingers = detector.fingersUp()
        indexFinger_open = fingers[1] == 1 and fingers[0] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0
        selectionFinger_open = fingers[1] == 1 and fingers[0] == 0 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0

        #print(fingers.count(1))

        # Selection Mode 
        if selectionFinger_open:
            print("Selection Phase")
            xp, yp = 0, 0
            if y1 < 130:
                if 145<x1<280:
                    header = overlayList[0]
                    drawColor = color1
                elif 450 < x1 < 600:
                    header = overlayList[1]
                    drawColor = color2
                elif 775<x1<910:
                    header = overlayList[2]
                    drawColor = color3
                elif 1060<x1<1120:
                    header = overlayList[3]
                    drawColor = eraserColor
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 5)
        # Drawing Mode
        if indexFinger_open:
            print("Drawing Mode")
            if xp==0 and yp==0:
                xp, yp = x1, y1

            if drawColor == eraserColor:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
         
            xp, yp = x1, y1
        
        if not indexFinger_open and not selectionFinger_open:
            xp, yp = x1, y1 

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)


    img[0:130, 0:1280] = header 
    cv2.namedWindow("Air Canvas - Painter", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Air Canvas - Painter", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Air Canvas - Painter", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

