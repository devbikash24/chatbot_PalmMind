from flask import Flask, render_template, request, jsonify, session
from pydantic import BaseModel, EmailStr, Field
import re
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import dateparser

from werkzeug.utils import secure_filename
import PyPDF2  # For processing PDFs
import docx2txt  # For processing Word documents

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session handling

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_ENV")


# Define allowed document extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
UPLOAD_FOLDER = './uploads'  # Directory where uploaded files will be saved
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extract text from documents
def extract_text_from_document(file_path):
    file_ext = file_path.rsplit('.', 1)[1].lower()
    
    if file_ext == 'pdf':
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ''
            for page_num in range(pdf_reader.getNumPages()):
                text += pdf_reader.getPage(page_num).extractText()
        return text

    elif file_ext == 'docx':
        return docx2txt.process(file_path)

    elif file_ext == 'txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    return None

# Helper function to check if the uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define User Data Model
class User(BaseModel):
    name: str
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')  # Phone number validation using regex
    email: EmailStr  # Email validation

# Validate email and phone number formats
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def validate_phone_number(phone_number):
    return re.match(r"^\+?1?\d{9,15}$", phone_number) is not None

# Custom date parsing function with future date preference
def parse_date(input_text):
    today = datetime.today()

    # Handle specific phrases manually (e.g., "next Monday", "tomorrow")
    if "next monday" in input_text.lower():
        # Calculate the next Monday
        days_ahead = (7 - today.weekday() + 0) % 7 + 7  # Days until next Monday
        next_monday = today + timedelta(days=days_ahead)
        return next_monday.strftime('%Y-%m-%d')

    elif "tomorrow" in input_text.lower():
        # Handle tomorrow
        tomorrow = today + timedelta(days=1)
        return tomorrow.strftime('%Y-%m-%d')

    elif "next friday" in input_text.lower():
        # Calculate the next Friday
        days_ahead = (7 - today.weekday() + 4) % 7 + 7  # Days until next Friday
        next_friday = today + timedelta(days=days_ahead)
        return next_friday.strftime('%Y-%m-%d')

    # Use dateparser with settings to prefer future dates
    parsed_date = dateparser.parse(input_text, settings={'PREFER_DATES_FROM': 'future'})

    if parsed_date:
        return parsed_date.strftime('%Y-%m-%d')
    else:
        return "Invalid date"

# Mock appointment booking tool
def book_appointment(date, email, phone):
    # Normally, this would call a booking API like Google Calendar
    return f"Appointment successfully booked on {date} for {email}."

@app.route('/')
def index():
    """ Renders the homepage with the chatbot interface. """
    if 'user_info' in session:
        return render_template('app4.html', show_form=False)
    return render_template('app4.html', show_form=True)


@app.route('/submit-call-me-form', methods=['POST'])
def submit_call_me_form():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')

    # Validate phone number and email
    if not validate_phone_number(phone) or not validate_email(email):
        return jsonify({"success": False, "message": "Invalid phone number or email."}), 400

    # Return a success message
    message = f"Call request received from {name}. We will contact you at {email} or {phone}."
    return jsonify({"success": True, "message": message}), 200

@app.route('/submit-appointment-form', methods=['POST'])
def submit_appointment_form():
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')
    date = data.get('date')

    # Parse the date and validate inputs
    parsed_date = parse_date(date)

    if parsed_date == "Invalid date":
        return jsonify({
            "success": False,
            "message": "Invalid date format. Please enter a valid date like 'next Monday' or '2024-09-20'."
        }), 400

    if not validate_email(email) or not validate_phone_number(phone):
        return jsonify({"success": False, "message": "Invalid email or phone number."}), 400

    # Return a success message
    message = f"Appointment successfully booked on {parsed_date} for {name}."
    return jsonify({"success": True, "message": message}), 200


@app.route('/submit-query-document', methods=['POST'])
def submit_query_document():
    if 'document' not in request.files:
        return jsonify({"success": False, "message": "No document uploaded."}), 400

    file = request.files['document']
    query = request.form.get('query')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text from the uploaded document
        document_text = extract_text_from_document(file_path)

        if document_text:
            # Placeholder logic to "query" the document based on user input
            if query.lower() in document_text.lower():
                response = f"I found the following related information in the document: {query}"
            else:
                response = "Sorry, I couldn't find anything related to your query in the document."

            return jsonify({"success": True, "message": response}), 200
        else:
            return jsonify({"success": False, "message": "Failed to process the document."}), 400
    else:
        return jsonify({"success": False, "message": "Invalid file format."}), 400

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles user queries related to document content or appointment booking.
    """
    user_message = request.json.get('message')

    # Route the message based on user input
    if "call me" in user_message.lower():
        return jsonify({"action": "showCallMeForm"})
    elif "book an appointment" in user_message.lower():
        return jsonify({"action": "showAppointmentForm"})
    elif "query document" in user_message.lower():
        return jsonify({"action": "showUploadForm"})
    else:
        response = "I can help you with bookings, calling, or answering your queries."
    response = "I can help you with bookings, calling, or answering your queries."
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
