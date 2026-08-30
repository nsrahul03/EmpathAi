# -----------------------------------------------------------
# IMPORT LIBRARIES
# -----------------------------------------------------------

import cv2
import numpy as np
from tensorflow.keras.models import load_model
from collections import deque


# -----------------------------------------------------------
# LOAD TRAINED MODEL
# -----------------------------------------------------------

model = load_model("fer2013_best_model.keras")


# Emotion labels
emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]


# -----------------------------------------------------------
# LOAD FACE DETECTOR
# -----------------------------------------------------------

face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# -----------------------------------------------------------
# START WEBCAM
# -----------------------------------------------------------

cap = cv2.VideoCapture(0)

print("Webcam started. Press 'q' to quit.")


# -----------------------------------------------------------
# SMOOTHING BUFFER
# -----------------------------------------------------------

prediction_buffer = deque(maxlen=7)


# -----------------------------------------------------------
# STABILITY VARIABLES
# -----------------------------------------------------------

current_emotion = "Neutral"
candidate_emotion = None
candidate_count = 0


CONF_THRESHOLD = 0.40
DRASTIC_THRESHOLD = 0.70
STABLE_FRAMES = 2


# -----------------------------------------------------------
# MAIN LOOP
# -----------------------------------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # -------------------------------------------------------
    # DETECT FACES
    # -------------------------------------------------------

    faces = face_classifier.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )


    # -------------------------------------------------------
    # SELECT LARGEST FACE (MAIN PERSON)
    # -------------------------------------------------------

    if len(faces) > 0:

        # Find the largest face (width * height)
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])

        x, y, w, h = largest_face


        # ---------------------------------------------------
        # EXTRACT FACE REGION
        # ---------------------------------------------------

        roi_gray = gray[y:y+h, x:x+w]

        roi_gray = cv2.resize(roi_gray, (48, 48))

        roi_gray = roi_gray / 255.0

        roi_gray = np.reshape(roi_gray, (1, 48, 48, 1))


        # ---------------------------------------------------
        # MODEL PREDICTION
        # ---------------------------------------------------

        prediction = model.predict(roi_gray, verbose=0)

        prediction_buffer.append(prediction)

        avg_prediction = np.mean(prediction_buffer, axis=0)

        max_index = np.argmax(avg_prediction)

        confidence = avg_prediction[0][max_index]

        predicted_emotion = emotion_labels[max_index]


        # ---------------------------------------------------
        # STABLE PREDICTION LOGIC
        # ---------------------------------------------------

        if confidence > DRASTIC_THRESHOLD:

            current_emotion = predicted_emotion
            candidate_count = 0

        elif confidence > CONF_THRESHOLD:

            if predicted_emotion == candidate_emotion:

                candidate_count += 1

            else:

                candidate_emotion = predicted_emotion
                candidate_count = 1

            if candidate_count >= STABLE_FRAMES:

                current_emotion = candidate_emotion


        # ---------------------------------------------------
        # DRAW FACE BOX
        # ---------------------------------------------------

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )


        # ---------------------------------------------------
        # DISPLAY EMOTION
        # ---------------------------------------------------

        text = f"{current_emotion} ({confidence:.2f})"

        cv2.putText(
            frame,
            text,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )


    # -------------------------------------------------------
    # SHOW WINDOW
    # -------------------------------------------------------

    cv2.imshow("Emotion Detection (Main Person)", frame)


    # Exit when 'q' pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# -----------------------------------------------------------
# CLEANUP
# -----------------------------------------------------------

cap.release()
cv2.destroyAllWindows()