import datetime
import requests

# Calendly API Token & User URI (Replace with actual credentials)
CALENDLY_API_TOKEN = "your_calendly_api_token"
CALENDLY_USER_URI = "your_calendly_user_uri"

# Business Hours
BUSINESS_HOURS = {
    0: ("10:00:00", "18:00:00"),  # Monday
    1: ("10:00:00", "18:00:00"),  # Tuesday
    2: ("10:00:00", "18:00:00"),  # Wednesday
    3: ("10:00:00", "18:00:00"),  # Thursday
    4: ("10:00:00", "16:00:00"),  # Friday
    5: None,  # Saturday (Closed)
    6: ("10:00:00", "18:00:00")   # Sunday (10-6)
}

# Track appointments per day
appointments = {}

def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    day_of_week = now.weekday()

    if day_of_week in BUSINESS_HOURS:
        hours = BUSINESS_HOURS[day_of_week]
        if hours is None:
            return "Marcelin's Auto Repair™ is Closed today."
        
        opening_time, closing_time = hours
        if opening_time <= current_time < closing_time:
            return f"Marcelin's Auto Repair™ is Open. Current time: {current_time}"
        else:
            return f"Marcelin's Auto Repair™ is Closed. Current time: {current_time}"

    return "Invalid day of the week."

def book_appointment(name, phone, vehicle, location, issues, mechanic_before, parts_ready, contact_method):
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    # Limit to 4 appointments per day
    if appointments.get(today, 0) >= 4:
        return "Sorry, no available slots today. Please choose another day."

    appointments[today] = appointments.get(today, 0) + 1  # Increment count

    # Calendly API request
    headers = {
        "Authorization": f"Bearer {CALENDLY_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Create a scheduling link
    calendly_event_url = f"https://api.calendly.com/event_types/{CALENDLY_USER_URI}/scheduling_links"
    data = {
        "max_event_count": 1,
        "owner": CALENDLY_USER_URI,
        "questions_and_answers": [
            {"question": "Vehicle Make & Model", "answer": vehicle},
            {"question": "Meeting Location", "answer": location},
            {"question": "Issues with Vehicle", "answer": issues},
            {"question": "Has Another Mechanic Worked on It?", "answer": mechanic_before},
            {"question": "Will Parts Be Ready?", "answer": parts_ready},
            {"question": "Best Contact Method", "answer": contact_method}
        ]
    }
    
    response = requests.post(calendly_event_url, headers=headers, json=data)
    
    if response.status_code == 201:
        return f"Appointment booked successfully for {name} on {today}! Check your email for confirmation."
    else:
        return f"Failed to book appointment. Calendly Error: {response.text}"

# Example Usage
print(get_time())
print(book_appointment(
    name="John Doe",
    phone="123-456-7890",
    vehicle="Toyota Camry 2018",
    location="123 Main St",
    issues="Brake problems",
    mechanic_before="Yes",
    parts_ready="No",
    contact_method="Phone"
))
