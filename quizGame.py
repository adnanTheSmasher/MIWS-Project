import cv2
import threading
import HandTrackingModule as htm
import time

_last_gesture = -1  # yar i am changing the logic fist wala kaam nahi karraha 
_gesture_start_time = 0
HOLD_TIME = 1.5  # seconds 
_confirmed = False

_cap = None
_running = False
_detector = None
_gesture = {"fingers": -1, "holding": -1, "progress": 0} #-1=agr kuch bhi nahi hai, 0=when fist gesture for selection, 1-4-fingers for option
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
    threading.Thread(target=_loop, daemon=True).start()
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
    global _last_gesture, _gesture_start_time, _confirmed, _gesture
    while _running:
        if not _cap or not _cap.isOpened():
            break
        success, img = _cap.read()
        if not success:
            #print("Can't Open Camera")
            #break
            continue
        img = cv2.flip(img, 1)
        img = _detector.findHands(img, draw=False)
        lmList, _ = _detector.findPosition(img, draw=False)
        
        count = -1 # default kuch bhi nahi hoga

        if len(lmList) != 0:
            fingers = _detector.fingersUp()
             # Exact same logic as your quizGame.py
            option1 = fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0 and fingers[0]==0
            option2 = fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0 and fingers[0]==0
            option3 = fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0 and fingers[0]==0
            option4 = fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==1 and fingers[0]==0
           
            if option1:
                count = 1
            elif option2:
                count = 2
            elif option3:
                count = 3 
            elif option4:
                count = 4
        
        current_time = time.time()

        if _confirmed:
            if count == -1:
                _confirmed = False
                _last_gesture = -1
                _gesture_start_time = current_time
                with _lock:
                    _gesture['holding'] = -1
                    _gesture['fingers'] = -1
                    _gesture['progress'] = 0
                continue

        if count != _last_gesture:
            _last_gesture = count
            _gesture_start_time = current_time
            with _lock:
                _gesture['fingers'] = -1
                _gesture['holding'] = count
                _gesture['progress'] = 0

        if count != -1:
            hold_time = current_time - _gesture_start_time
            progress = min(int((hold_time/HOLD_TIME) * 100), 100)

            if hold_time >= HOLD_TIME:
                with _lock:
                    _gesture['holding'] = count
                    _gesture['fingers'] = count
                    _gesture['progress'] = 100
                _confirmed = True
            else:
                with _lock:  # not yet confirmed
                    _gesture['holding'] = count
                    _gesture['fingers']  = -1   # not yet confirmed
                    _gesture['progress'] = progress

        else:
            with _lock:
                _gesture['fingers']  = -1
                _gesture['holding'] = -1
                _gesture['progress'] = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop()
            break
