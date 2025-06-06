# app/paraphraser.py
import openai
import os

def paraphrase_text(text):
    prompt =  (
    f"Please rewrite the following sentence to make it more natural, fluent, and clear, "
    f"while preserving the original meaning. Use everyday, native-level English:\n\n"
    f"Original: \"{text}\"\n\n"
    f"Paraphrased:"
)
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    return response.choices[0].message["content"].strip()
