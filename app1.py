from flask import Flask, render_template, request, jsonify
from groq import Groq
# from  import handle_document_query
# from chatbot.user_info import collect_user_information
# from chatbot.appointment import handle_appointment_booking

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session handling
from pydantic import BaseModel, EmailStr, constr

# Define User Data Model
# class User(BaseModel):
#     name: str
#     phone_number: constr(regex=r'^\+?[1-9]\d{1,14}$')  # Phone number validation
#     email: EmailStr  # Email validation
# A dictionary to store the user information temporarily during the chat session.
session = {}




import re

def validate_email(email):
    """ Validate email format using regex. """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def validate_phone_number(phone_number):
    """ Validate phone number format using regex. """
    return re.match(r"^\+?1?\d{9,15}$", phone_number) is not None


def handle_appointment_booking(d):
    s = f"bad,{d}"
    return s

def handle_document_query(d):
    s = f"sorry,{d}"
    return s


app = Flask(__name__)

@app.route('/')
def index():
    """ Renders the homepage with the chatbot interface. """
    # If session exists, skip the form, otherwise render form
    if 'user_info' in session:
        return render_template('chat.html', show_form=False)
    return render_template('chat.html', show_form=True)

# New route to handle form submission
@app.route('/submit-form', methods=['POST'])
def submit_form():
    """
    Handles the user details form submission, validates input, and stores in session.
    """
    data = request.json
    name = data.get('name')
    phone = data.get('phone')
    email = data.get('email')

    # Validate phone number and email
    if not validate_phone_number(phone) or not validate_email(email):
        return jsonify({"success": False})

    # Store data in session
    session['user_info'] = {'name': name, 'phone': phone, 'email': email}

    return jsonify({"success": True, "user_info": session['user_info']}), 200  # Return user info in the response

@app.route('/skip_form', methods=['POST'])
def skip_form():
    """ Allows the user to skip the form. """
    session['user_info'] = {
        "name": "Anonymous",
        "phone": "N/A",
        "email": "N/A"
    }
    return jsonify({"success": True, "user_info": session['user_info']}), 200  # Return anonymous info


from langchain.agents import initialize_agent, Tool
from langchain.agents import create_structured_chat_agent
from datetime import datetime
import dateparser
import re
from langchain_groq import ChatGroq

import getpass
import os
from dotenv import load_dotenv
load_dotenv()

# Set your Groq API key here
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_ENV")

# client = Groq(
#     api_key=  os.environ["GROQ_API_KEY"] ,
# )
def parse_date(input_text):
    parsed_date = dateparser.parse(input_text)
    if parsed_date:
        return parsed_date.strftime('%Y-%m-%d')
    else:
        return "Could not understand the date."
# Mock appointment booking tool (with Google Calendar API integration placeholder)
def book_appointment(date, email, phone):
    # Call to Google Calendar API or custom booking API
    # Example: Make the API request to Google Calendar to book the appointment here
    return f"Appointment successfully booked on {date} for {email}."


# LangChain Tools
date_tool = Tool(name="DateParser", func=parse_date, description="Extracts dates from natural language (e.g., 'next Monday') and converts to YYYY-MM-DD.")
email_tool = Tool(name="EmailValidator", func=validate_email, description="Validates email addresses.")
phone_tool = Tool(name="PhoneValidator", func=validate_phone_number, description="Validates phone numbers.")
booking_tool = Tool(name="AppointmentBooking", func=book_appointment, description="Books appointments using the provided date, email, and phone.")


tools = [date_tool, email_tool, phone_tool, booking_tool]
model = ChatGroq(model="llama3-8b-8192")
client = model  # Using the Groq client as LLM
from langchain.prompts import PromptTemplate

# Define the prompt for the agent
# Define the prompt using PromptTemplate
prompt_template = """
You are a helpful assistant that helps users with their queries. You can use the following tools to assist them:
{tools}
Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}
When necessary, feel free to use the tools to provide accurate responses. If you need to perform intermediate steps, you can explain them.
Here is the query:
{input_names}

{agent_scratchpad}
"""

# Use PromptTemplate to handle dynamic input
prompt = PromptTemplate(
    input_variables=["input", "tool_names", "agent_scratchpad"],  # Expecting these variables in the prompt
    template=prompt_template
)

# Create the agent with client, tools, and prompt
agent = create_structured_chat_agent(llm=client, tools=tools, prompt=prompt)

@app.route('/submit-conversational-form', methods=['POST'])
def submit_conversational_form():
    """ Handles the form submission from the conversational flow """
    data = request.json
    name = data.get('name')
    date_input = data.get('date')
    phone = data.get('phone')
    email = data.get('email')

    # Parse date, validate email and phone
    parsed_date = parse_date(date_input)
    if not validate_email(email) or not validate_phone_number(phone):
        return jsonify({"success": False, "message": "Invalid email or phone number."}), 400

    # Book appointment using Google Calendar API or custom API (Mock)
    booking_result = book_appointment(parsed_date, email, phone)
    return jsonify({"success": True, "message": booking_result}), 200

def d(user_message):
    # Initialize an empty list to collect all the chunks of the response
    chunks = []
    
    # Streaming response using Groq
    for chunk in model.stream(user_message):
        if hasattr(chunk, 'content'):
            chunks.append(chunk.content)  # Extract the content from AIMessageChunk
    # Combine all the chunk content into a single string
    full_message = "".join(chunks)  # Concatenate all chunk contents into one response
    print("=====>", full_message) 
    return full_message
def handle_call_request1():
    return {
        "type": "form",
        "fields": ["name", "phone", "email"]
    }

def handle_appointment_booking1():
    return {
        "type": "form",
        "fields": ["name", "phone", "email", "date"]
    }
@app.route('/parse_date', methods=['POST'])
def parse_date():
    data = request.get_json()
    natural_date = data.get('date', '')
    # Try to parse the date from natural language
    parsed_date = dateparser.parse(natural_date)
    if parsed_date:
        return jsonify({'date': parsed_date.strftime('%Y-%m-%d')})
    else:
        return jsonify({'error': 'Could not parse date'}), 400

@app.route('/chat', methods=['POST'])
def chat():
    """ Handles user queries related to document content. """
    user_message = request.json.get('message')
    
    # Route the message based on the user's query
    if "call me" in user_message.lower():
        return jsonify({"action": "showCallMeForm"})
    elif "book an appointment" in user_message.lower():
        return jsonify({"action": "showAppointmentForm"})
    else:
        response = handle_document_query(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
