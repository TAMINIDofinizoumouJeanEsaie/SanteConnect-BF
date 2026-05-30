"""
Module: ordonnance.py
This file contains the Prescription class.
A prescription is created during a consultation and lists the medicines for the patient.
Author  : Member 2 - ESA STONE
Course  : Programming I with Python (3PRG1205)
"""

import uuid
from datetime import datetime


class Prescription:
    """
    This class represents a medical prescription.
    It keeps track of which medicines were prescribed to a patient.
    """

    def __init__(self, consultation_id, patient_name, doctor_name):
        """
        Creates a new prescription.
        We need the consultation ID, the patient name and the doctor name.
        """

        # generate a random unique ID for this prescription
        self.prescription_id = f"PRE-{uuid.uuid4().hex[:8].upper()}"

        self.consultation_id = consultation_id  # which consultation this belongs to
        self.patient_name = patient_name        # name of the patient
        self.doctor_name = doctor_name          # name of the doctor who wrote it
        self.date = datetime.now().strftime('%Y-%m-%d %H:%M')  # today's date and time

        # this list will hold all the medicines prescribed
        # each medicine is stored as a dictionary with name, quantity and instructions
        self.prescribed_medicines = []

    def add_medicine(self, medicine_name, quantity, instructions):
        """
        Adds a medicine to the prescription.
        We store the name, how many units and how to take it.
        """

        # create a dictionary to hold the medicine details
        item = {
            'name': medicine_name,
            'quantity': quantity,
            'instructions': instructions
        }

        # add it to the list
        self.prescribed_medicines.append(item)
        print(f"Medicine added: {medicine_name} x{quantity}")

    def validate(self):
        """
        Checks that the prescription has at least one medicine.
        Returns True if valid, False if empty.
        """

        if len(self.prescribed_medicines) == 0:
            print("Error: no medicines have been added to this prescription.")
            return False

        print(f"Prescription {self.prescription_id} is valid - {len(self.prescribed_medicines)} medicine(s).")
        return True

    def print_prescription(self):
        """
        Prints the full prescription in a nice readable format.
        Uses a for loop to go through all the medicines.
        """

        print("\n" + "=" * 55)
        print("        MEDICAL PRESCRIPTION - SanteConnect BF")
        print("=" * 55)
        print(f"  Prescription No : {self.prescription_id}")
        print(f"  Consultation    : {self.consultation_id}")
        print(f"  Date            : {self.date}")
        print(f"  Patient         : {self.patient_name}")
        print(f"  Doctor          : Dr. {self.doctor_name}")
        print("-" * 55)
        print("  MEDICINES PRESCRIBED:")
        print()

        # go through each medicine in the list and print it
        for index, med in enumerate(self.prescribed_medicines, start=1):
            print(f"  {index}. {med['name']}")
            print(f"     Quantity     : {med['quantity']} unit(s)")
            print(f"     Instructions : {med['instructions']}")
            print()

        print("-" * 55)
        print("  Doctor signature : ____________________")
        print("  Clinic stamp     : ____________________")
        print("=" * 55)

    def to_dict(self):
        """
        Converts the prescription into a dictionary for saving to JSON.
        """
        return {
            'prescription_id': self.prescription_id,
            'consultation_id': self.consultation_id,
            'patient_name': self.patient_name,
            'doctor_name': self.doctor_name,
            'date': self.date,
            'prescribed_medicines': self.prescribed_medicines
        }

    def __str__(self):
        """
        Short text description of the prescription.
        """
        return (
            f"Prescription {self.prescription_id} - "
            f"Patient: {self.patient_name} - "
            f"{len(self.prescribed_medicines)} medicine(s) - "
            f"Date: {self.date}"
        )


# this block only runs when we run this file directly
if __name__ == '__main__':
    print("=== TEST - Prescription class ===\n")

    # create a test prescription
    presc = Prescription(
        consultation_id='CONS-00001',
        patient_name='Ouedraogo Ibrahim',
        doctor_name='Traore Fatimata'
    )

    # add some medicines
    presc.add_medicine('Doliprane 500mg', 20, '1 tablet morning, noon and evening after meals for 5 days')
    presc.add_medicine('Amoxil 250mg syrup', 2, '1 tablespoon morning and evening for 7 days')
    presc.add_medicine('Coartem', 6, '4 tablets twice on day 1, then 4 per day for 2 more days')

    # check it is valid then print it
    presc.validate()
    presc.print_prescription()

    print("\n--- String representation ---")
    print(presc)
      
