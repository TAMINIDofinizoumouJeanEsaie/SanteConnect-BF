"""
date_utils.py
This file contains functions to work with dates.
We use it to calculate ages, check if a medicine is expired,
get today's date, and other date-related things.
"""

# We import datetime so we can work with dates in Python
from datetime import datetime, date


# The format we use for dates everywhere in the app
DATE_FORMAT = "%d/%m/%Y"

# Format when we also want to show the time (for logs)
TIMESTAMP_FORMAT = "%d/%m/%Y at %H:%M"

# Format used for backup file names (no spaces or slashes)
FILE_NAME_FORMAT = "%Y%m%d_%H%M%S"

# We show an alert if a medicine expires in less than 90 days
EXPIRY_ALERT_THRESHOLD = 90


def today():
    """Return today's date as a string like 27/05/2026."""
    return datetime.now().strftime(DATE_FORMAT)


def timestamp():
    """Return the current date and time as a string. Used for logs."""
    return datetime.now().strftime(TIMESTAMP_FORMAT)


def file_timestamp():
    """Return the current time in a format good for file names."""
    return datetime.now().strftime(FILE_NAME_FORMAT)


def calculate_age(date_of_birth):
    """Calculate how old someone is based on their date of birth."""

    # Try to convert the string into a real date object
    try:
        birth = datetime.strptime(date_of_birth, DATE_FORMAT)
        today_date = date.today()

        # Start by just subtracting the years
        age = today_date.year - birth.year

        # Check if their birthday has already happened this year
        # If not, we subtract 1 because they are not yet that age
        birthday_happened = (
            (today_date.month, today_date.day) >= (birth.month, birth.day)
        )
        if not birthday_happened:
            age -= 1

        return age

    except ValueError:
        # If the date format is wrong, we return -1 to signal an error
        return -1


def days_until_expiry(expiry_date):
    """Return how many days are left before a medicine expires."""

    try:
        # Convert the expiry date string into a date object
        expiry = datetime.strptime(expiry_date, DATE_FORMAT)

        # Get today's date without hours/minutes
        today_dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Subtract today from the expiry date
        delta = expiry - today_dt

        # delta.days is negative if the medicine is already expired
        return delta.days

    except ValueError:
        return -9999


def is_expired(expiry_date):
    """Return True if a medicine is already expired."""

    days = days_until_expiry(expiry_date)

    # If days is 0 or negative, it is expired
    return days <= 0


def expiry_alert(expiry_date):
    """Return True if a medicine will expire in less than 90 days."""

    days = days_until_expiry(expiry_date)

    # Between 1 and 90 days means we should show an alert
    return 0 < days <= EXPIRY_ALERT_THRESHOLD


def format_date_long(date_str):
    """Convert a date like 15/03/2000 into a readable text like 15 March 2000."""

    # Dictionary that maps month numbers to month names
    months = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }

    try:
        d = datetime.strptime(date_str, DATE_FORMAT)
        return f"{d.day} {months[d.month]} {d.year}"
    except ValueError:
        # If the date is wrong, just return what was given
        return date_str


def date_in_x_days(num_days):
    """Return the date that will be in a certain number of days from today."""

    from datetime import timedelta

    # timedelta lets us add days to a date
    future = datetime.now() + timedelta(days=num_days)
    return future.strftime(DATE_FORMAT)


def compare_dates(date1, date2):
    """
    Compare two dates.
    Returns -1 if date1 is before date2.
    Returns  0 if they are the same.
    Returns  1 if date1 is after date2.
    Returns -9999 if one of the dates is invalid.
    """

    try:
        d1 = datetime.strptime(date1, DATE_FORMAT)
        d2 = datetime.strptime(date2, DATE_FORMAT)

        if d1 < d2:
            return -1
        elif d1 == d2:
            return 0
        else:
            return 1

    except ValueError:
        return -9999


def generate_unique_id(prefix="SC"):
    """Generate a unique ID using the current time. Example: SC-20260527-143512-847."""

    import random

    # Use the current time to make the ID unique
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Add a random number at the end in case two IDs are created at the same second
    suffix = random.randint(100, 999)

    return f"{prefix}-{ts}-{suffix}"

