from flask import Flask, request, jsonify 
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

app = Flask(__name__)
CORS(app)

# Load Hugging Face API token from environment variables
hf_token = os.getenv("HUGGINGFACE_TOKEN")

if not hf_token:
    raise ValueError("Hugging Face API token is missing. Please set HUGGINGFACE_TOKEN in Render.")

# Load Llama 3.2 Model & Tokenizer with authentication
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=hf_token)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, 
    token=hf_token, 
    torch_dtype=torch.float16, 
    device_map="auto"
)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Invalid request"}), 400

        # Move input to correct device (CPU/GPU)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        input_ids = tokenizer(user_message, return_tensors="pt").input_ids.to(device)

        # Generate response
        output = model.generate(input_ids, max_length=100)
        response = tokenizer.decode(output[0], skip_special_tokens=True)

        return jsonify({"reply": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
