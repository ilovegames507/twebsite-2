from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def calendly_webhook():
    data = request.json
    print("📩 Received Webhook:", data)

    event_type = data.get("event")
    event_details = data.get("payload", {})

    if event_type == "invitee.created":
        return jsonify({"message": "New appointment booked!", "details": event_details}), 200
    elif event_type == "invitee.canceled":
        return jsonify({"message": "Appointment canceled!", "details": event_details}), 200

    return jsonify({"message": "Event received"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
