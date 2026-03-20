import cv2
import threading
import HandTrackingModule as htm


_cap = None
_running = None
_detector = None
_gesture = {"fingers": -1} #-1=agr kuch bhi nahi hai, 0=when fist gesture for selection, 1-4-fingers for option
_lock = threading.Lock()


def start():  # this will start the camera of device
    global _cap, _detector, _running
    if _running:
        return
    _cap = cv2.VideoCapture(0)
    _cap.set(3, 1280)
    _cap.set(4, 720)
    _detector = htm.handDetector(maxHands=1, detectionCon=0.85)
    _running = True
    threading.Thread(target=_loop, deamon=True).start()
    print("[Quiz Game Started]")

def stop(): # this will stop the logic
    global _cap, _running
    _running = False
    if _cap:
        _cap.release()
        _cap = None
    
    print("[Quiz Game Stoped]")

def get_gesture(): # je sirf JS ko gesture return karega
    with _lock:
        return dict(_gesture)
    
def _loop():
    global _gesture
    while _running:
        if not _cap or not _cap.isOpened():
            break
        success, img = _cap.read()
        if not success:
            #print("Can't Open Camera")
            #break
            continue
        img = cv2.flip(img, 1)
        img = _detector.findHands(img, draw=True)
        lmList, _ = _detector.findPosition(img, draw=False)
        
        count = -1 # default kuch bhi nahi hoga

        if len(lmList) != 0:
            fingers = _detector.fingersUp()
             # Exact same logic as your quizGame.py
            option1 = fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0 and fingers[0]==0
            option2 = fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0 and fingers[0]==0
            option3 = fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0 and fingers[0]==0
            option4 = fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1 and fingers[0]==0
            selectOption    = fingers[1]==0 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0 and fingers[0]==0

            if option1:
                count = 1
            elif option2:
                count = 2
            elif option3:
                count = 3 
            elif option4:
                count = 4
            elif selectOption:
                count = 0

            with _lock:
                _gesture['fingers'] = count
        
        cv2.imshow("Quiz Game", img)