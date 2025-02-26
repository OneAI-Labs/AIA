from google.cloud import firestore
import json
from collections import Counter

db = firestore.Client()
chat_collection = db.collection("chat_history")

def analyze_feedback():
    print("\n🔥 Analyzing feedback ratings from Firestore...\n")
    
    feedback_counts = Counter()
    training_data = []  # ✅ New list to store good training data

    docs = chat_collection.stream()
    for doc in docs:
        data = doc.to_dict()
        feedback = data.get("user_feedback")
        ai_response = data.get("ai_response", "N/A")
        user_message = data.get("user_message", "N/A")
        
        if feedback == 2:  # ✅ Only take highly-rated responses
            training_data.append({"input": user_message, "output": ai_response})
    
    # ✅ Save training data for fine-tuning
    with open("train_data.json", "w", encoding="utf-8") as f:
        json.dump(training_data, f, indent=4)

    print(f"📂 Saved {len(training_data)} high-rated responses to 'train_data.json' for fine-tuning.")

if __name__ == "__main__":
    analyze_feedback()


