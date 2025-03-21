import requests

CALENDLY_API_TOKEN = "YOUR_CALENDLY_API_KEY"
CALENDLY_EVENT_TYPE = "YOUR_EVENT_TYPE_UUID"  # Replace with your actual event UUID

def book_appointment(name, phone, vehicle, location, issue, safe_place, mechanic_before, contact_method, services):
    headers = {
        "Authorization": f"Bearer {CALENDLY_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    calendly_event_url = f"https://api.calendly.com/event_types/{CALENDLY_EVENT_TYPE}/scheduling_links"

    data = {
        "max_event_count": 1,
        "owner": f"https://api.calendly.com/users/YOUR_USER_UUID",
        "questions_and_answers": [
            {"question": "What is your name?", "answer": name},
            {"question": "What is your year/make/model of your car?", "answer": vehicle},
            {"question": "Do you have a safe and legal place for me to work?", "answer": safe_place},
            {"question": "What is the issue with your vehicle?", "answer": issue},
            {"question": "Where is the vehicle located? (Need address to calculate travel fees)", "answer": location},
            {"question": "Has another mechanic worked on this issue in the last 6 months?", "answer": mechanic_before},
            {"question": "What is the best way to contact you? (Include contact info)", "answer": contact_method},
            {"question": "Are you looking for any of these common services? (Check all that apply)", "answer": services}
        ]
    }

    response = requests.post(calendly_event_url, headers=headers, json=data)
    
    if response.status_code == 201:
        return f"Appointment booked successfully for {name}! Check your email for confirmation."
    else:
        return f"Failed to book appointment. Calendly Error: {response.text}"
