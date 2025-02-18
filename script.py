from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "Invalid request"}), 400
    user_message = data["message"]
    ai_response = f"You said: {user_message}"  # Replace with real AI response logic
    return jsonify({"reply": ai_response})

if __name__ == "__main__":
    app.run(debug=True)

