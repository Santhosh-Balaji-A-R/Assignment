from pytz import timezone as pytz_timezone
from datetime import datetime

# Convert class datetime from IST to the requested timezone
def convert_timezone(class_info, to_tz):
    dt = datetime.fromisoformat(class_info['datetime'])
    ist = pytz_timezone('Asia/Kolkata')
    dt_ist = ist.localize(dt)
    target = pytz_timezone(to_tz)
    converted = dt_ist.astimezone(target)
    class_info['datetime'] = converted.strftime('%Y-%m-%d %H:%M:%S')
    return class_info

# Validate required fields in booking request
def validate_booking_input(data):
    required = ['class_id', 'client_name', 'client_email']
    for field in required:
        if field not in data:
            return False, f"{field} is required"
    return True, None
