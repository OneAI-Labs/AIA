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
    raise ValueError("Hugging Face API token is missing. Please set HUGGINGFACE_TOKEN in your environment.")

# Load Llama 3.2 Model & Tokenizer with authentication
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=hf_token)
    tokenizer.pad_token = tokenizer.eos_token  # ✅ Set PAD token to EOS token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        token=hf_token, 
        torch_dtype=torch.float16, 
        device_map="auto"
    )
    model.eval()  # Set the model to evaluation mode
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
except Exception as e:
    print(f"⚠️ Error loading model: {e}")
    model = None  # Prevent server crash if model fails to load

# ✅ API Status Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "API is running!"}), 200

# ✅ Chat Route with Correct Formatting
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

        # ✅ Correct Chat Formatting: Instruction + User Prompt
        formatted_prompt = f"User: {user_message}\nAI:"

        # Tokenize input properly
        encoded_input = tokenizer(
            formatted_prompt, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=256
        ).to(device)

        # Generate response with proper stopping conditions
        with torch.no_grad():
            output = model.generate(
                input_ids=encoded_input["input_ids"],
                attention_mask=encoded_input["attention_mask"],
                max_length=100,  
                do_sample=True,
                temperature=0.7,
                top_p=0.8,
                early_stopping=True
            )

        # ✅ Remove everything before "AI:" so it doesn’t repeat itself
        response_text = tokenizer.decode(output[0], skip_special_tokens=True)
        if "AI:" in response_text:
            response_text = response_text.split("AI:")[-1].strip()

        return jsonify({"reply": response_text})  # ✅ Clean output

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)




