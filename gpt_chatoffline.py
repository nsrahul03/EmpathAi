import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"

def generate_response(user_input, emotion):

    prompt = f"""
    You are an empathetic AI assistant.

    User emotion: {emotion}

    Respond accordingly:
    - Sad → comfort
    - Happy → match energy
    - Angry → calm
    - Neutral → friendly

    User: {user_input}
    """

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False   # 🔥 THIS FIXES YOUR ERROR
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data["message"]["content"]
        else:
            return f"⚠️ Error: {response.text}"

    except Exception as e:
        return f"⚠️ Connection Error: {e}"