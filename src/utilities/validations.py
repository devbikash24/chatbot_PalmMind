import re
from datetime import datetime
from dateutil.parser import parse

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def validate_phone(phone):
    pattern = r'^\+?[0-9\s]*$'
    return re.match(pattern, phone)

def extract_date(query):
    try:
        # Attempt to parse date from user query
        date = parse(query, fuzzy=True)
        return date.strftime('%Y-%m-%d')
    except Exception:
        return None
