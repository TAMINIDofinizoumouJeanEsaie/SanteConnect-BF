from datetime import datetime
from models.personne import Personne


# list of specialities the clinic works with
SPECIALITIES = (
    "General Medicine",
    "Paediatrics",
    "Gynaecology-Obstetrics",
    "General Surgery",
    "Internal Medicine",
    "Dermatology",
    "Ophthalmology",
    "ENT",
    "Cardiology",
    "Psychiatry"
)

# days doctors can work
WORKING_DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")


class Medecin(Personne):
    """
    Represents a doctor in SanteConnect BF.
    Inherits from Personne.
    """

    # counter to give each doctor a unique id
    _doctor_counter = 0

    def __init__(self, last_name, first_name, date_of_birth, gender, phone, speciality, licence_number):
        """
        Creates a new doctor.

        Args:
            last_name (str): family name
            first_name (str): first name
            date_of_birth (str): DD/MM/YYYY
            gender (str): M or F
            phone (str): 8 digits
            speciality (str): medical speciality
            licence_number (str): medical council number
        """
        # calling parent init
        super().__init__(last_name, first_name, date_of_birth, gender, phone)

        # unique id for the doctor
        Medecin._doctor_counter = Medecin._doctor_counter + 1
        self.doctor_id = "MED-" + str(Medecin._doctor_counter).zfill(3)

        self.speciality = speciality
        self.licence_number = licence_number.strip()

        # schedule is a list of dicts
        self.schedule = []

        # how many consultations this doctor has done
        self.total_consultations = 0

        # is the doctor currently available or not
        self.is_available = True

    def display_info(self):
        """
        Prints doctor info.
        This is the polymorphism part - different from Patient version.
        """
        print("=" * 50)
        print("DOCTOR PROFILE - SanteConnect BF")
        print("=" * 50)
        print("Doctor ID    : " + self.doctor_id)
        print("Full Name    : Dr " + self.get_full_name())
        print("Speciality   : " + self.speciality)
        print("Licence No   : " + self.licence_number)
        print("Age          : " + str(self.calculate_age()) + " years old")
        print("Phone        : " + self.get_phone())

        if self.is_available:
            print("Available    : Yes")
        else:
            print("Available    : No")

        print("Consultations: " + str(self.total_consultations))

        # print schedule if there is one
        if len(self.schedule) > 0:
            print("Schedule:")
            for slot in self.schedule:
                print("  " + slot["day"] + " | " + slot["start_time"] + " - " + slot["end_time"] + " | Room " + slot["room"])
        else:
            print("Schedule     : Not set")

        print("=" * 50)

    def add_schedule_slot(self, day, start_time, end_time, room):
        """
        Adds a time slot to the doctor schedule.

        Args:
            day (str): day of the week
            start_time (str): when the slot starts
            end_time (str): when the slot ends
            room (str): room number

        Returns:
            bool: True if added, False if there was a problem
        """
        # check the day is valid first
        if day not in WORKING_DAYS:
            print("[ERROR] " + day + " is not a valid working day.")
            return False

        # check if doctor already has something that day
        for slot in self.schedule:
            if slot["day"] == day:
                print("[CONFLICT] Dr " + self.get_full_name() + " already has a slot on " + day)
                return False

        # build the slot as a dictionary and add it
        new_slot = {
            "day": day,
            "start_time": start_time,
            "end_time": end_time,
            "room": room
        }
        self.schedule.append(new_slot)
        print("[OK] Slot added: " + day + " " + start_time + "-" + end_time + " Room " + room)
        return True

    def increment_consultations(self):
        """Adds 1 to the consultation count."""
        self.total_consultations = self.total_consultations + 1

    def set_availability(self, available):
        """
        Changes if the doctor is available or not.

        Args:
            available (bool): True or False
        """
        self.is_available = available
        if available:
            print("[OK] Dr " + self.get_full_name() + " is now available.")
        else:
            print("[OK] Dr " + self.get_full_name() + " is now unavailable.")

    def to_dict(self):
        """
        Converts doctor data to dictionary for JSON saving.

        Returns:
            dict: all doctor data
        """
        data = {
            "doctor_id": self.doctor_id,
            "last_name": self.get_last_name(),
            "first_name": self.get_first_name(),
            "date_of_birth": self.get_date_of_birth(),
            "gender": self.get_gender(),
            "phone": self.get_phone(),
            "speciality": self.speciality,
            "licence_number": self.licence_number,
            "schedule": self.schedule,
            "total_consultations": self.total_consultations,
            "is_available": self.is_available
        }
        return data

    def __str__(self):
        """Short description of the doctor."""
        return "Dr " + self.get_full_name() + " [" + self.speciality + "]"
