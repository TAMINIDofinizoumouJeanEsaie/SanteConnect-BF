"""
validation.py
This file contains functions to check user inputs.
We use these functions everywhere in the project to make sure
the user types the right thing.
"""

# List of blood groups that exist
BLOOD_GROUPS = ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')

# Phone numbers in Burkina Faso have 8 digits
PHONE_LENGTH = 8

# Valid starting digits for Burkina Faso phone numbers
VALID_PREFIXES = ('0', '5', '6', '7')


def validate_phone(phone):
    """Check if a phone number is valid (Burkina Faso format)."""

    # Remove spaces and dashes just in case the user added them
    phone = phone.strip().replace(' ', '').replace('-', '')

    # Phone must only contain numbers
    if not phone.isdigit():
        return False

    # Phone must have exactly 8 digits
    if len(phone) != PHONE_LENGTH:
        return False

    # Phone must start with 0, 5, 6 or 7
    if phone[0] not in VALID_PREFIXES:
        return False

    # If we get here, the phone number is good
    return True


def validate_date(date_str):
    """Check if a date is written in the right format (DD/MM/YYYY)."""

    from datetime import datetime

    date_str = date_str.strip()

    # We try to convert the string into a real date
    # If it fails, the format is wrong
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def validate_blood_group(blood_group):
    """Check if a blood group is one of the known ones."""

    # We just check if the value is in our list
    return blood_group.strip().upper() in BLOOD_GROUPS


def validate_email(email):
    """Check if an email address looks correct."""

    email = email.strip()

    # An email needs an @ symbol
    if '@' not in email:
        return False

    # Split the email at the @ sign
    parts = email.split('@')

    # There must be exactly two parts: before and after @
    if len(parts) != 2:
        return False

    # The part after @ must have a dot (like gmail.com)
    if '.' not in parts[1]:
        return False

    return True


def get_integer_input(message, min_val, max_val):
    """Ask the user to type a number and keep asking until they type a valid one."""

    # We use a while loop so we keep asking if the input is wrong
    while True:
        user_input = input(message).strip()

        # Check that what the user typed is actually a number
        if not user_input.lstrip('-').isdigit():
            print("Please type a whole number.")
            continue

        # Convert the string to an integer
        value = int(user_input)

        # Check that the number is inside the allowed range
        if value < min_val or value > max_val:
            print(f"The number must be between {min_val} and {max_val}.")
            continue

        # The input is valid, we can return it
        return value


def get_float_input(message, min_val=0.0, max_val=9999999.0):
    """Ask the user to type a decimal number and keep asking until it is valid."""

    while True:
        # Replace comma with dot so both work (some people type 1,5 instead of 1.5)
        user_input = input(message).strip().replace(',', '.')

        # Try to convert to a float
        try:
            value = float(user_input)
        except ValueError:
            print("Please type a valid number.")
            continue

        # Check the range
        if value < min_val or value > max_val:
            print(f"The number must be between {min_val} and {max_val}.")
            continue

        return value


def get_non_empty_string(message, max_length=100):
    """Ask the user to type something and make sure they did not leave it empty."""

    while True:
        user_input = input(message).strip()

        # We do not accept empty answers
        if not user_input:
            print("This field cannot be empty.")
            continue

        # We do not accept very long answers either
        if len(user_input) > max_length:
            print(f"Too long. Maximum {max_length} characters.")
            continue

        return user_input


def validate_username(username):
    """Check if a username only uses letters, numbers and underscores."""

    username = username.strip()

    # Username must be between 3 and 20 characters
    if len(username) < 3 or len(username) > 20:
        return False

    # Go through each character and check it is allowed
    for char in username:
        if not (char.isalnum() or char == '_'):
            return False

    return True
