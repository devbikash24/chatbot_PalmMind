from flask import Blueprint, request, jsonify
from src.utilities.validations import validate_email, validate_phone_number
from src.utilities.date_utilities import parse_date

# Initialize the Blueprint for form-related routes
form_bp = Blueprint('form', __name__)

# Session dictionary (if using Flask's session, this should be handled with the session object)
session = {}

@form_bp.route('/submit-call-me-form', methods=['POST'])
def submit_call_me_form():
    """
    Handles the submission of the 'Call Me' form.
    Validates the user's phone number and email before proceeding.
    """
    data = request.json or {}
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')

    # Validate the phone number and email format
    if not validate_phone_number(phone):
        return jsonify({"success": False, "message": "Invalid phone number format."}), 400
    if not validate_email(email):
        return jsonify({"success": False, "message": "Invalid email format."}), 400

    # Create success message
    message = f"Call request received from {name}. We will contact you at {email} or {phone}."
    return jsonify({"success": True, "message": message}), 200

@form_bp.route('/submit-appointment-form', methods=['POST'])
def submit_appointment_form():
    """
    Handles the submission of the appointment booking form.
    Validates the user's phone number, email, and date before proceeding.
    """
    data = request.json or {}
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    date_input = data.get('date')

    # Validate the date, email, and phone number
    parsed_date = parse_date(date_input)
    if parsed_date == "Invalid date":
        return jsonify({"success": False, "message": "Invalid date format. Please provide a valid date."}), 400
    if not validate_email(email):
        return jsonify({"success": False, "message": "Invalid email format."}), 400
    if not validate_phone_number(phone):
        return jsonify({"success": False, "message": "Invalid phone number format."}), 400

    # Return a success message if all validations pass
    message = f"Appointment successfully booked on {parsed_date} for {name}."
    return jsonify({"success": True, "message": message}), 200
