from datetime import datetime
from models.personne import Personne


# blood groups we accept in the system
BLOOD_GROUPS = ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown")

# possible statuses for a patient file
PATIENT_STATUSES = ("active", "archived", "deceased", "transferred")


class Patient(Personne):
    """
    Represents a patient in SanteConnect BF.
    Inherits from Personne.
    """

    # this counter helps us give each patient a unique file number
    _file_counter = 142

    def __init__(self, last_name, first_name, date_of_birth, gender, phone, blood_group="Unknown"):
        """
        Creates a new patient.

        Args:
            last_name (str): family name
            first_name (str): first name
            date_of_birth (str): DD/MM/YYYY
            gender (str): M or F
            phone (str): 8 digits
            blood_group (str): blood group, default is Unknown
        """
        # call the parent class init first
        super().__init__(last_name, first_name, date_of_birth, gender, phone)

        # generate file id for this patient
        Patient._file_counter = Patient._file_counter + 1
        year = datetime.now().year
        self.file_id = "BF-" + str(year) + "-" + str(Patient._file_counter).zfill(5)

        # set blood group
        if blood_group in BLOOD_GROUPS:
            self.blood_group = blood_group
        else:
            self.blood_group = "Unknown"

        # list of allergies the patient has
        self.allergies = []

        # list of chronic conditions
        self.chronic_conditions = []

        # visit history stored as list of tuples
        self.visit_history = []

        # vaccines the patient got stored as a dictionary
        self.vaccination_status = {}

        # current status of the file
        self.status = "active"

    def display_info(self):
        """
        Prints all the patient info to the screen.
        This is the polymorphism part - Patient has its own version of this.
        """
        print("=" * 50)
        print("PATIENT FILE - SanteConnect BF")
        print("=" * 50)
        print("File Number  : " + self.file_id)
        print("Full Name    : " + self.get_full_name())
        print("Age          : " + str(self.calculate_age()) + " years old")

        # check gender to print something readable
        if self.get_gender() == "M":
            print("Gender       : Male")
        else:
            print("Gender       : Female")

        print("Date of birth: " + self.get_date_of_birth())
        print("Phone        : " + self.get_phone())
        print("Blood Group  : " + self.blood_group)
        print("Status       : " + self.status.upper())

        # print allergies if there are any
        if len(self.allergies) > 0:
            print("Allergies:")
            for allergy in self.allergies:
                print("  - " + allergy)
        else:
            print("Allergies    : None")

        # print chronic conditions
        if len(self.chronic_conditions) > 0:
            print("Chronic Conditions:")
            for condition in self.chronic_conditions:
                print("  - " + condition)

        print("Total Visits : " + str(len(self.visit_history)))
        print("=" * 50)

    def add_medical_history(self, entry_type, description):
        """
        Adds an allergy or chronic condition to the patient record.

        Args:
            entry_type (str): either 'allergy' or 'chronic_condition'
            description (str): what the allergy or condition is
        """
        if entry_type == "allergy":
            if description not in self.allergies:
                self.allergies.append(description)
                print("[OK] Allergy added: " + description)
            else:
                print("[INFO] Allergy already in the list.")
        elif entry_type == "chronic_condition":
            if description not in self.chronic_conditions:
                self.chronic_conditions.append(description)
                print("[OK] Condition added: " + description)
        else:
            print("[ERROR] Type not recognised: " + entry_type)

    def add_visit(self, reason, diagnosis):
        """
        Saves a visit to the patient history.
        Each visit is a tuple so it cannot be changed after.

        Args:
            reason (str): why the patient came
            diagnosis (str): what the doctor found
        """
        visit_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        # tuple because we dont want to modify old visits
        visit = (visit_date, reason, diagnosis)
        self.visit_history.append(visit)
        print("[OK] Visit saved on " + visit_date)

    def get_visit_history(self):
        """Prints all visits for this patient."""
        if len(self.visit_history) == 0:
            print("[INFO] No visits yet for " + self.get_full_name())
            return

        print("Visit history for " + self.get_full_name() + " (" + self.file_id + ")")
        i = 1
        for visit in self.visit_history:
            visit_date, reason, diagnosis = visit
            print("Visit " + str(i) + " on " + visit_date)
            print("  Reason    : " + reason)
            print("  Diagnosis : " + diagnosis)
            i = i + 1

    def add_vaccine(self, vaccine_name, date_given):
        """
        Adds a vaccine to the patient vaccination record.

        Args:
            vaccine_name (str): name of the vaccine
            date_given (str): date in DD/MM/YYYY format
        """
        self.vaccination_status[vaccine_name] = date_given
        print("[OK] Vaccine " + vaccine_name + " added on " + date_given)

    def archive(self):
        """Sets the patient status to archived."""
        self.status = "archived"
        print("[OK] File " + self.file_id + " is now archived.")

    def to_dict(self):
        """
        Converts patient data to a dictionary for saving to JSON.

        Returns:
            dict: all patient data
        """
        data = {
            "file_id": self.file_id,
            "last_name": self.get_last_name(),
            "first_name": self.get_first_name(),
            "date_of_birth": self.get_date_of_birth(),
            "gender": self.get_gender(),
            "phone": self.get_phone(),
            "blood_group": self.blood_group,
            "allergies": self.allergies,
            "chronic_conditions": self.chronic_conditions,
            "visit_history": [list(v) for v in self.visit_history],
            "vaccination_status": self.vaccination_status,
            "status": self.status
        }
        return data

    def __str__(self):
        """Short description of the patient."""
        return "Patient [" + self.file_id + "] - " + self.get_full_name()
