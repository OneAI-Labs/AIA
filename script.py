from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)  
CORS(app)  # Enable CORS for all routes

@app.route("/")
def home():
    return "Hello, Flask is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "Error: No message received"}), 400

    # AI response simulation (Replace this with your OpenAI API call)
    ai_response = f"AI response to: {user_message}"
    
    return jsonify({"reply": ai_response})

if __name__ == "__main__":
    app.run(debug=True)

