import os
import stripe
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 🔹 Load your secret Stripe API key
stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

# 🔹 Replace with your actual Stripe price ID for VIP Membership
VIP_PRICE_ID = "price_VIP"

# 🎟️ Route to Create a Stripe Checkout Session
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": VIP_PRICE_ID,
                    "quantity": 1,
                }
            ],
            success_url="http://localhost:5000/success",
            cancel_url="http://localhost:5000/cancel",
        )
        return jsonify({"id": session.id})
    except Exception as e:
        return jsonify(error=str(e)), 400

# ✅ Success Page
@app.route("/success")
def success():
    return "✅ Payment Successful! Your VIP Membership is active."

# ❌ Cancel Page
@app.route("/cancel")
def cancel():
    return "❌ Payment Canceled. Please try again."

# 🔥 Run the Flask server
if __name__ == "__main__":
    app.run(port=5000, debug=True)
