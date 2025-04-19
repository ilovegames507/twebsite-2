from flask import Flask, jsonify
from flask_cors import CORS
import os
from authlib.integrations.flask_client import OAuth
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("your-service-account-key.json")  # Path to your service account key
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

app = Flask(__name__)
CORS(app)  # Allow all origins

@app.route('/')
def home():
    return "Hello, world!"

@app.route('/members')
def members():
    return jsonify({"members": ["Alice", "Bob", "Charlie"]})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))  # Default to 5001 if no environment variable is set
    app.run(host="0.0.0.0", port=port)
