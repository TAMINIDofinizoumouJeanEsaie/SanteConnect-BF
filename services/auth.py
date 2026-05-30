import hashlib
import json
import os
from datetime import datetime


# where we save the user accounts
USERS_FILE = "data/users.json"

# roles that are allowed in the system
ALLOWED_ROLES = ("admin", "doctor", "nurse", "cashier", "pharmacist")

# how many wrong attempts before locking the account
MAX_ATTEMPTS = 3


def hash_password(password):
    """
    Converts a password to a hash so we never store it in plain text.

    Args:
        password (str): the real password

    Returns:
        str: the hashed version
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users():
    """
    Loads all users from the JSON file.

    Returns:
        dict: all users, empty dict if file doesnt exist
    """
    if not os.path.exists(USERS_FILE):
        return {}

    try:
        file = open(USERS_FILE, "r", encoding="utf-8")
        data = json.load(file)
        file.close()
        return data
    except:
        print("[ERROR] Could not read users file.")
        return {}


def save_users(users):
    """
    Saves all users to the JSON file.

    Args:
        users (dict): the users dictionary to save

    Returns:
        bool: True if saved ok, False if not
    """
    try:
        # create the data folder if it doesnt exist
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        file = open(USERS_FILE, "w", encoding="utf-8")
        json.dump(users, file, indent=4, ensure_ascii=False)
        file.close()
        return True
    except:
        print("[ERROR] Could not save users file.")
        return False


def create_user(username, password, role):
    """
    Creates a new user account.

    Args:
        username (str): the login name
        password (str): the password in plain text
        role (str): what role this user has

    Returns:
        bool: True if created, False if something went wrong
    """
    # check the role is allowed
    if role not in ALLOWED_ROLES:
        print("[ERROR] Role not allowed: " + role)
        return False

    users = load_users()

    # check username is not already taken
    if username in users:
        print("[ERROR] Username already exists: " + username)
        return False

    # password needs to be at least 6 characters
    if len(password) < 6:
        print("[ERROR] Password too short. Minimum 6 characters.")
        return False

    # save the user with hashed password
    users[username] = {
        "password_hash": hash_password(password),
        "role": role,
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "is_locked": False,
        "failed_attempts": 0
    }

    if save_users(users):
        print("[OK] User created: " + username + " with role " + role)
        return True
    return False


def login(username, password):
    """
    Tries to log in with given username and password.

    Args:
        username (str): the username to check
        password (str): the password to check

    Returns:
        bool: True if login worked, False if not
    """
    users = load_users()

    # check username exists
    if username not in users:
        print("[ERROR] Username not found: " + username)
        return False

    user = users[username]

    # check if account is locked
    if user["is_locked"] == True:
        print("[LOCKED] This account is locked. Contact your admin.")
        return False

    # compare the passwords using hash
    if hash_password(password) == user["password_hash"]:
        # reset failed attempts on success
        users[username]["failed_attempts"] = 0
        save_users(users)
        print("[OK] Login successful. Welcome " + username + " (" + user["role"] + ")")
        return True
    else:
        # wrong password, add 1 to failed attempts
        users[username]["failed_attempts"] = users[username]["failed_attempts"] + 1
        failed = users[username]["failed_attempts"]
        remaining = MAX_ATTEMPTS - failed

        if failed >= MAX_ATTEMPTS:
            users[username]["is_locked"] = True
            save_users(users)
            print("[LOCKED] Account locked after " + str(MAX_ATTEMPTS) + " failed attempts.")
        else:
            save_users(users)
            print("[ERROR] Wrong password. " + str(remaining) + " attempt(s) left.")

        return False


def get_role(username):
    """
    Returns the role of a user.

    Args:
        username (str): the username to look up

    Returns:
        str: the role, or empty string if not found
    """
    users = load_users()

    if username in users:
        return users[username]["role"]

    return ""


def login_menu():
    """
    Shows a login screen in the terminal.
    Uses a while loop to let the user try again if they fail.

    Returns:
        tuple: (username, role) if login works, ("", "") if all attempts fail
    """
    print("=" * 45)
    print("SANTECONNECT BF - System Login")
    print("=" * 45)

    attempts = 0
    logged_in = False

    # keep trying until logged in or out of attempts
    while logged_in == False and attempts < MAX_ATTEMPTS:
        print("Attempt " + str(attempts + 1) + " of " + str(MAX_ATTEMPTS))
        username = input("Username : ").strip()
        password = input("Password : ").strip()

        if login(username, password):
            logged_in = True
            role = get_role(username)
            return (username, role)
        else:
            attempts = attempts + 1

    print("[EXIT] Too many failed attempts. Goodbye.")
    return ("", "")


def reset_password(username, new_password, admin_username):
    """
    Resets a user password. Only admins can do this.

    Args:
        username (str): account to reset
        new_password (str): the new password
        admin_username (str): who is doing the reset

    Returns:
        bool: True if done, False if not allowed
    """
    users = load_users()

    if admin_username not in users:
        print("[ERROR] Admin not found.")
        return False

    if users[admin_username]["role"] != "admin":
        print("[DENIED] Only admins can reset passwords.")
        return False

    if username not in users:
        print("[ERROR] User not found: " + username)
        return False

    if len(new_password) < 6:
        print("[ERROR] New password too short.")
        return False

    users[username]["password_hash"] = hash_password(new_password)
    users[username]["is_locked"] = False
    users[username]["failed_attempts"] = 0

    if save_users(users):
        print("[OK] Password reset for " + username + " by " + admin_username)
        return True
    return False
