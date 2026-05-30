"""
main.py
This is the main file of SanteConnect BF.
Run this file to start the program: python main.py

It shows the login screen, then the main menu,
and sends the user to the right section depending on their choice.
"""

import os
import sys

# We import the display functions from our formatage file
from utils.formatage import (
    display_title,
    display_subtitle,
    display_success,
    display_error,
    display_warning,
    display_info,
    display_menu,
    display_app_header,
    display_separator,
    wait_for_user,
    confirm_action,
    BLUE, GREEN, RED, CYAN, RESET, BOLD
)

# We import the helper functions we need
from utils.validation import get_integer_input
from utils.date_utils import today, timestamp

# Basic info about the app
VERSION     = "1.0.0"
CLINIC_NAME = "SanteConnect BF"
AUTHORS     = ("Member 1", "Member 2", "Member 3", "Member 4")


def patient_menu(logged_in_user):
    """Show the patient management menu and handle the user's choice."""

    patient_options = {
        "1": "Register a new patient",
        "2": "Search for a patient",
        "3": "Edit a patient record",
        "4": "View patient visit history",
        "5": "Export patient record",
        "0": "Back to main menu"
    }

    # Keep showing the menu until the user chooses to go back
    while True:
        display_menu("PATIENT MANAGEMENT", patient_options)
        choice = input(f"  {CYAN}Your choice: {RESET}").strip()

        if choice == "1":
            display_subtitle("Register a new patient")
            display_info("Module being integrated - Member 1.")
            wait_for_user()

        elif choice == "2":
            display_subtitle("Search for a patient")
            display_info("Module being integrated - Member 1.")
            wait_for_user()

        elif choice == "3":
            display_subtitle("Edit a patient record")
            display_info("Module being integrated - Member 1.")
            wait_for_user()

        elif choice == "4":
            display_subtitle("Visit history")
            display_info("Module being integrated - Member 1.")
            wait_for_user()

        elif choice == "5":
            display_subtitle("Export patient record")
            display_info("Module being integrated - Member 3.")
            wait_for_user()

        elif choice == "0":
            # Go back to the main menu
            break

        else:
            display_error("Invalid choice. Please enter a number from the menu.")
            wait_for_user()


def consultation_menu(logged_in_user):
    """Show the consultations menu and handle the user's choice."""

    consultation_options = {
        "1": "Record a new consultation",
        "2": "Enter vital signs",
        "3": "View consultation history",
        "4": "Generate a prescription",
        "5": "Close a consultation",
        "0": "Back to main menu"
    }

    while True:
        display_menu("MEDICAL CONSULTATIONS", consultation_options)
        choice = input(f"  {CYAN}Your choice: {RESET}").strip()

        if choice == "1":
            display_subtitle("New consultation")
            display_info("Module being integrated - Member 2.")
            wait_for_user()

        elif choice == "2":
            display_subtitle("Vital signs entry")
            display_info("Blood pressure, temperature, weight, height, HR, SpO2...")
            display_info("Module being integrated - Member 2.")
            wait_for_user()

        elif choice == "3":
            display_subtitle("Consultation history")
            display_info("Module being integrated - Member 2.")
            wait_for_user()

        elif choice == "4":
            display_subtitle("Generate prescription")
            display_info("Module being integrated - Member 2.")
            wait_for_user()

        elif choice == "5":
            display_subtitle("Close a consultation")
            display_info("Module being integrated - Member 2.")
            wait_for_user()

        elif choice == "0":
            break

        else:
            display_error("Invalid choice. Please enter a number from the menu.")
            wait_for_user()


