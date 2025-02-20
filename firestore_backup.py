import os
import json
from google.cloud import firestore
from google.oauth2 import service_account

# 🔥 Path to Firestore credentials
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "firestore_credentials.json")

# 🔥 Path to local backup folder INSIDE `AIA`
BACKUP_FOLDER = os.path.join(os.path.dirname(__file__), "firestore_backup")

# ✅ Ensure backup folder exists
os.makedirs(BACKUP_FOLDER, exist_ok=True)

# ✅ Authenticate Firestore client
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
db = firestore.Client(credentials=credentials)

# 🔄 Function to fetch all Firestore collections & save locally
def backup_firestore():
    collections = db.collections()
    
    for collection in collections:
        collection_name = collection.id
        docs = collection.stream()

        data = {doc.id: doc.to_dict() for doc in docs}

        # ✅ Save to JSON file inside `AIA/firestore_backup/`
        file_path = os.path.join(BACKUP_FOLDER, f"{collection_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        print(f"✅ Backed up: {collection_name} -> {file_path}")

# 🚀 Run backup
if __name__ == "__main__":
    print("🔥 Starting Firestore backup...")
    backup_firestore()
    print("✅ Backup completed successfully!")

