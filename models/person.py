from abc import ABC, abstractmethod
import re
from datetime import date


# this is the parent class for all people in the system
# Patient, Medecin and Personnel will all inherit from this

class Personne(ABC):
    """
    Abstract base class for any person in SanteConnect BF.
    Cannot be used directly, only through child classes.
    """

    def __init__(self, last_name, first_name, date_of_birth, gender, phone):
        """
        Sets up the basic info for a person.

        Args:
            last_name (str): family name
            first_name (str): first name
            date_of_birth (str): format DD/MM/YYYY
            gender (str): M or F
            phone (str): 8 digit phone number
        """
        # private attributes so no one can change them directly from outside
        self.__last_name = last_name.strip().upper()
        self.__first_name = first_name.strip().capitalize()
        self.__date_of_birth = date_of_birth.strip()
        self.__gender = gender.strip().upper()
        self.__phone = phone.strip()

    # getters so other parts of the code can read the private attributes

    def get_last_name(self):
        """Returns last name."""
        return self.__last_name

    def get_first_name(self):
        """Returns first name."""
        return self.__first_name

    def get_date_of_birth(self):
        """Returns date of birth."""
        return self.__date_of_birth

    def get_gender(self):
        """Returns gender."""
        return self.__gender

    def get_phone(self):
        """Returns phone number."""
        return self.__phone

    def set_phone(self, new_phone):
        """
        Updates phone number if it is valid.

        Args:
            new_phone (str): new phone number to set
        """
        if self.validate_phone(new_phone):
            self.__phone = new_phone.strip()
        else:
            print("[ERROR] Phone number is not valid. Nothing changed.")

    def get_full_name(self):
        """Returns first name and last name together."""
        return self.__first_name + " " + self.__last_name

    def calculate_age(self):
        """
        Calculates age from date of birth.

        Returns:
            int: age in years, 0 if date is wrong
        """
        try:
            day, month, year = self.__date_of_birth.split("/")
            birth_date = date(int(year), int(month), int(day))
            today = date.today()
            age = today.year - birth_date.year
            # check if birthday already happened this year
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age = age - 1
            return age
        except:
            return 0

    def validate_phone(self, number):
        """
        Checks if phone number has exactly 8 digits.

        Args:
            number (str): the number to check

        Returns:
            bool: True if valid, False if not
        """
        pattern = re.compile(r"^\d{8}$")
        return bool(pattern.match(number.strip()))

    # every child class must have this method but it looks different in each one
    # that is polymorphism
    @abstractmethod
    def display_info(self):
        """Shows the person's info. Each child class does this differently."""
        pass

    def __str__(self):
        """Simple string version of the person."""
        return self.get_full_name() + " | Age: " + str(self.calculate_age()) + " | Phone: " + self.__phone
