from flask import Flask, request, jsonify
from data_store import (
    get_all_classes, add_booking, get_bookings_by_email, seed_classes
)
from utils import convert_timezone, validate_booking_input

# Initialize Flask app
app = Flask(__name__)

# Endpoint to list all available fitness classes
@app.route('/classes', methods=['GET'])
def list_classes():
    timezone = request.args.get('tz', 'Asia/Kolkata') # Optional query param 'tz' for timezone conversion (default: Asia/Kolkata)
    classes = get_all_classes()
    return jsonify([convert_timezone(c, timezone) for c in classes]), 200 # Convert class datetimes to requested timezone and return

# Endpoint to book a spot in a class
@app.route('/book', methods=['POST'])
def book():
    data = request.json
    is_valid, error = validate_booking_input(data) # Validate request body
    if not is_valid:
        return jsonify({'error': error}), 400

    try:
        booking = add_booking(data['class_id'], data['client_name'], data['client_email'])
        return jsonify({'message': 'Booking successful', 'booking': booking}), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

# Endpoint to retrieve all bookings by client email
@app.route('/bookings', methods=['GET'])
def get_bookings():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    return jsonify(get_bookings_by_email(email)), 200

# Seed the classes and start the Flask server
if __name__ == '__main__':
    seed_classes()
    app.run(debug=True)
