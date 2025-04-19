import stripe
import firebase_admin
from firebase_admin import credentials, firestore
import uuid  # Generate unique idempotency keys

# 🔹 Initialize Firebase
cred = credentials.Certificate("your-firebase-admin-sdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 🔹 Initialize Stripe
stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

# 🏠 Step 1: Create a Customer
def create_customer(email, first_name, last_name):
    try:
        customer = stripe.Customer.create(
            email=email,
            name=f"{first_name} {last_name}",
            description="VIP Customer"
        )
        print(f"✅ Customer created: {customer.id}")
        return customer.id
    except stripe.error.StripeError as e:
        print(f"❌ Error creating customer: {e.user_message} | {e}")
        return None

# 💳 Step 2: Save a Card to Customer
def save_card(customer_id, card_token):
    try:
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={"token": card_token}
        )

        stripe.PaymentMethod.attach(payment_method.id, customer=customer_id)
        stripe.Customer.modify(
            customer_id,
            invoice_settings={"default_payment_method": payment_method.id}
        )

        print(f"✅ Card saved: {payment_method.id}")
        return payment_method.id
    except stripe.error.StripeError as e:
        print(f"❌ Error saving card: {e.user_message} | {e}")
        return None

# 💎 Step 3: Create a VIP Subscription
def create_subscription(customer_id, email, price_id):
    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],  # Price ID from Stripe dashboard
            expand=["latest_invoice.payment_intent"]
        )

        print(f"✅ Subscription created: {subscription.id}")
        save_subscription_to_firebase(customer_id, subscription.id, email, "Basic")
        return subscription.id
    except stripe.error.StripeError as e:
        print(f"❌ Error creating subscription: {e.user_message} | {e}")
        return None

# 🔼 Step 4: Upgrade or Downgrade Subscription
def change_subscription(subscription_id, customer_id, email, new_price_id):
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)

        updated_subscription = stripe.Subscription.modify(
            subscription_id,
            items=[{
                "id": subscription["items"]["data"][0].id,
                "price": new_price_id
            }],
            proration_behavior="create_prorations"  # Charges only for the difference
        )

        print(f"✅ Subscription upgraded/downgraded to {new_price_id}")
        save_subscription_to_firebase(customer_id, updated_subscription.id, email, "VIP")
        return updated_subscription.id
    except stripe.error.StripeError as e:
        print(f"❌ Error changing subscription: {e.user_message} | {e}")
        return None

# 🗑️ Step 5: Cancel a Subscription
def cancel_subscription(subscription_id, customer_id):
    try:
        # Retrieve subscription to ensure it exists
        subscription = stripe.Subscription.retrieve(subscription_id)
        if not subscription:
            print(f"❌ Subscription {subscription_id} does not exist.")
            return False
        
        stripe.Subscription.delete(subscription_id)
        print(f"✅ Subscription canceled: {subscription_id}")

        # Remove from Firebase
        db.collection("subscriptions").document(customer_id).delete()
        print(f"✅ Subscription removed from Firebase")
        return True
    except stripe.error.StripeError as e:
        print(f"❌ Error canceling subscription: {e.user_message} | {e}")
        return False

# 🔹 Save Subscription Data to Firebase
def save_subscription_to_firebase(customer_id, subscription_id, email, plan):
    if not customer_id or not subscription_id:
        print("❌ Error: Missing customer_id or subscription_id")
        return

    customer_ref = db.collection("subscriptions").document(customer_id)
    customer_ref.set({
        "customer_id": customer_id,
        "subscription_id": subscription_id,
        "email": email,
        "plan": plan,
    })
    print(f"✅ Saved subscription {subscription_id} to Firebase")

# 🎯 Example Usage
customer_email = "customer@example.com"
first_name = "John"
last_name = "Doe"
card_token = "NEW_CARD_TOKEN_FROM_FRONTEND"
basic_plan_price_id = "price_BASIC"   # Replace with Stripe Price ID
vip_plan_price_id = "price_VIP"       # Replace with Stripe Price ID

# 🔄 Create Customer & Subscription
customer_id = create_customer(customer_email, first_name, last_name)
if customer_id:
    card_id = save_card(customer_id, card_token)
    if card_id:
        subscription_id = create_subscription(customer_id, customer_email, basic_plan_price_id)

# 🔼 Upgrade to VIP Plan
if subscription_id:
    change_subscription(subscription_id, customer_id, customer_email, vip_plan_price_id)
