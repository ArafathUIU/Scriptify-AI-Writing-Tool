from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from app.grammar_correction import correct_grammar
from app.style_improvement import improve_text 

app = Flask(__name__)
CORS(app)  # Optional, allows cross-origin requests if needed

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/correct", methods=["POST"])
def correct():
    try:
        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No input text provided."}), 400
        corrected_text = correct_grammar(text)
        return jsonify({"corrected": corrected_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/improve", methods=["POST"])
def improve():
    try:
        data = request.get_json()
        text = data.get("text", "")
        action = data.get("action", "")
        if not text or not action:
            return jsonify({"error": "Text and action are required."}), 400
        improved_text = improve_text(text, action)
        return jsonify({"result": improved_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
