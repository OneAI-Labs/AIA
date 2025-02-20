from google.cloud import firestore
from collections import Counter

db = firestore.Client()
chat_collection = db.collection("chat_history")

def analyze_feedback():
    print("\n🔥 Analyzing feedback ratings from Firestore...\n")
    
    feedback_counts = Counter()
    bad_responses = []
    neutral_responses = []
    good_responses = []
    
    docs = chat_collection.stream()
    for doc in docs:
        data = doc.to_dict()
        feedback = data.get("user_feedback")
        ai_response = data.get("ai_response", "N/A")
        user_message = data.get("user_message", "N/A")
        
        if feedback is not None:
            feedback_counts[feedback] += 1
            if feedback == 0:
                bad_responses.append((user_message, ai_response))
            elif feedback == 1:
                neutral_responses.append((user_message, ai_response))
            elif feedback == 2:
                good_responses.append((user_message, ai_response))
    
    # Summary of feedback
    print(f"✅ Feedback Summary:")
    print(f"   👍 Good (2): {feedback_counts[2]}")
    print(f"   ➖ Neutral (1): {feedback_counts[1]}")
    print(f"   👎 Bad (0): {feedback_counts[0]}\n")
    
    # Show examples of bad responses for improvement
    if bad_responses:
        print("🚨 Examples of bad responses:")
        for user_msg, ai_resp in bad_responses[:5]:
            print(f"User: {user_msg}\nAI: {ai_resp}\n")
    
    if neutral_responses:
        print("🟡 Examples of neutral responses:")
        for user_msg, ai_resp in neutral_responses[:5]:
            print(f"User: {user_msg}\nAI: {ai_resp}\n")
    
    if good_responses:
        print("✅ Examples of good responses:")
        for user_msg, ai_resp in good_responses[:5]:
            print(f"User: {user_msg}\nAI: {ai_resp}\n")
    
    print("🚀 Analysis complete! Use this data to refine AI responses.")

if __name__ == "__main__":
    analyze_feedback()