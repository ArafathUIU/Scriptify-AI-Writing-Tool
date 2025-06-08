from flask import Flask, render_template, request, jsonify
from app.style_improvement import improve_text
from app.paraphrasing import paraphrase_text
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Style improvement route
@app.route('/improve', methods=['POST'])
def improve():
    data = request.get_json()
    action = data.get('action')
    text = data.get('text')
    instruction = data.get('instruction', '').strip()

    # If user provides custom instruction, redirect to /custom-instruction logic
    if instruction:
        return custom_instruction_internal(text, instruction)

    improved_text = improve_text(text, action)
    return jsonify({'result': improved_text})

# Paraphrasing route
@app.route('/paraphrase', methods=['POST'])
def paraphrase():
    data = request.get_json()
    text = data.get('text')
    instruction = data.get('instruction', '').strip()

    # Paraphrasing also supports custom instruction
    if instruction:
        return custom_instruction_internal(text, instruction)

    paraphrased_text = paraphrase_text(text)
    return jsonify({'result': paraphrased_text})

# Grammar correction route
@app.route('/correct', methods=['POST'])
def correct():
    data = request.get_json()
    text = data.get('text')
    instruction = data.get('instruction', '').strip()

    if instruction:
        return custom_instruction_internal(text, instruction)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"Please correct grammar and spelling:\n{text}"}
            ],
            temperature=0.4
        )
        result = response.choices[0].message['content'].strip()
        return jsonify({'corrected': result})
    except Exception as e:
        return jsonify({'error': f"OpenAI API error: {str(e)}"}), 500

# Explicit custom instruction route
@app.route('/custom-instruction', methods=['POST'])
def custom_instruction():
    data = request.get_json()
    text = data.get('text')
    instruction = data.get('instruction')
    return custom_instruction_internal(text, instruction)

# Internal handler to avoid duplication
def custom_instruction_internal(text, instruction):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"{instruction}\n{text}"}
            ],
            temperature=0.7
        )
        result = response.choices[0].message['content'].strip()
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': f"OpenAI API error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
