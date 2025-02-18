import os
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
openai.api_key = os.getenv("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")

app = Flask(__name__)  
CORS(app)  # Enable CORS for frontend communication

@app.route("/")
def home():
    return "Hello, Flask is running with OpenAI!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "Error: No message received"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" if your plan allows
            messages=[{"role": "user", "content": user_message}],
            max_tokens=100
        )
        ai_reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error calling OpenAI API:", e)
        ai_reply = "Sorry, I couldn't process your request."

    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
    app.run(debug=True)


