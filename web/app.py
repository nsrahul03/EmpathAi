from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64
from PIL import Image
import io
import tensorflow as tf

app = Flask(__name__)

# Load trained emotion models
MODEL_PATH = "fer2013_best_model.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# Emotion labels
EMOTIONS = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]

# OpenCV Haar Cascade for face detection
FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data or "image" not in data:
            return jsonify({"error": "No image received"}), 400

        # Remove base64 header
        image_data = data["image"].split(",")[1]

        # Decode base64 image
        image_bytes = base64.b64decode(image_data)

        # Convert image to OpenCV format
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        frame = np.array(image)

        # Convert RGB to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Detect faces
        faces = FACE_CASCADE.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(60, 60)
        )

        # No face detected
        if len(faces) == 0:
            return jsonify({
                "face_detected": False,
                "emotion": "No face detected",
                "confidence": 0
            })

        # Select the largest face
        largest_face = max(
            faces,
            key=lambda rect: rect[2] * rect[3]
        )

        x, y, w, h = largest_face

        # Crop only the detected face
        face = gray[y:y + h, x:x + w]

        # Resize to CNN input size
        face = cv2.resize(face, (48, 48))

        # Normalize pixel values
        face = face.astype("float32") / 255.0

        # Reshape for CNN
        face = np.expand_dims(face, axis=0)
        face = np.expand_dims(face, axis=-1)

        # Predict emotion
        predictions = model.predict(face, verbose=0)

        emotion_index = np.argmax(predictions[0])
        emotion = EMOTIONS[emotion_index]
        confidence = float(predictions[0][emotion_index]) * 100

        return jsonify({
            "face_detected": True,
            "emotion": emotion,
            "confidence": round(confidence, 2),
            "face": {
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h)
            }
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
