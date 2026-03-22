import cv2
import mediapipe as mp
import time
import math


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon)

        self.mp_draw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]


    def findHands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmlist.append([id, cx, cy])
                xList.append(cx)
                yList.append(cy)
                # if id == 4:
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin-20, ymin-20), (xmax+20, ymax+20), (0, 255, 0), 2)
        return self.lmlist, bbox

    def fingersUp(self):
        fingers = []
        # for Thumb
        if self.lmlist[self.tipIds[0]][1] < self.lmlist[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #for Fingers
        for id in range(1, 5):
            if self.lmlist[self.tipIds[id]][2] < self.lmlist[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
    
    def fingersUpBothHands(self, img):
        hands_data = {
            'Left': [], 'Right': []
        }

        if self.results.multi_hand_landmarks:
            for handNo, handLms in enumerate(self.results.multi_hand_landmarks):
                lmList = []
                #print(f"handNo = {handNo},  handLms = {handLms}")
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    lmList.append([id, int(lm.x*w), int(lm.y*h)])

                handtype = self.results.multi_handedness[handNo].classification[0].label.strip()
                fingers = []
               
                 # Thumb
                if handtype == "Right":
                    if lmList[self.tipIds[0]][1] < lmList[self.tipIds[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                elif handtype == "Left":    
                    if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # Fingers
                for id in range(1, 5):
                    if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0) 
                
                hands_data[handtype] = fingers
        return hands_data


    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmlist[p1][1], self.lmlist[p1][2]
        x2, y2 = self.lmlist[p2][1], self.lmlist[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]


def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = handDetector(maxHands=2, detectionCon=0.85)

    while True:
        success, img = cap.read()
        if not success:
            break
        img = detector.findHands(img)
        lmlist = detector.findPosition(img, draw=False)
        print(detector.fingersUpBothHands())
        #if len(lmlist) != 0:
        #    print(lmlist[4])
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)
        cv2.imshow("MediaPipe Hands", img)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()