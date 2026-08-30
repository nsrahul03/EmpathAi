# ==========================================
# train_model.py
# ------------------------------------------
# Trains emotion detection model using:
# - FER2013 dataset
# - Custom webcam dataset
# Saves best model in .keras format
# ==========================================

import os
import cv2
import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# =====================================
# 1️⃣ LOAD FER2013 DATASET
# =====================================

print("📥 Loading FER2013 dataset...")

data = pd.read_csv("fer2013.csv")

pixels = data["pixels"].tolist()

X_fer = []

for pixel_sequence in pixels:
    # Convert string → array
    face = np.fromstring(pixel_sequence, dtype=int, sep=" ")

    # Reshape to image
    face = face.reshape(48, 48)

    # Normalize (0–1)
    face = face / 255.0

    X_fer.append(face)

X_fer = np.array(X_fer)
X_fer = X_fer.reshape(-1, 48, 48, 1)

# One-hot labels
y_fer = tf.keras.utils.to_categorical(data["emotion"], 7)

print("✅ FER2013 loaded")

# =====================================
# 2️⃣ LOAD CUSTOM DATASET
# =====================================

print("📷 Loading webcam dataset...")

dataset_path = "my_data"

emotion_map = {
    "angry":0,
    "disgust":1,
    "fear":2,
    "happy":3,
    "sad":4,
    "surprise":5,
    "neutral":6
}

X_webcam = []
y_webcam = []

for emotion_folder in os.listdir(dataset_path):

    folder_path = os.path.join(dataset_path, emotion_folder)

    if emotion_folder not in emotion_map:
        continue

    label = emotion_map[emotion_folder]

    for img_name in os.listdir(folder_path):

        img_path = os.path.join(folder_path, img_name)

        img = cv2.imread(img_path)

        if img is None:
            continue

        # Convert → grayscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Resize → 48x48
        img = cv2.resize(img, (48, 48))

        # Normalize
        img = img / 255.0

        X_webcam.append(img)
        y_webcam.append(label)

X_webcam = np.array(X_webcam).reshape(-1,48,48,1)
y_webcam = tf.keras.utils.to_categorical(y_webcam,7)

print("✅ Webcam dataset loaded")

# =====================================
# 3️⃣ COMBINE DATA
# =====================================

print("🔗 Combining datasets...")

X = np.concatenate((X_fer, X_webcam), axis=0)
y = np.concatenate((y_fer, y_webcam), axis=0)

print("📊 Total samples:", X.shape[0])

# =====================================
# 4️⃣ TRAIN/VALIDATION SPLIT
# =====================================

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =====================================
# 5️⃣ MODEL ARCHITECTURE
# =====================================

print("🧠 Building CNN model...")

model = Sequential([

    Conv2D(32,(3,3),activation="relu",input_shape=(48,48,1)),
    BatchNormalization(),
    MaxPooling2D(2,2),
    Dropout(0.25),

    Conv2D(64,(3,3),activation="relu"),
    BatchNormalization(),
    MaxPooling2D(2,2),
    Dropout(0.25),

    Conv2D(128,(3,3),activation="relu"),
    BatchNormalization(),
    MaxPooling2D(2,2),
    Dropout(0.25),

    Flatten(),

    Dense(256,activation="relu"),
    Dropout(0.5),

    Dense(7,activation="softmax")
])

# Compile model
model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# =====================================
# 6️⃣ CALLBACKS
# =====================================

early_stop = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=10,
    restore_best_weights=True
)

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    "best_emotion_model.keras",
    monitor="val_accuracy",
    save_best_only=True
)

# =====================================
# 7️⃣ TRAIN
# =====================================

print("🚀 Training started...")

history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=60,
    batch_size=64,
    callbacks=[early_stop, checkpoint]
)

# =====================================
# 8️⃣ SAVE FINAL MODEL
# =====================================

model.save("final_emotion_model.keras")

print("🎉 Training complete!")