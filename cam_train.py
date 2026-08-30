import cv2
import os
import time

# Change this to your emotions
emotions = ["angry","disgust","fear", "happy","sad","surprise","neutral"]

# Select emotion you want to collect
current_emotion = "sad"   # Change manually when collecting

save_path = f"my_data/{current_emotion}"
os.makedirs(save_path, exist_ok=True)

cap = cv2.VideoCapture(0)

img_count = 0

print("Press 's' to save image")
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale (if your model uses grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize to match model input
    resized = cv2.resize(gray, (48, 48))

    cv2.putText(frame, f"Collecting: {current_emotion}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    cv2.imshow("Data Collection", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        filename = os.path.join(save_path, f"{current_emotion}_{int(time.time())}.jpg")
        cv2.imwrite(filename, resized)
        img_count += 1
        print(f"Saved {img_count}")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
