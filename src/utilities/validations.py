import re
from datetime import datetime
from dateutil.parser import parse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Validate an email address using a regular expression.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def validate_phone_number(phone_number: str) -> bool:
    """
    Validate a phone number using a regular expression.

    Args:
        phone_number (str): The phone number to validate.

    Returns:
        bool: True if the phone number is valid, False otherwise.
    """
    return re.match(r"^\+?[1-9]\d{1,14}$", phone_number) is not None

class User(BaseModel):
    """
    A Pydantic model to represent a user, including name, phone number, and email.

    Attributes:
        name (str): The name of the user.
        phone_number (str): The phone number of the user, validated by regex.
        email (EmailStr): The email address of the user, validated by Pydantic's EmailStr.
    """
    name: str
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')
    email: EmailStr

def extract_date(query: str) -> Optional[str]:
    """
    Extract a date from a given query string using natural language parsing.

    Args:
        query (str): The query string to extract a date from.

    Returns:
        Optional[str]: The extracted date in 'YYYY-MM-DD' format, or None if no valid date is found.
    """
    try:
        # Attempt to parse date from user query
        date = parse(query, fuzzy=True)
        return date.strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return None

# Example usage:
if __name__ == "__main__":
    # Validate email and phone number
    email = "test@example.com"
    phone = "+1234567890"
    print(validate_email(email))  # True
    print(validate_phone_number(phone))  # True

    # Create a user instance
    user = User(name="John Doe", phone_number=phone, email=email)
    print(user)

    # Extract date from a query
    query = "Can we schedule a meeting on October 15th?"
    extracted_date = extract_date(query)
    print(f"Extracted Date: {extracted_date}")
