import cv2
import HandTrackingModule as htm


_cap = None
_running = None
_wCam, _hCam = 600, 300
_detector = None
_gesture = {
    'direction': None
}
_last_direction = None

def setup():
    global _cap, _running, _wCam, _hCam, _detector
    _cap = cv2.VideoCapture(0)
    _cap.set(3, _wCam)
    _cap.set(4, _hCam)
    _running = True
    _detector = htm.handDetector(maxHands=1, detectionCon=0.85) 


def stop():
    global _cap, _running
    _running = False
    if _cap:
        _cap.release()
    cv2.destroyAllWindows()

def getDirections():
    return dict(_gesture)

def MainLoop():
    global _cap, _running, _wCam, _hCam, _detector, _gesture, _last_direction

    while _running:
        success, img = _cap.read()
        if not success:
            print("Not able to open camera....")
            _running = False
            stop()
        img = cv2.flip(img, 1)
        
        img = _detector.findHands(img, True)
        lmList, _ = _detector.findPosition(img, draw=False)
        if(len(lmList)==0):
            _gesture["direction"] = _last_direction
        if len(lmList) != 0:
            fingers = _detector.fingersUp()
        
            # print(fingers.count(1))
            MRPfingersClosed = fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 # middle, ring and pinkie finger band hogi
            fist = fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0 and fingers[0] == 0
            new_dir = None
            if fist:
                print("Down")
                new_dir = 3

            elif MRPfingersClosed:
                x_tip, y_tip = lmList[8][1], lmList[8][2]
                x_base, y_base = lmList[6][1], lmList[6][2]

                dx = x_tip - x_base
                dy = y_tip - y_base

                threshold = 20
                if abs(dx) < threshold and abs(dy) < threshold:
                    new_dir = None 
                else:
                    if abs(dx) > abs(dy):
                        if dx > 0:
                            print("RIGHT")
                            new_dir = 2
                        else:
                            print("LEFT")
                            new_dir = 4
                    else:
                        if dy < 0:
                            print("UP")
                            new_dir = 1
                        else:
                            print("Down")
                            new_dir = 3

            if new_dir is not None and new_dir != _last_direction:
                if not (
                    (_last_direction == 1 and new_dir == 3) or  # UP → DOWN
                    (_last_direction == 3 and new_dir == 1) or  # DOWN → UP
                    (_last_direction == 2 and new_dir == 4) or  # RIGHT → LEFT
                    (_last_direction == 4 and new_dir == 2)     # LEFT → RIGHT
                ):
                    _gesture['direction'] = new_dir
                    _last_direction = new_dir
            
        print(getDirections())
        cv2.imshow("Snake Gesture Game", img)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
                stop()


if __name__ == "__main__":
    setup()
    MainLoop()