def pharmacy_menu(logged_in_user):
    """Show the pharmacy menu and handle the user's choice."""

    pharmacy_options = {
        "1": "View medicine stock",
        "2": "Add a medicine to the catalogue",
        "3": "Update stock",
        "4": "Stock and expiry alerts",
        "5": "Dispense on prescription",
        "0": "Back to main menu"
    }

    while True:
        display_menu("PHARMACY & STOCK", pharmacy_options)
        choice = input(f"  {CYAN}Your choice: {RESET}").strip()

        if choice == "1":
            display_subtitle("Medicine stock")
            display_info("Module being integrated - Member 2.")
            wait_for_user()

        elif choice == "2":
            display_subtitle("Add a medicine")
            display_info("Module being integrated - Member 2.")
            wait_for_user()

        elif choice == "3":
            display_subtitle("Update stock")
            display_info("Module being integrated - Member 2.")
            wait_for_user()

        elif choice == "4":
            display_subtitle("Active alerts")
            display_warning("Checking low stock and upcoming expiry dates...")
            display_info("Module being integrated - Member 2.")
            wait_for_user()

        elif choice == "5":
            display_subtitle("Dispensing on prescription")
            display_info("Module being integrated - Member 2.")
            wait_for_user()

        elif choice == "0":
            break

        else:
            display_error("Invalid choice. Please enter a number from the menu.")
            wait_for_user()


def billing_menu(logged_in_user):
    """Show the billing menu and handle the user's choice."""

    billing_options = {
        "1": "Create a new invoice",
        "2": "Record a payment",
        "3": "View unpaid invoices",
        "4": "Generate a receipt",
        "5": "Daily cash report",
        "0": "Back to main menu"
    }

    while True:
        display_menu("BILLING & CASHIER", billing_options)
        choice = input(f"  {CYAN}Your choice: {RESET}").strip()

        if choice in ("1", "2", "3", "4", "5"):
            display_info("Module being integrated - Member 3.")
            wait_for_user()

        elif choice == "0":
            break

        else:
            display_error("Invalid choice. Please enter a number from the menu.")
            wait_for_user()


def reports_menu(logged_in_user):
    """Show the reports menu and handle the user's choice."""

    report_options = {
        "1": "Medical report (consultations, diseases)",
        "2": "Financial report (revenue, cash)",
        "3": "Epidemiological statistics",
        "4": "Export data to CSV",
        "0": "Back to main menu"
    }

    while True:
        display_menu("REPORTS & STATISTICS", report_options)
        choice = input(f"  {CYAN}Your choice: {RESET}").strip()

        if choice in ("1", "2", "3", "4"):
            display_info("Module being integrated - Member 3.")
            wait_for_user()

        elif choice == "0":
            break

        else:
            display_error("Invalid choice. Please enter a number from the menu.")
            wait_for_user()


def staff_menu(logged_in_user):
    """Show the staff management menu and handle the user's choice."""

    staff_options = {
        "1": "View staff list",
        "2": "Add a staff member",
        "3": "Edit a staff profile",
        "4": "On-call schedule",
        "0": "Back to main menu"
    }

    while True:
        display_menu("STAFF MANAGEMENT", staff_options)
        choice = input(f"  {CYAN}Your choice: {RESET}").strip()

        if choice in ("1", "2", "3", "4"):
            display_info("Module being integrated - Member 1.")
            wait_for_user()

        elif choice == "0":
            break

        else:
            display_error("Invalid choice. Please enter a number from the menu.")
            wait_for_user()


def backup_menu(logged_in_user):
    """Show the backup menu and handle the user's choice."""

    backup_options = {
        "1": "Manual backup now",
        "2": "Check data integrity",
        "3": "Restore from a backup",
        "4": "View audit log",
        "0": "Back to main menu"
    }

    while True:
        display_menu("BACKUP & SECURITY", backup_options)
        choice = input(f"  {CYAN}Your choice: {RESET}").strip()

        if choice in ("1", "2", "3", "4"):
            display_info("Module being integrated - Member 3.")
            wait_for_user()

        elif choice == "0":
            break

        else:
            display_error("Invalid choice. Please enter a number from the menu.")
            wait_for_user()


