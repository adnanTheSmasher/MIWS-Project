import cv2
import HandTrackingModule as htm
import time


_gesture = {"fingers": -1, "holding": -1, "progress": 0} #-1=agr kuch bhi nahi hai, 0=when fist gesture for selection, 1-4-fingers for option
_cap = None
_running = True
_detector = None
RIGHT = "Right"
LEFT = "Left"

def setup():
    global _cap, _running, _detector
    _cap = cv2.VideoCapture(0)
    _cap.set(3, 1280)
    _cap.set(4, 720)
    _running = True
    _detector = htm.handDetector(maxHands=1, detectionCon=0.85)

def stop():
    global _cap, _running
    _running = False
    if _cap: 
        _cap.release()
    cv2.destroyAllWindows()


def loopForGesture():
    global _cap, _running, _detector
    while _running:
        success, img = _cap.read()
        if not success:
            print("NOt abelt o open camera")
            break
        img = cv2.flip(img, 1)
        img = _detector.findHands(img, draw=True)
        lmList, _ = _detector.findPosition(img, draw=False)
        hands = _detector.fingersUpBothHands(img)

        right_hand = hands.get(RIGHT, [])
        left_hand = hands.get(LEFT, [])

        if len(right_hand) == 5: # right hand screen pai hai
             selected = sum(right_hand)

             if 0 < selected < 5 :
                  print("Selected Option: ", selected)
        
        if len(left_hand) == 5: # left hand screen pai hai
            if sum(left_hand) == 0:
                 print("confirmed")

            


        cv2.imshow("Quiz Gesture Capture", img)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
                stop()
                break


if __name__ == "__main__":
    setup()
    loopForGesture()