"""
formatting.py
This file handles everything related to displaying things in the terminal.
Colors, titles, tables, menus, error messages, etc.
"""

# These are color codes for the terminal
# We put them in variables so we can reuse them easily
RED    = '\033[91m'
GREEN  = '\033[92m'
YELLOW = '\033[93m'
BLUE   = '\033[94m'
CYAN   = '\033[96m'
BOLD   = '\033[1m'
RESET  = '\033[0m'   # This resets the color back to normal

# How wide we want the display to be
TERMINAL_WIDTH = 60


def display_title(title, symbol='='):
    """Display a big title with lines above and below it."""

    # Create a full line of the symbol (like ========)
    line = symbol * TERMINAL_WIDTH

    # Center the title text
    centred_title = title.upper().center(TERMINAL_WIDTH)

    print(f"\n{BLUE}{BOLD}{line}{RESET}")
    print(f"{BLUE}{BOLD}{centred_title}{RESET}")
    print(f"{BLUE}{BOLD}{line}{RESET}\n")


def display_subtitle(title):
    """Display a smaller title with dashes."""

    line = '-' * TERMINAL_WIDTH
    print(f"\n{CYAN}{line}")
    print(f"  {title}")
    print(f"{line}{RESET}")


def display_success(message):
    """Display a success message in green."""
    print(f"{GREEN}  [OK] {message}{RESET}")


def display_error(message):
    """Display an error message in red."""
    print(f"{RED}  [ERROR] {message}{RESET}")


def display_warning(message):
    """Display a warning message in yellow."""
    print(f"{YELLOW}  [WARNING] {message}{RESET}")


def display_info(message):
    """Display a simple info message."""
    print(f"  [INFO] {message}")


def display_table(headers, rows):
    """Display data in a table with columns."""

    # Make sure we have headers
    if not headers:
        display_error("No headers given for the table.")
        return

    # Start by setting column widths equal to the header length
    col_widths = [len(str(h)) for h in headers]

    # Go through every row and every cell to find the longest value
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    # Build the separator line between rows
    separator = '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'

    # Print the top separator
    print(f"\n{CYAN}{separator}{RESET}")

    # Print the header row
    header_line = '|'
    for i, h in enumerate(headers):
        header_line += f" {BOLD}{str(h).ljust(col_widths[i])}{RESET}{CYAN} |"
    print(f"{CYAN}{header_line}{RESET}")

    # Print the separator after headers
    print(f"{CYAN}{separator}{RESET}")

    # Print each data row
    for row in rows:
        row_str = '|'
        for i, cell in enumerate(row):
            if i < len(col_widths):
                row_str += f" {str(cell).ljust(col_widths[i])} |"
        print(row_str)

    # Print the bottom separator
    print(f"{CYAN}{separator}{RESET}\n")


def display_menu(title, options):
    """Display a menu with numbered options."""

    display_title(title)

    # Loop through all the options and print them
    for key, value in options.items():
        # Option 0 is always the exit/back option, we show it in red
        if key == "0":
            print(f"  {RED}[{key}]{RESET}  {value}")
        else:
            print(f"  {CYAN}[{key}]{RESET}  {value}")

    print()


def display_separator(symbol='-', width=TERMINAL_WIDTH):
    """Print a simple line across the screen."""
    print(symbol * width)


def display_app_header(clinic_name, version, logged_in_user):
    """Display the header at the top of the screen with app info."""

    line = '=' * TERMINAL_WIDTH
    print(f"\n{BLUE}{BOLD}{line}{RESET}")
    print(f"{BLUE}{BOLD}{'SanteConnect BF'.center(TERMINAL_WIDTH)}{RESET}")
    print(f"{CYAN}{'Integrated Clinic Management System'.center(TERMINAL_WIDTH)}{RESET}")
    print(f"{BLUE}{BOLD}{line}{RESET}")
    print(f"  Version: {GREEN}{version}{RESET}    |    User: {GREEN}{logged_in_user}{RESET}")
    print(f"{BLUE}{line}{RESET}\n")


def confirm_action(message):
    """Ask the user to confirm something by typing Y or N."""

    answer = input(f"{YELLOW}  ? {message} (Y/N): {RESET}").strip().lower()

    # Return True if they said yes
    return answer in ('y', 'yes')


def wait_for_user():
    """Wait for the user to press Enter before continuing."""
    input(f"\n{CYAN}  Press Enter to continue...{RESET}")
