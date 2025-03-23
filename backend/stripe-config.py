import stripe

# 🔹 Load your secret Stripe API key
stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

# 🔹 Webhook secret (if you're handling webhooks)
WEBHOOK_SECRET = "YOUR_STRIPE_WEBHOOK_SECRET"

# 🔹 Price IDs for different subscription plans (Replace with your actual Stripe Price IDs)
PRICE_IDS = {
    "silver": "price_SILVER_PLAN_ID",
    "gold": "price_GOLD_PLAN_ID",
    "platinum": "price_PLATINUM_PLAN_ID"
}

def get_price_id(plan_name):
    """Returns the Stripe Price ID based on the subscription plan name."""
    return PRICE_IDS.get(plan_name.lower())  # Case insensitive lookup
