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
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session handling

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_ENV')
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Define allowed document extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
UPLOAD_FOLDER = 'data/docs'  # Directory where uploaded files will be saved
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])




GROQ_API_KEY = os.getenv('GROQ_ENV')

from src.utilities.load_configuration import LoadConfiguration
app_config = LoadConfiguration()
from src.utilities.create_vectordb import PrepareFAISSVectorDB




@app.route('/upload-document', methods=['POST'])
def upload_file():
    upload_folder = app.config['UPLOAD_FOLDER']


    # Step 1: Remove all files from the upload directory before proceeding
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory and all its contents
        except Exception as e:
            return jsonify({'success': False, 'message': f'Failed to delete files: {str(e)}'})

    # Step 2: Handle the file upload
    print("Files received:", request.files)  # Debugging line to check what's received

    if 'document' not in request.files:
        return jsonify({'success': False, 'message': 'No file part'})

    file = request.files['document']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        try:
            # Save the file to the upload folder
            file.save(file_path)

            # Step 3: Process the file (e.g., vectorize and store in FAISS)
            db_instance = PrepareFAISSVectorDB(app_config)
            db_instance.prepare_and_save_vectordb()  # Pass file_path to use it
            db_instance.load_vectordb()

            return jsonify({'success': True, 'message': 'File successfully uploaded and vectorized'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return jsonify({'success': False, 'message': 'Invalid file format'})



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Extract text from documents

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

import faiss
import pickle

from groq import Groq
GROQ_API = os.getenv("GROQ_ENV")
client = Groq(api_key=GROQ_API)
from langchain.prompts import PromptTemplate

# Load FAISS index from disk
def load_faiss_index():

    FAISS_FOLDER_INDEX = 'data/faiss/faiss_index'
    FAISS_FOLDER = 'data/faiss'
    app.config['FAISS_FOLDER_INDEX'] = FAISS_FOLDER_INDEX
    app.config['FAISS_FOLDER'] = FAISS_FOLDER
    index_file = os.path.join(app.config['FAISS_FOLDER_INDEX'], "index.faiss")
    pkl_file = os.path.join(app.config['FAISS_FOLDER_INDEX'], "index.pkl")
    metadata_file = os.path.join(app.config['FAISS_FOLDER'], "faiss_metadata.pkl")

    if os.path.exists(index_file) and os.path.exists(pkl_file) and os.path.exists(metadata_file):
        # Load FAISS index
        index = faiss.read_index(index_file)

        # Load pickled data (necessary for loading the vector store correctly)
        with open(pkl_file, 'rb') as f:
            vector_data = pickle.load(f)

        # Log the structure of the pickled data
        print(f"Vector data type: {type(vector_data)}")
        print(f"Vector data content: {vector_data}")

        # Load metadata (if any)
        with open(metadata_file, 'rb') as f:
            faiss_metadata = pickle.load(f)

        # Assuming the vector data is a tuple, let's unpack it
        if isinstance(vector_data, tuple):
            docstore, index_to_docstore_id = vector_data
        else:
            return None  # Handle error if the structure is unexpected

        # Return a loaded FAISS vectorstore using LangChain FAISS
        return FAISS(embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"), 
                     index=index, 
                     docstore=docstore, 
                     index_to_docstore_id=index_to_docstore_id)
    else:
        return None
def generate_groq_response(client, query_text, retrieved_texts):
    # Create a prompt template
    template = """You are a helpful assistant. Use the following retrieved documents to answer the question in a helpful way.

    Retrieved Documents:
    {retrieved_texts}
    
    Question: {query_text}
    
    Answer:"""

    # Define the PromptTemplate
    prompt = PromptTemplate(
        input_variables=["retrieved_texts", "query_text"],
        template=template,
    )
    
    # Format the prompt with the retrieved documents and query
    formatted_prompt = prompt.format(
        retrieved_texts="\n".join(retrieved_texts),
        query_text=query_text,
    )
    
    try:
        # Example structure based on typical API usage
        response = client.chat.completions.create(  # Adjust the method according to Groq's API
            messages=[  # Messages should be an array of dicts
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": formatted_prompt}
            ],
            model="llama3-8b-8192",  # Adjust this based on the Groq API model you are using
            temperature=0.7,  # Set temperature for response generation
            max_tokens=200  # Limit the response length
        )

        # print(response.choices[0])
        return response.choices[0].message.content  # Extract the generated answer
    
    except Exception as e:
        return f"Error in generating response: {str(e)}"


@app.route('/query-document', methods=['POST'])
def submit_query_document():

    data = request.get_json()  # Get the JSON data from the request
    query = data.get('query')


    # Load the FAISS index
    faiss_store = load_faiss_index()
    if not faiss_store:
        return jsonify({"success": False, "message": "No FAISS index found."}), 400

    if not query:
        return jsonify({"success": False, "message": "Query not provided."}), 400

    # Perform the similarity search on the FAISS index
    results = faiss_store.similarity_search(query, k=3)  # Retrieve top 3 most similar documents

    # Retrieve the top relevant documents' content
    retrieved_texts = [result.page_content for result in results]

    # Generate a response using Groq and LangChain PromptTemplate
    response = generate_groq_response(client, query, retrieved_texts)

    return jsonify({"success": True, "message": response}), 200

# Function to generate response using Groq and PromptTemplate

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
