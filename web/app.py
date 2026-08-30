from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import base64
import io
import os


app = Flask(__name__)

# --------------------------------------------------
# Model configuration
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "fer2013_best_model.keras"
)

model = load_model(MODEL_PATH, compile=False)

EMOTIONS = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        image_data = data["image"]

        # Remove the base64 header
        image_data = image_data.split(",", 1)[1]

        # Decode image
        image_bytes = base64.b64decode(image_data)

        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("L")

        # Resize to FER2013 model input
        image = image.resize((48, 48))

        # Convert to NumPy array
        image_array = np.array(image, dtype=np.float32)

        # Normalize
        image_array = image_array / 255.0

        # Model expects:
        # (batch, height, width, channels)
        image_array = image_array.reshape(
            1, 48, 48, 1
        )

        # Prediction
        predictions = model.predict(
            image_array,
            verbose=0
        )

        emotion_index = int(
            np.argmax(predictions[0])
        )

        emotion = EMOTIONS[emotion_index]

        confidence = float(
            predictions[0][emotion_index]
        )

        return jsonify({
            "emotion": emotion,
            "confidence": round(
                confidence * 100,
                2
            )
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# --------------------------------------------------
# Run application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )

