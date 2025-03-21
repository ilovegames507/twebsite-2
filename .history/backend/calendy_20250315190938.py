import datetime

def get_time():
    # Get the current time and day of the week
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    day_of_week = now.weekday() 
    
    
    if day_of_week == 5:  
        return f"Marcelin's Auto Repair™ is Closed today."
    
    elif day_of_week == 6:  
        return f"Marcelin's Auto Repair™ is Closed today."
    
    
    elif day_of_week in range(0, 5):  
        opening_time = "10:00:00"
        closing_time = "18:00:00"
        if opening_time <= current_time < closing_time:
            return f"Marcelin's Auto Repair™ is Open. Current time: {current_time}"
        else:
            return f"Marcelin's Auto Repair™ is Closed. Current time: {current_time}"
    

    elif day_of_week == 4:  
        opening_time = "10:00:00"
        closing_time = "16:00:00"
        if opening_time <= current_time < closing_time:
            return f"Marcelin's Auto Repair™ is Open. Current time: {current_time}"
        else:
            return f"Marcelin's Auto Repair™ is Closed. Current time: {current_time}"


print(get_time())
