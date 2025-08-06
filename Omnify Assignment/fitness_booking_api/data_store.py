import json
import os
from datetime import datetime, timezone

CLASSES_FILE = 'classes.json'
BOOKINGS_FILE = 'bookings.json'

# Load JSON data from file. If file doesn't exist, create it with an empty list.
def load_json(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)
    with open(file, 'r') as f:
        return json.load(f)

# Save data to a JSON file
def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

# Return all fitness classes
def get_all_classes():
    return load_json(CLASSES_FILE)

# Add a booking for a given class ID
def add_booking(class_id, name, email):
    classes = load_json(CLASSES_FILE)
    bookings = load_json(BOOKINGS_FILE)

    for cls in classes:
        if cls['id'] == class_id:
            if cls['available_slots'] <= 0: # Check if class has available slots
                raise ValueError("No available slots.")
            cls['available_slots'] -= 1 # Reduce available slots
            booking = {
                "id": len(bookings) + 1,
                "class_id": class_id,
                "client_name": name,
                "client_email": email,
                "datetime": datetime.now(timezone.utc).isoformat()
            }
            bookings.append(booking)
            save_json(CLASSES_FILE, classes)
            save_json(BOOKINGS_FILE, bookings)
            return booking
    raise ValueError("Class not found.") # If class_id not found

# Get all bookings for a particular client email
def get_bookings_by_email(email):
    bookings = load_json(BOOKINGS_FILE)
    classes = load_json(CLASSES_FILE)
    return [
        {
            "class_name": next((c["name"] for c in classes if c["id"] == b["class_id"]), "Unknown"),
            "datetime": b["datetime"],
            "client_name": b["client_name"],
        }
        for b in bookings if b["client_email"] == email
    ]

# Seed the class data into classes.json if not already populated
def seed_classes():
    """Create classes.json with sample data if it's missing, empty, or corrupt."""
    try:
        classes = load_json(CLASSES_FILE)
        # Skip if data already present
        if isinstance(classes, list) and len(classes) > 0:
            print("classes.json already populated. Skipping seeding.")
            return
    except Exception as e:
        print(f"Could not load {CLASSES_FILE}: {e}")

    print("Seeding sample classes into classes.json...")
    sample_classes = [
        {"id": 1, "name": "Yoga", "datetime": "2025-08-06T07:00:00", "instructor": "Aarti", "available_slots": 5},
        {"id": 2, "name": "Zumba", "datetime": "2025-08-06T08:00:00", "instructor": "Raj", "available_slots": 10},
        {"id": 3, "name": "HIIT", "datetime": "2025-08-06T09:00:00", "instructor": "Sameer", "available_slots": 8}
    ]
    save_json(CLASSES_FILE, sample_classes)
    print("Seeded successfully.")

