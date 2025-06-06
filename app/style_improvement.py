# app/style_improvement.py
from dotenv import load_dotenv
import os
import openai

load_dotenv()  # loads variables from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def improve_text(text, action):
    prompt_map = {
        "formal": f"Make this text more formal:\n{text}",
        "concise": f"Make this text more concise:\n{text}",
        "vocabulary": f"Improve the vocabulary of the following text:\n{text}"
    }

    prompt = prompt_map.get(action, text)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Error improving text: {e}"
