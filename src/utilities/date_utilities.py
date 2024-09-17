from datetime import datetime, timedelta
import dateparser

def parse_date(input_text: str) -> str:
    """
    Parses a date from natural language text input.

    This function handles specific cases like 'next Monday', 'tomorrow', 
    'next Friday' and falls back to using the dateparser library for other formats.

    Args:
        input_text (str): Natural language date input.

    Returns:
        str: The parsed date in 'YYYY-MM-DD' format, or 'Invalid date' if parsing fails.
    """
    today = datetime.today()
    input_text = input_text.lower()

    special_cases = {
        "next monday": 7 - today.weekday() + 0,  # Monday is 0
        "next friday": 7 - today.weekday() + 4,  # Friday is 4
        "tomorrow": 1
    }

    for case, days_ahead in special_cases.items():
        if case in input_text:
            return (today + timedelta(days=(days_ahead % 7 + 7))).strftime('%Y-%m-%d')

    # Use dateparser for other natural language date formats
    parsed_date = dateparser.parse(input_text, settings={'PREFER_DATES_FROM': 'future'})
    
    return parsed_date.strftime('%Y-%m-%d') if parsed_date else "Invalid date"
