from flask import Flask, render_template, request, jsonify
from app.grammar_correction import correct_grammar

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/correct", methods=["POST"])
def correct():
    try:
        data = request.get_json()
        text = data.get("text", "")
        corrected_text = correct_grammar(text)
        return jsonify({"corrected": corrected_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
