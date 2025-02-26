from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
from google.cloud import firestore

app = Flask(__name__)
CORS(app)

# Load Hugging Face API token
hf_token = os.getenv("HUGGINGFACE_TOKEN")
if not hf_token:
    raise ValueError("Hugging Face API token is missing. Please set HUGGINGFACE_TOKEN in your environment.")

# ✅ Initialize Firestore
db = firestore.Client()
chat_collection = db.collection("chat_history")

# Load Llama Model & Tokenizer
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=hf_token)
    tokenizer.pad_token = tokenizer.eos_token  

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        token=hf_token, 
        torch_dtype=torch.float16, 
        device_map="auto"
    )
    model.eval()  
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    model = None  

# ✅ API Status Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "API is running!"}), 200

# ✅ Chat Route - Store Conversations in Firestore
@app.route("/chat", methods=["POST"])
def chat():
    try:
        if model is None:
            return jsonify({"error": "Model failed to load."}), 500

        data = request.json
        if not data or "message" not in data:
            return jsonify({"error": "Invalid request. Missing 'message' field."}), 400

        user_message = data["message"].strip()
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # ✅ Fetch Last 3 Messages from Firestore (Memory)
        past_chats = chat_collection.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(3).stream()
        chat_history = "\n".join([
            f"User: {chat.to_dict().get('user_message', '')}\nAI: {chat.to_dict().get('ai_response', '')}"
            for chat in past_chats
        ])

        # ✅ AI System Prompt (More Conversational)
        system_prompt = (
            "You are a highly intelligent and articulate AI assistant named AI-A, trained to engage in human-like conversations. "
            "Your responses should be clear, thoughtful, and contextually relevant. "
            "Maintain a friendly and conversational tone, and provide informative and engaging replies. "
            "If the user greets you, respond naturally. If they ask a question, provide a helpful answer. "
            "If the message is unclear, politely ask for clarification."
        )

        # ✅ Combine Memory and User Message
        formatted_prompt = f"{system_prompt}\n\n{chat_history}\nUser: {user_message}\nAI:"

        encoded_input = tokenizer(
            formatted_prompt, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=512  # ✅ Increased length for better context
        ).to(device)

        # ✅ Adjusted Generation Parameters for Conversational Flow
        with torch.no_grad():
            output = model.generate(
                input_ids=encoded_input["input_ids"],
                attention_mask=encoded_input["attention_mask"],
                max_length=150,  # ✅ Increased response length
                do_sample=True,
                temperature=0.7,  # ✅ Reduce randomness for better coherence
                top_p=0.92,  # ✅ Keeps responses logical but varied
                repetition_penalty=1.1,  # ✅ Reduce repeated words
                num_return_sequences=1,  
                early_stopping=True
            )

        response_text = tokenizer.decode(output[0], skip_special_tokens=True).strip()

        # ✅ Clean AI response
        if "AI:" in response_text:
            response_text = response_text.split("AI:")[-1].strip()

        # ✅ Store AI response in Firestore
        chat_doc = chat_collection.document()
        chat_doc.set({
            "user_message": user_message,
            "ai_response": response_text,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

        return jsonify({"reply": response_text, "chat_id": chat_doc.id})  

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Fetch Past Chats Route for Frontend
@app.route("/chat-history", methods=["GET"])
def chat_history():
    try:
        chats = chat_collection.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(20).stream()

        history = []
        for chat in chats:
            chat_data = chat.to_dict()
            history.append({
                "chat_id": chat.id,
                "user_message": chat_data.get("user_message", ""),
                "ai_response": chat_data.get("ai_response", ""),
                "timestamp": chat_data.get("timestamp")
            })

        return jsonify({"chat_history": history})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ New Route for Storing User Feedback
@app.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = request.json
        chat_id = data.get("chat_id")
        rating = data.get("rating")  # 👍 2 (good) / ➖ 1 (neutral) / 👎 0 (bad)

        if not chat_id or rating not in [0, 1, 2]:
            return jsonify({"error": "Invalid request. Provide 'chat_id' and 'rating' (0, 1, or 2)."}), 400

        # ✅ Store feedback in Firestore
        chat_doc = chat_collection.document(chat_id)
        chat_doc.update({"user_feedback": rating})

        return jsonify({"message": "Feedback saved successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
