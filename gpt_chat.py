# ==============================
# gpt_chat.py
# Handles GPT responses
# ==============================

import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(user_input, emotion):
    """
    Generates AI response based on user input + emotion
    """

    # Build smart emotional prompt
    prompt = f"""
    The user is feeling {emotion}.
    Respond in a helpful, human, and emotionally intelligent way.

    User: {user_input}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # fast + cheap model
            messages=[
                {"role": "system", "content": "You are a smart emotional AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {str(e)}"