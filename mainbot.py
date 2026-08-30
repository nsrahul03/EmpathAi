
# Main program (runs everything)

from cam import start_camera, get_emotion
from gpt_chatoffline import generate_response

# ------------------------------
# Start system
# ------------------------------

print("🚀 Empath AI Running...\n")

# Start camera in background
start_camera()

# ------------------------------
# Chat loop
# ------------------------------

while True:
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    # Get current detected emotion
    emotion = get_emotion()

    print(f"🧠 Detected Emotion: {emotion}")

    # Generate AI response
    reply = generate_response(user_input, emotion)

    print(f"🤖 AI: {reply}\n")