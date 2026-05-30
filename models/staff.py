from datetime import datetime
from models.personne import Personne


# all the roles that exist in the clinic
STAFF_ROLES = (
    "nurse",
    "midwife",
    "lab_technician",
    "pharmacist",
    "cashier",
    "receptionist",
    "care_assistant",
    "administrator"
)

# shift types with start and end times
# each one is a tuple of (name, start, end)
SHIFT_TYPES = (
    ("morning", "07:30", "13:30"),
    ("afternoon", "13:30", "19:30"),
    ("night", "19:30", "07:30"),
    ("full_day", "08:00", "17:00")
)


class Personnel(Personne):
    """
    Represents a non-doctor staff member in SanteConnect BF.
    Inherits from Personne.
    """

    # counter for generating staff ids
    _staff_counter = 0

    def __init__(self, last_name, first_name, date_of_birth, gender, phone, role, hire_date=""):
        """
        Creates a new staff member.

        Args:
            last_name (str): family name
            first_name (str): first name
            date_of_birth (str): DD/MM/YYYY
            gender (str): M or F
            phone (str): 8 digits
            role (str): job role in the clinic
            hire_date (str): when they were hired, optional
        """
        # call parent init
        super().__init__(last_name, first_name, date_of_birth, gender, phone)

        # unique staff id
        Personnel._staff_counter = Personnel._staff_counter + 1
        self.staff_id = "PER-" + str(Personnel._staff_counter).zfill(3)

        self.role = role.lower()

        # if no hire date given use today
        if hire_date == "":
            self.hire_date = datetime.now().strftime("%d/%m/%Y")
        else:
            self.hire_date = hire_date

        # default shift is full day
        self.shift = {
            "shift_name": "full_day",
            "start_time": "08:00",
            "end_time": "17:00"
        }

        # is this person currently working or not
        self.is_active = True

        # list of leave periods
        self.leave_records = []

        # number of times absent without notice
        self.absence_count = 0

    def display_info(self):
        """
        Prints staff member info.
        This is the polymorphism part - different from Patient and Medecin versions.
        """
        print("=" * 50)
        print("STAFF PROFILE - SanteConnect BF")
        print("=" * 50)
        print("Staff ID     : " + self.staff_id)
        print("Full Name    : " + self.get_full_name())
        print("Role         : " + self.role.replace("_", " ").title())
        print("Age          : " + str(self.calculate_age()) + " years old")
        print("Phone        : " + self.get_phone())
        print("Hire Date    : " + self.hire_date)

        if self.is_active:
            print("Status       : Active")
        else:
            print("Status       : Inactive")

        print("Shift        : " + self.shift["shift_name"] + " (" + self.shift["start_time"] + " - " + self.shift["end_time"] + ")")
        print("Absences     : " + str(self.absence_count))

        # print leave history if any
        if len(self.leave_records) > 0:
            print("Leave History:")
            for record in self.leave_records:
                print("  From " + record["start"] + " to " + record["end"] + " - " + record["reason"])

        print("=" * 50)

    def set_shift(self, shift_name):
        """
        Changes the shift for this staff member.

        Args:
            shift_name (str): morning, afternoon, night or full_day

        Returns:
            bool: True if changed, False if shift name not found
        """
        # go through the shift types and find the matching one
        for shift in SHIFT_TYPES:
            name, start, end = shift
            if name == shift_name:
                self.shift["shift_name"] = name
                self.shift["start_time"] = start
                self.shift["end_time"] = end
                print("[OK] Shift updated to " + shift_name + " for " + self.get_full_name())
                return True

        print("[ERROR] Shift type not found: " + shift_name)
        return False

    def record_leave(self, start_date, end_date, reason):
        """
        Records a leave period for this staff member.

        Args:
            start_date (str): when leave starts DD/MM/YYYY
            end_date (str): when leave ends DD/MM/YYYY
            reason (str): why they are on leave
        """
        leave_entry = {
            "start": start_date,
            "end": end_date,
            "reason": reason
        }
        self.leave_records.append(leave_entry)
        self.is_active = False
        print("[OK] Leave recorded for " + self.get_full_name() + " from " + start_date + " to " + end_date)

    def return_to_duty(self):
        """Marks the staff member as active again."""
        self.is_active = True
        print("[OK] " + self.get_full_name() + " is back on duty.")

    def record_absence(self):
        """Adds one absence to the count."""
        self.absence_count = self.absence_count + 1
        print("[INFO] Absence recorded for " + self.get_full_name() + ". Total: " + str(self.absence_count))

    def calculate_seniority(self):
        """
        Calculates how many years this person has worked here.

        Returns:
            int: number of years, 0 if date is wrong
        """
        try:
            day, month, year = self.hire_date.split("/")
            return datetime.now().year - int(year)
        except:
            return 0

    def to_dict(self):
        """
        Converts staff data to dictionary for JSON saving.

        Returns:
            dict: all staff data
        """
        data = {
            "staff_id": self.staff_id,
            "last_name": self.get_last_name(),
            "first_name": self.get_first_name(),
            "date_of_birth": self.get_date_of_birth(),
            "gender": self.get_gender(),
            "phone": self.get_phone(),
            "role": self.role,
            "hire_date": self.hire_date,
            "shift": self.shift,
            "is_active": self.is_active,
            "leave_records": self.leave_records,
            "absence_count": self.absence_count
        }
        return data

    def __str__(self):
        """Short description of the staff member."""
        if self.is_active:
            status = "Active"
        else:
            status = "Inactive"
        return self.get_full_name() + " [" + self.role + "] - " + status
