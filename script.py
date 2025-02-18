import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("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")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400

    user_message = data["message"]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Change to the correct model you're using
            messages=[{"role": "user", "content": user_message}]
        )
        ai_response = response["choices"][0]["message"]["content"]
    except Exception as e:
        return jsonify({"error": f"Error calling OpenAI API: {str(e)}"}), 500

    return jsonify({"reply": ai_response})

if __name__ == "__main__":
    app.run(debug=True)

