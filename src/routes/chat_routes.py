import os
from flask import Blueprint, request, jsonify, render_template, session
from groq import Groq

from src.utilities.faiss_utilities import load_faiss_index
from src.utilities.groq_utilties import generate_groq_response
from src.utilities.load_configuration import LoadConfiguration

# Load configuration
app_config = LoadConfiguration()
GROQ_API_KEY = app_config.groq_key
client = Groq(api_key=GROQ_API_KEY)

# Initialize the Blueprint for chat-related routes
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/')
def index():
    """
    Renders the homepage with the chatbot interface.
    If user information is in the session, the form will not be shown.
    """
    show_form = 'user_info' not in session
    return render_template('app4.html', show_form=show_form)

@chat_bp.route('/query-document', methods=['POST'])
def submit_query_document():
    """
    Handles document querying by performing a similarity search using FAISS
    and generates a response using the Groq API.
    """
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({"success": False, "message": "No query provided."}), 400

    faiss_store = load_faiss_index()
    if not faiss_store:
        return jsonify({"success": False, "message": "FAISS index not found."}), 400

    # Perform similarity search on the FAISS index
    results = faiss_store.similarity_search(query, k=3)
    retrieved_texts = [result.page_content for result in results]

    # Generate a response using the retrieved texts and the Groq API
    response = generate_groq_response(client, query, retrieved_texts)
    return jsonify({"success": True, "message": response}), 200

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    Handles generic user messages and routes the action based on user input.
    Returns a JSON response based on keywords detected in the user's message.
    """
    user_message = request.json.get('message', '').lower()

    if not user_message:
        return jsonify({"response": "Please provide a valid message."}), 400

    # Route the message based on the user's input
    if "call me" in user_message:
        return jsonify({"action": "showCallMeForm"})
    if "book an appointment" in user_message:
        return jsonify({"action": "showAppointmentForm"})
    if "query document" in user_message:
        return jsonify({"action": "showUploadForm"})

    # Default response if no action is matched
    return jsonify({"response": "I can help you with bookings, calling, or answering your queries."}), 200
