import pytest
from app import app
from data_store import save_json

# Files used for test data
CLASSES_FILE = 'classes.json'
BOOKINGS_FILE = 'bookings.json'

# Test data for classes and bookings
TEST_CLASSES = [
    {"id": 1, "name": "Yoga", "datetime": "2025-08-06T07:00:00", "instructor": "Aarti", "available_slots": 1},
    {"id": 2, "name": "Zumba", "datetime": "2025-08-06T08:00:00", "instructor": "Raj", "available_slots": 2},
]

TEST_BOOKINGS = []

# Flask test client with reset test data
@pytest.fixture
def client():
    save_json(CLASSES_FILE, TEST_CLASSES)
    save_json(BOOKINGS_FILE, TEST_BOOKINGS)
    return app.test_client()

# Test: List classes
def test_get_classes(client):
    res = client.get('/classes')
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

# Test: List classes with timezone conversion
def test_get_classes_with_timezone(client):
    res = client.get('/classes?tz=UTC')
    assert res.status_code == 200
    dt_str = res.get_json()[0]['datetime']
    assert " " in dt_str and "T" not in dt_str

# Test: Successful booking
def test_successful_booking(client):
    res = client.post('/book', json={
        "class_id": 1,
        "client_name": "Test User",
        "client_email": "test@example.com"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["booking"]["class_id"] == 1

# Test: Booking a full class
def test_overbooking(client):
    client.post('/book', json={
        "class_id": 1,
        "client_name": "User1",
        "client_email": "u1@example.com"
    })
    res = client.post('/book', json={
        "class_id": 1,
        "client_name": "User2",
        "client_email": "u2@example.com"
    })
    assert res.status_code == 400
    assert "No available slots" in res.get_data(as_text=True)

# Test: Missing required booking fields
def test_missing_fields(client):
    res = client.post('/book', json={
        "class_id": 2,
        "client_name": "Test"
    })
    assert res.status_code == 400
    assert "client_email is required" in res.get_data(as_text=True)

# Test: Booking a non-existent class
def test_invalid_class_id(client):
    res = client.post('/book', json={
        "class_id": 999,
        "client_name": "NoClass",
        "client_email": "n/a"
    })
    assert res.status_code == 400
    assert "Class not found" in res.get_data(as_text=True)

# Test: List Booking with emial
def test_get_bookings_by_email(client):
    client.post('/book', json={
        "class_id": 2,
        "client_name": "EmailTest",
        "client_email": "emailtest@example.com"
    })
    res = client.get('/bookings?email=emailtest@example.com')
    assert res.status_code == 200
    bookings = res.get_json()
    assert bookings[0]["client_name"] == "EmailTest"

# Test: List Booking without emial
def test_get_bookings_without_email(client):
    res = client.get('/bookings')
    assert res.status_code == 400
    assert "Email is required" in res.get_data(as_text=True)
