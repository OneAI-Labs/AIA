from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)
CORS(app)

# Load Llama 3.2 Model & Tokenizer
MODEL_NAME = "meta-llama/Meta-Llama-3-2-3B"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Invalid request"}), 400

        # Tokenize input
        input_ids = tokenizer(user_message, return_tensors="pt").input_ids.to("cuda")

        # Generate response
        output = model.generate(input_ids, max_length=100)
        response = tokenizer.decode(output[0], skip_special_tokens=True)

        return jsonify({"reply": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)



