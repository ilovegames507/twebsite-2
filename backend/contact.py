from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import firebase_admin
from firebase_admin import credentials, messaging
import re
import phonenumbers
from phonenumbers import NumberParseException

app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'spainproject23@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = ("Marcelin's Auto Repair", 'spainproject23@gmail.com')
app.config['MAIL_PASSWORD'] = 'Tangie07!'
mail = Mail(app)

cred = credentials.Certificate('path/to/your/firebase-adminsdk.json')  
firebase_admin.initialize_app(cred)


def validate_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email)


def validate_phone_number(phone):
    try:
        parsed_number = phonenumbers.parse(phone, "US") 
        return phonenumbers.is_valid_number(parsed_number)
    except NumberParseException:
        return False

@app.route('/contact', methods=['POST'])
def contact():
   
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')

  
    if not name or not email or not message:
        return jsonify({"error": "Missing required fields"}), 400
    
    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    if phone and not validate_phone_number(phone):
        return jsonify({"error": "Invalid phone number"}), 400


    email_body = f"""
    New Contact Form Submission:

    Name: {name}
    Email: {email}
    Phone: {phone}
    Message: {message}
    """

    
    try:
        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            recipients=['your-email@gmail.com'], 
            body=email_body
        )
        mail.send(msg)
        print("Email sent successfully!")

        
        fcm_token = "your-device-fcm-token"  
        notification_message = f"New Contact Form Submission:\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"

        fcm_message = messaging.Message(
            notification=messaging.Notification(
                title="New Contact Form Submission",
                body=notification_message
            ),
            token=fcm_token
        )

        
        response = messaging.send(fcm_message)
        print(f"Successfully sent push notification: {response}")

        return jsonify({"message": "Message sent successfully!"}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
