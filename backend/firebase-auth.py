import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, request, jsonify
from flask_cors import CORS  
import requests  

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  


cred = credentials.Certificate("serviceAccountKey.json")  
firebase_admin.initialize_app(cred)


config = {
    "apiKey": "AIzaSyD1Ys1GB31nGOvNi9SC38n30MORxZzc10s",
    "authDomain": "your-project.firebaseapp.com",
    "databaseURL": "https://your-project-default-rtdb.firebaseio.com/",
    "storageBucket": "your-project.appspot.com",
    "messagingSenderId": "your-messaging-id",
    "appId": "your-app-id",
}

firebase = pyrebase.initialize_app(config)
pyre_auth = firebase.auth()  
db = firebase.database()  

def login():
    """Logs in a user with email and password."""
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        user = pyre_auth.sign_in_with_email_and_password(email, password)
        print("Login successful!")
        
        user_data = db.child("users").child(user['localId']).get().val()
        print("Welcome,", user_data["email"])
    except requests.exceptions.HTTPError as e:  
        error_message = e.response.json()
        print("Error logging in:", error_message)
        ans = input("Do you want to sign up instead? (yes/no): ")
        if ans.lower() == "yes":
            signup()

def send_verification_email(user):
    """Sends email verification to the user."""
    pyre_auth.send_email_verification(user['idToken'])
    print("A verification email has been sent. Please check your inbox.")

def signup():
    """Signs up a new user and saves data to Firebase Database."""
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    try:
        user = pyre_auth.create_user_with_email_and_password(email, password)
        print("User created successfully!")

     
        user_data = {
            "email": email,
            "uid": user['localId']
        }
        db.child("users").child(user['localId']).set(user_data)
        print("User data saved to Firebase Database.")
        send_verification_email(user)
    except requests.exceptions.HTTPError as e:  
        error_message = e.response.json()
        print("Error creating user:", error_message)

def user_exists(email):
    """Checks if a user already exists in the Firebase Database."""
    users = db.child("users").get()
    if users.each():
        for user in users.each():
            if user.val()["email"] == email:
                return True
    return False

@app.route("/google-login", methods=["POST"])
def google_login():
    """Verifies Google ID Token sent from frontend and logs in the user."""
    try:
        data = request.json
        print("Received Data:", data)  
        id_token = data.get("token")  
        if not id_token:
            return jsonify({"error": "Missing token"}), 400

        decoded_token = auth.verify_id_token(id_token)  
        uid = decoded_token["uid"]
        email = decoded_token.get("email", "Unknown Email")

        return jsonify({"message": "User authenticated", "uid": uid, "email": email})
    except Exception as e:
        print("Error:", str(e))  
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(debug=True, port=5001)  