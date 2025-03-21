import firebase_admin
from firebase_admin import credentials, firestore
import datetime


cred = credentials.Certificate("path/to/your/serviceAccountKey.json") #
firebase_admin.initialize_app(cred)

db = firestore.client()  

def add_user(user_id, name, email, phone, age):
    user_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "age": age,
        "created_at": datetime.utcnow()  # Store timestamp
    }

    db.collection("users").document(user_id).set(user_data)
    print(f"User {name} added successfully!")


add_user("user_123", "Alice Doe", "alice@example.com", "+1234567890", 25)    
    
def store_data(user_id, data):
    db.collection("users").document(user_id).update({"data": data})
    print(f"Data for user {user_id} updated successfully!")
    
    
def update_user(user_id, update_data):
    doc_ref = db.collection("users").document(user_id)
    doc_ref.update(update_data)
    print("User data updated successfully!")


update_user("user_123", {"age": 26})
