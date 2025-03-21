from square.client import Client

# Initialize Square Client
client = Client(
    access_token="YOUR_SQUARE_ACCESS_TOKEN",
    environment="sandbox"  # Change to "production" when live
)

# 🏠 Step 1: Create a Customer
def create_customer(email, first_name, last_name):
    body = {
        "idempotency_key": "unique-customer-key-123",
        "given_name": first_name,
        "family_name": last_name,
        "email_address": email
    }

    response = client.customers.create_customer(body)
    return response.body  # Returns customer_id

# 💳 Step 2: Save a New Card to the Customer
def save_card(customer_id, card_token):
    body = {
        "idempotency_key": "unique-key-456",  # Unique key for each request
        "source_id": card_token  # Correct key for the card token
    }

    response = client.customers.create_customer_card(customer_id, body)
    return response.body

# 🗑️ Step 3: Delete an Existing Card
def delete_card(customer_id, card_id):
    response = client.customers.delete_customer_card(customer_id, card_id)
    return response.body

# ➕ Step 4: Add a New Card
def add_new_card(customer_id, card_token):
    body = {
        "idempotency_key": "unique-key-789",  # Unique for each request
        "source_id": card_token
    }

    response = client.customers.create_customer_card(customer_id, body)
    return response.body

# 🎯 Example Usage
customer_id = "CUSTOMER_ID_FROM_STEP_1"
old_card_id = "OLD_CARD_ID"
new_card_token = "NEW_CARD_TOKEN_FROM_FRONTEND"

# 1️⃣ Delete the old card
delete_response = delete_card(customer_id, old_card_id)
print(delete_response)

# 2️⃣ Add the new card
new_card_response = add_new_card(customer_id, new_card_token)
print(new_card_response)
