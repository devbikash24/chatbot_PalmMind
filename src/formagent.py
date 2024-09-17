from .utilities.validations import validate_email, validate_phone, extract_date
from .tool_agent import ToolAgent

class FormsAgent:
    def process_form(self, form_data):
        name = form_data.get('name')
        email = form_data.get('email')
        phone = form_data.get('phone')
        date_query = form_data.get('date_query')

        if not name or not validate_email(email) or not validate_phone(phone):
            return {"message": "Invalid input provided"}
        
        date = extract_date(date_query)
        if not date:
            return {"message": "Could not extract a valid date"}

        # Further processing or booking logic with the tool agent
        tool_agent = ToolAgent()
        appointment_status = tool_agent.book_appointment(name, email, phone, date)
        
        if appointment_status:
            return {
                "message": f"Appointment booked for {name} on {date}. We will contact you at {phone}."
            }
        else:
            return {"message": "Failed to book the appointment. Please try again."}
