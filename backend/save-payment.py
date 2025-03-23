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
        print(f"❌ Error creating customer: {e}")
        return None

# 💳 Step 2: Save a New Card to the Customer
def save_card(customer_id, card_token):
    try:
        payment_method = stripe.PaymentMethod.attach(
            card_token,
            customer=customer_id
        )

        stripe.Customer.modify(
            customer_id,
            invoice_settings={"default_payment_method": payment_method.id}
        )

        print(f"✅ Card saved: {payment_method.id}")
        return payment_method.id
    except stripe.error.StripeError as e:
        print(f"❌ Error saving card: {e}")
        return None

# 🗑️ Step 3: Delete an Existing Card
def delete_card(payment_method_id):
    try:
        stripe.PaymentMethod.detach(payment_method_id)
        print(f"✅ Card deleted: {payment_method_id}")
        return True
    except stripe.error.StripeError as e:
        print(f"❌ Error deleting card: {e}")
        return False

# 🔄 Step 4: Replace Old Card with New Card
def replace_card(customer_id, old_card_id, new_card_token):
    if delete_card(old_card_id):
        new_card_id = save_card(customer_id, new_card_token)
        if new_card_id:
            return new_card_id
    return None

# 🔹 Save Customer & Card to Firebase
def save_customer_to_firebase(customer_id, card_id, email):
    if customer_id and card_id:
        customer_ref = db.collection("customers").document(customer_id)
        customer_ref.set({
            "customer_id": customer_id,
            "card_id": card_id,
            "email": email
        })
        print(f"✅ Saved {customer_id} to Firebase")
    else:
        print("❌ Error: Invalid customer or card ID")

# 🎯 Example Usage
customer_id = "CUSTOMER_ID_FROM_STEP_1"
old_card_id = "OLD_CARD_ID"
new_card_token = "NEW_CARD_TOKEN_FROM_FRONTEND"

# 🔄 Replace old card and save new one
new_card_id = replace_card(customer_id, old_card_id, new_card_token)
if new_card_id:
    save_customer_to_firebase(customer_id, new_card_id, "customer@example.com")