def login_screen():
    """
    Show the login screen.
    The user has 3 attempts to enter the right username and password.
    Returns the username if login works, or empty string if it fails.
    """

    display_title("SYSTEM LOGIN")

    # Maximum number of tries before we block access
    MAX_ATTEMPTS = 3
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        # Show how many tries are left
        remaining = MAX_ATTEMPTS - attempts
        print(f"  Attempts remaining: {BLUE}{remaining}{RESET}\n")

        username = input(f"  {CYAN}Username: {RESET}").strip()
        password = input(f"  {CYAN}Password: {RESET}").strip()

        # Check if the username and password are correct
        # For now we use admin/admin123 for testing
        # Later this will be replaced by the real auth module from Member 1
        if username == "admin" and password == "admin123":
            display_success(f"Welcome, {username}!")
            print(f"  Login time: {timestamp()}")
            wait_for_user()
            return username

        else:
            attempts += 1
            display_error("Wrong username or password.")
            print()

    # If we reach here, the user failed 3 times
    display_error("Access blocked. Please contact the administrator.")
    return ""


def initialise_system():
    """Create the folders the app needs if they do not exist yet."""

    # List of folders we need
    required_folders = ['data', 'logs', 'backups', 'models', 'services', 'utils']

    for folder in required_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)


def main_menu(logged_in_user):
    """
    Show the main menu of the application.
    This is the central hub - from here the user can go anywhere.
    We use a while loop to keep the menu open until the user quits.
    """

    main_options = {
        "1": "Patient Management",
        "2": "Medical Consultations",
        "3": "Pharmacy & Stock",
        "4": "Billing & Cashier",
        "5": "Reports & Statistics",
        "6": "Staff Management",
        "7": "Backup & Security",
        "0": "Quit SanteConnect BF"
    }

    # This loop keeps running until the user chooses to quit
    while True:
        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Show the header with the user's name and today's date
        display_app_header(CLINIC_NAME, VERSION, logged_in_user)
        print(f"  Date: {GREEN}{today()}{RESET}\n")

        # Show the menu
        display_menu("MAIN MENU", main_options)

        choice = input(f"  {CYAN}Your choice: {RESET}").strip()

        # We use try/except to handle unexpected crashes without closing the app
        try:
            if choice == "1":
                patient_menu(logged_in_user)

            elif choice == "2":
                consultation_menu(logged_in_user)

            elif choice == "3":
                pharmacy_menu(logged_in_user)

            elif choice == "4":
                billing_menu(logged_in_user)

            elif choice == "5":
                reports_menu(logged_in_user)

            elif choice == "6":
                staff_menu(logged_in_user)

            elif choice == "7":
                backup_menu(logged_in_user)

            elif choice == "0":
                # Ask the user to confirm before quitting
                if confirm_action("Are you sure you want to quit?"):
                    display_success(f"Goodbye, {logged_in_user}!")
                    print(f"  Logout time: {timestamp()}")
                    display_separator()
                    break

            else:
                display_error("Invalid option. Choose a number between 0 and 7.")
                wait_for_user()

        except KeyboardInterrupt:
            # This happens when the user presses Ctrl+C
            print("\n")
            display_warning("You pressed Ctrl+C.")
            if confirm_action("Do you want to quit?"):
                break

        except Exception as error:
            # Something unexpected happened - show the error but do not crash
            display_error(f"Something went wrong: {error}")
            wait_for_user()


# This is where the program starts
# The "if __name__" check makes sure this only runs when we execute main.py directly
if __name__ == '__main__':
    # Clear the screen first
    os.system('cls' if os.name == 'nt' else 'clear')

    # Show the welcome screen
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{BOLD}{'SanteConnect BF'.center(60)}{RESET}")
    print(f"{CYAN}{'Integrated Clinic Management System'.center(60)}{RESET}")
    print(f"{CYAN}{f'Version {VERSION}'.center(60)}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}")
    print(f"\n  {today()} - Burkina Institute of Technology")
    print(f"  Course 3PRG1205 - Programming I with Python\n")
    display_separator()

    # Set up the folders
    initialise_system()

    # Show the login screen and get the username
    user = login_screen()

    # If login was successful, open the main menu
    if user:
        main_menu(user)
    else:
        display_error("Could not log in. The program will close.")
        sys.exit(1)

