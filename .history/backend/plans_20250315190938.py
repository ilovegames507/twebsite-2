from square.client import Client
import uuid

square_client = Client(
    access_token="YOUR_SQUARE_ACCESS_TOKEN",
    environment="sandbox"
)


TIERS = ["broke", "slicer", "gold"]
DURATIONS = ["1_month", "3_months", "1_year"]


SUBSCRIPTION_PLANS = {
    "broke_1_month": "PLAN_ID_BROKE_1M",
    "broke_3_months": "PLAN_ID_BROKE_3M",
    "broke_1_year": "PLAN_ID_BROKE_1Y",
    
    "slicer_1_month": "PLAN_ID_SLICER_1M",
    "slicer_3_months": "PLAN_ID_SLICER_3M",
    "slicer_1_year": "PLAN_ID_SLICER_1Y",
    
    "gold_1_month": "PLAN_ID_GOLD_1M",
    "gold_3_months": "PLAN_ID_GOLD_3M",
    "gold_1_year": "PLAN_ID_GOLD_1Y"
}


CHECKOUT_PRICES = {
    "broke_1_month": {"name": "Broke - Monthly", "price": 500},  # $5.00
    "broke_3_months": {"name": "Broke - 3 Months", "price": 1350},  # $13.50 (10% off)
    "broke_1_year": {"name": "Broke - Yearly", "price": 4800},  # $48.00 (20% off)
    
    "slicer_1_month": {"name": "Slicer - Monthly", "price": 1500},  # $15.00
    "slicer_3_months": {"name": "Slicer - 3 Months", "price": 4000},  # $40.00
    "slicer_1_year": {"name": "Slicer - Yearly", "price": 15000},  # $150.00

    "gold_1_month": {"name": "Gold - Monthly", "price": 3000},  # $30.00
    "gold_3_months": {"name": "Gold - 3 Months", "price": 8500},  # $85.00
    "gold_1_year": {"name": "Gold - Yearly", "price": 30000}  # $300.00
}

def create_subscription(tier, duration, customer_id):
    """Creates an automatic subscription for a given tier and duration."""
    
    key = f"{tier}_{duration}"
    if key not in SUBSCRIPTION_PLANS:
        print("Invalid tier or duration. Available options: broke, slicer, gold & 1_month, 3_months, 1_year.")
        return
    
    plan_id = SUBSCRIPTION_PLANS[key]
    
    result = square_client.subscriptions_api.create_subscription(
        body={
            "idempotency_key": str(uuid.uuid4()),
            "plan_id": plan_id,
            "customer_id": customer_id,
            "start_date": "2022-01-01T00:00:00Z"
        }
    )
    
    if result.is_success():
        print("Subscription created successfully!")
        print(result.body)
    else:
        print("Error creating subscription:", result.errors)

def create_checkout_link(tier, duration):
    """Generates a one-time payment checkout link for a given tier and duration."""
    
    key = f"{tier}_{duration}"
    if key not in CHECKOUT_PRICES:
        print("Invalid tier or duration. Available options: broke, slicer, gold & 1_month, 3_months, 1_year.")
        return

    item = CHECKOUT_PRICES[key]
    
    body = {
        "idempotency_key": str(uuid.uuid4()), 
        "order": {
            "location_id": "YOUR_LOCATION_ID",
            "line_items": [
                {
                    "name": item["name"],
                    "quantity": "1",
                    "base_price_money": {
                        "amount": item["price"],  
                        "currency": "USD"
                    }
                }
            ]
        },
        "redirect_url": "https://yourwebsite.com/subscription-success"  
    }

    result = square_client.checkout.create_checkout(location_id="YOUR_LOCATION_ID", body=body)

    if result.is_success():
        print("Checkout URL:", result.body["checkout"]["checkout_page_url"])
        return result.body["checkout"]["checkout_page_url"]
    else:
        print("Error creating checkout:", result.errors)
        return None


create_subscription("gold", "1_month", "CUSTOMER_ID")


checkout_url = create_checkout_link("slicer", "3_months")
print("Checkout URL:", checkout_url)
