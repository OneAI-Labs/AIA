from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()
chat_collection = db.collection("chat_history")

def update_feedback_ratings():
    print("🔥 Updating feedback ratings in Firestore...")

    # Fetch all chat documents
    docs = chat_collection.stream()

    for doc in docs:
        data = doc.to_dict()
        feedback = data.get("user_feedback")

        # Skip if there's no feedback
        if feedback is None:
            continue

        # Convert old ratings to new scale
        new_rating = None
        if feedback == 1:
            new_rating = 2  # Good
        elif feedback == 0:
            new_rating = 0  # Bad
        elif feedback == 2:
            new_rating = 1  # Neutral

        if new_rating is not None:
            chat_collection.document(doc.id).update({"user_feedback": new_rating})
            print(f"✅ Updated {doc.id}: {feedback} -> {new_rating}")

    print("🚀 All feedback ratings updated successfully!")

if __name__ == "__main__":
    update_feedback_ratings()
