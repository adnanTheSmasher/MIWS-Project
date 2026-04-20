import cv2
import HandTrackingModule as htm
import time


_gesture = {"fingers_right": -1, "fingers_left": -1, "progress": 0, 'direction': -1} #-1=agr kuch bhi nahi hai, 0=when fist gesture for selection, 1-4-fingers for option
_cap = None
_running = True
_detector = None
_last_direction = None
RIGHT = "Right"
LEFT = "Left"

def setup():
    global _cap, _running, _detector
    _cap = cv2.VideoCapture(0)
    _cap.set(3, 600)
    _cap.set(4, 300)
    _running = True
    _detector = htm.handDetector(maxHands=2, detectionCon=0.85)

def stop():
    global _cap, _running
    _running = False
    if _cap: 
        _cap.release()
    cv2.destroyAllWindows()


def getDirections():
    return dict(_gesture)

def resetProgress():
    global _gesture
    _gesture["progress"] = 0

def loopForGesture():
    global _cap, _running, _detector, _gesture, _last_direction
    if not _cap or not _cap.isOpened():
        print("Camera Not initialized....")
        _running = False
        return
    
    while _running:
        success, img = _cap.read()
        if not success:
            print("NOt abelt o open camera")
            time.sleep(0.1)
            break
        img = cv2.flip(img, 1)
        img = _detector.findHands(img, draw=True)
        hands = _detector.fingersUpBothHands(img)
        lmList, _ = _detector.findPosition(img)

        right_hand = hands.get(RIGHT, [])
        left_hand = hands.get(LEFT, [])

        if len(right_hand) == 5: # right hand screen pai hai
            selected = sum(right_hand)

            if 0 < selected < 5 :
                #print("Selected Option: ", selected)
                _gesture["fingers_right"] = selected
                _gesture["progress"] = 0
                MRPfingersClosed = right_hand[2] == 0 and right_hand[3]==0 and right_hand[4]==0 # middle, ring and pinkie finger band hogi
                fist = right_hand[1] == 1 and right_hand[2]==1 and right_hand[3]==1
                new_dir = None
                if fist:
                    print("Down")
                    new_dir = 3

                if MRPfingersClosed:
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
            
        if len(left_hand) == 5: # left hand screen pai hai
            selected = sum(left_hand)
            if 0 < selected < 5:
                 #print("confirmed")
                if _gesture["fingers_left"] != selected:  # Only reset if changed
                    _gesture["progress"] = 0
                _gesture["fingers_left"] = selected 
            elif selected == 0:
                _gesture["progress"] += 1
                if _gesture["progress"] >= 50:
                    print("confirmed")
                    _gesture["progress"] = 0


        gesture = getDirections()
        #print(gesture)

        cv2.imshow("Snake Gesture Capture", img)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
                stop()
                break


if __name__ == "__main__":
    setup()
    loopForGesture()


