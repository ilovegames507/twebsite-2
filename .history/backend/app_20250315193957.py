from flask import Flask, jsonify
from flask_cors import CORS
import os
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
CORS(app)  # Allow all origins

@app.route('/')
def home():
    return "Hello, world!"

@app.route('/members')
def members():
    return jsonify({"members": ["Alice", "Bob", "Charlie"]})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to 5000
    app.run(host="0.0.0.0", port=port)

