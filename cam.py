# ==============================
# cam.py
# Handles webcam + emotion detection
# ==============================

import cv2
import numpy as np
import threading
import time
import os
from tensorflow.keras.models import load_model

# ------------------------------
# Load trained emotion model
# ------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Change this if your model name is different
MODEL_PATH = os.path.join(BASE_DIR, "fer2013_best_model.keras")

model = load_model(MODEL_PATH, compile=False)

# Emotion labels (same order as training)
emotion_labels = [
    "Angry", "Disgust", "Fear",
    "Happy", "Sad", "Surprise", "Neutral"
]

# Global variable to store current emotion
current_emotion = "Neutral"

# ------------------------------
# Start camera in background
# ------------------------------

def start_camera():
    """
    Starts emotion detection in a separate thread
    so main program doesn't block.
    """
    thread = threading.Thread(target=emotion_loop, daemon=True)
    thread.start()

# ------------------------------
# Emotion detection loop
# ------------------------------

def emotion_loop():
    global current_emotion

    # Open webcam (0 = default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return

    print("📷 Camera started (background)...")

    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        # Convert to grayscale (model expects grayscale)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Resize to 48x48 (model input size)
        face = cv2.resize(gray, (48, 48))

        # Normalize pixel values
        face = face / 255.0

        # Reshape for model → (1, 48, 48, 1)
        face = np.reshape(face, (1, 48, 48, 1))

        # Predict emotion
        predictions = model.predict(face, verbose=0)

        # Get highest probability index
        emotion_index = np.argmax(predictions)

        # Update global emotion
        current_emotion = emotion_labels[emotion_index]

        # Small delay to reduce CPU usage
        time.sleep(0.3)

# ------------------------------
# Get current emotion
# ------------------------------

def get_emotion():
    """
    Returns the latest detected emotion
    """
    return current_emotion