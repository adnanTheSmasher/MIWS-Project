import cv2
import HandTrackingModule as htm
import time
import csv
import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ========================================================
# GLOBALS
# ========================================================
_cap = None
_running = True
_detector = None
model = None
current_direction = -1

MODE = "collect"  # collect / play

DATA_FILE = "gesture_data.csv"
MODEL_FILE = "gesture_model.pkl"

RIGHT = "Right"

last_gesture = None
stable_count = 0

# ========================================================
# SETUP
# ========================================================
def setup():
    global _cap, _detector
    _cap = cv2.VideoCapture(0)
    _cap.set(3, 600)
    _cap.set(4, 300)
    _detector = htm.handDetector(maxHands=1, detectionCon=0.85)

def stop():
    global _cap, _running
    _running = False
    if _cap:
        _cap.release()
    cv2.destroyAllWindows()

# ========================================================
# DATA COLLECTION
# ========================================================
def save_to_csv(label, lmList):
    base_x, base_y = lmList[0][1], lmList[0][2]

    row = []
    for lm in lmList:
        row.extend([lm[1] - base_x, lm[2] - base_y])

    row.append(label)

    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print(f"Saved: {label}")

# ========================================================
# TRAIN MODEL (RANDOM FOREST)
# ========================================================
def train_model():
    global model

    if not os.path.exists(DATA_FILE):
        print("No data found!")
        return

    data = pd.read_csv(DATA_FILE, header=None)

    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=20,
        random_state=42
    )

    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)
    print("Model trained. Accuracy:", acc)

    joblib.dump(model, MODEL_FILE)

# ========================================================
# LOAD MODEL
# ========================================================
def load_model():
    global model
    if os.path.exists(MODEL_FILE):
        model = joblib.load(MODEL_FILE)
        print("Model Loaded!")
    else:
        print("No trained model found!")

# ========================================================
# PREDICT WITH CONFIDENCE
# ========================================================
def predict(lmList):
    global model

    if lmList is None or len(lmList) == 0:
        return "UNKNOWN"
    if model is None:
        return "UNKNOWN"

    base_x, base_y = lmList[0][1], lmList[0][2]

    row = []
    for lm in lmList:
        row.extend([lm[1] - base_x, lm[2] - base_y])

    probs = model.predict_proba([row])[0]
    max_prob = max(probs)
    prediction = model.classes_[probs.argmax()]

    if max_prob < 0.6:
        return "UNKNOWN"

    return prediction

def getPrediction():
    global current_direction
    return current_direction


# ========================================================
# MAIN LOOP
# ========================================================
def loop():
    global MODE, last_gesture, stable_count, current_direction

    load_model()

    while _running:
        success, img = _cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        img = _detector.findHands(img, draw=True)
        lmList, _ = _detector.findPosition(img, draw=False)

        key = cv2.waitKey(1) & 0xFF

        # =======================
        # COLLECT MODE
        # =======================
        if MODE == "collect" and lmList:
            if key == ord('u'):
                save_to_csv("UP", lmList)
            elif key == ord('d'):
                save_to_csv("DOWN", lmList)
            elif key == ord('l'):
                save_to_csv("LEFT", lmList)
            elif key == ord('r'):
                save_to_csv("RIGHT", lmList)
            elif key == ord("z"):
                save_to_csv("SELECT", lmList)
            elif key == ord("o"):
                save_to_csv("PAUSE", lmList)
            elif key == ord("x"):
                save_to_csv("OPTION 1", lmList)
            elif key == ord("e"):
                save_to_csv("OPTION 2", lmList)

            elif key == ord('t'):
                print("Training Model...")
                train_model()

            elif key == ord('p'):
                print("Switching to PLAY mode")
                load_model()
                MODE = "play"

        # =======================
        # PLAY MODE
        # =======================
        elif MODE == "play" and lmList and model is not None:
            gesture = predict(lmList)

            if gesture == last_gesture:
                stable_count += 1
            else:
                stable_count = 0

            if stable_count > 3:
                if gesture == "UP":
                    current_direction = "UP"
                elif gesture == "RIGHT":
                    current_direction = "RIGHT"
                elif gesture == "DOWN":
                    current_direction = "DOWN"
                elif gesture == "LEFT":
                    current_direction = "LEFT"
                elif gesture == "SELECT":
                    current_direction = "SELECT"
                elif gesture == "PAUSE":
                    current_direction = "PAUSE"
                elif gesture == "OPTION 1":
                    current_direction = "OPTION 1"
                elif gesture == "OPTION 2":
                    current_direction = "OPTION 2"
                else:
                    current_direction = -1

            last_gesture = gesture
            print("Gesture:", gesture, " | Final:", current_direction)
            cv2.putText(img, f"Gesture: {gesture}", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (255, 255, 0), 2)
        # =======================
        # UI
        # =======================
        cv2.putText(img, f"MODE: {MODE}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)

        cv2.imshow("Gesture AI - Random Forest", img)

        if key == ord('q'):
            stop()
            break

# ========================================================
# RUN
# ========================================================
if __name__ == "__main__":
    setup()
    loop()