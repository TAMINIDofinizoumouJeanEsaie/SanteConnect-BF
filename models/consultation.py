"""
Module: consultation.py
This file contains the Consultation class.
A consultation is when a patient sees a doctor at the clinic.
Author  : Member 2 - ESA STONE
Course  : Programming I with Python (3PRG1205)
"""

import uuid
from datetime import datetime
from models.ordonnance import Prescription


# normal vital sign ranges for adults (tuple because these values never change)
NORMAL_VITAL_RANGES = (
    ('systolic_bp',  90,  140),   # blood pressure top number
    ('diastolic_bp', 60,   90),   # blood pressure bottom number
    ('temperature',  36.1, 37.5), # body temperature in celsius
    ('heart_rate',   60,  100),   # beats per minute
    ('spo2',         95,  100),   # oxygen level in percent
)

# the different states a consultation can be in
CONSULTATION_STATUSES = ('waiting', 'in_progress', 'completed', 'cancelled')


class Consultation:
    """
    This class represents one medical consultation.
    It stores the patient info, vital signs, diagnosis and prescription.
    """

    def __init__(self, patient_id, doctor_id, patient_name, doctor_name, reason):
        """
        Creates a new consultation.
        We need both the patient and doctor info, plus the reason for the visit.
        """

        # give this consultation a unique ID
        self.consultation_id = f"CONS-{uuid.uuid4().hex[:6].upper()}"

        self.patient_id = patient_id      # patient ID number
        self.doctor_id = doctor_id        # doctor ID number
        self.patient_name = patient_name  # full name of patient
        self.doctor_name = doctor_name    # full name of doctor
        self.date_time = datetime.now().strftime('%Y-%m-%d %H:%M')  # when it happened
        self.reason = reason              # why the patient came in

        # dictionary to store the vital signs measured during consultation
        # we start with None for everything because nothing is measured yet
        self.vital_signs = {
            'blood_pressure': None,  # e.g. "120/80"
            'temperature': None,     # in celsius
            'weight': None,          # in kg
            'height': None,          # in metres
            'heart_rate': None,      # beats per minute
            'spo2': None             # oxygen saturation percent
        }

        self.diagnosis = ''              # main diagnosis (empty at first)
        self.secondary_diagnoses = []    # list of other diagnoses if any
        self.status = 'in_progress'      # consultation starts as in progress
        self.prescription = None         # no prescription yet

    def record_vital_signs(self, blood_pressure, temperature, weight, height, heart_rate, spo2):
        """
        Saves the vital signs measured during the consultation.
        We update the vital_signs dictionary with all the values.
        """

        self.vital_signs['blood_pressure'] = blood_pressure
        self.vital_signs['temperature'] = temperature
        self.vital_signs['weight'] = weight
        self.vital_signs['height'] = height
        self.vital_signs['heart_rate'] = heart_rate
        self.vital_signs['spo2'] = spo2

        print("Vital signs recorded.")

    def calculate_bmi(self):
        """
        Calculates the Body Mass Index (BMI) of the patient.
        Formula: BMI = weight / (height x height)
        Returns a tuple with the BMI value and what it means.
        """

        weight = self.vital_signs.get('weight')
        height = self.vital_signs.get('height')

        # we need both weight and height to do the calculation
        if weight is None or height is None or height == 0:
            return (None, "Not enough data to calculate BMI.")

        # do the calculation
        bmi = weight / (height ** 2)

        # figure out what the BMI means
        if bmi < 18.5:
            interpretation = 'Underweight'
        elif 18.5 <= bmi < 25.0:
            interpretation = 'Normal weight'
        elif 25.0 <= bmi < 30.0:
            interpretation = 'Overweight'
        elif 30.0 <= bmi < 35.0:
            interpretation = 'Obesity class I'
        elif 35.0 <= bmi < 40.0:
            interpretation = 'Obesity class II'
        else:
            interpretation = 'Obesity class III'

        # round to 2 decimal places and return both the value and the label
        return (round(bmi, 2), interpretation)

    def add_secondary_diagnosis(self, diagnosis):
        """
        Adds an extra diagnosis to the list.
        A patient can have more than one thing wrong at the same time.
        """
        self.secondary_diagnoses.append(diagnosis)
        print(f"Secondary diagnosis added: {diagnosis}")

    def generate_prescription(self):
        """
        Creates a new Prescription object for this consultation.
        Returns the prescription so the doctor can add medicines to it.
        """

        # create the prescription and link it to this consultation
        self.prescription = Prescription(
            consultation_id=self.consultation_id,
            patient_name=self.patient_name,
            doctor_name=self.doctor_name
        )

        print(f"Prescription {self.prescription.prescription_id} created.")
        return self.prescription

    def close(self):
        """
        Marks the consultation as completed.
        Once closed it cannot be changed.
        """

        if self.status == 'completed':
            print("This consultation is already completed.")
        else:
            self.status = 'completed'
            print(f"Consultation {self.consultation_id} is now closed.")

    def display_summary(self):
        """
        Prints a full summary of the consultation.
        Shows all the info: patient, doctor, vitals, diagnosis.
        """

        # get BMI before printing
        bmi_value, bmi_label = self.calculate_bmi()

        print("\n" + "=" * 55)
        print("      CONSULTATION SUMMARY - SanteConnect BF")
        print("=" * 55)
        print(f"  Consultation ID : {self.consultation_id}")
        print(f"  Date and time   : {self.date_time}")
        print(f"  Status          : {self.status.upper()}")
        print("-" * 55)
        print(f"  Patient         : {self.patient_name} (ID: {self.patient_id})")
        print(f"  Doctor          : Dr. {self.doctor_name}")
        print(f"  Reason          : {self.reason}")
        print("-" * 55)
        print("  VITAL SIGNS:")
        print(f"    Blood pressure : {self.vital_signs.get('blood_pressure', 'N/A')} mmHg")
        print(f"    Temperature    : {self.vital_signs.get('temperature', 'N/A')} C")
        print(f"    Weight         : {self.vital_signs.get('weight', 'N/A')} kg")
        print(f"    Height         : {self.vital_signs.get('height', 'N/A')} m")
        print(f"    Heart rate     : {self.vital_signs.get('heart_rate', 'N/A')} bpm")
        print(f"    SpO2           : {self.vital_signs.get('spo2', 'N/A')} %")

        # only show BMI if we were able to calculate it
        if bmi_value is not None:
            print(f"    BMI            : {bmi_value} -> {bmi_label}")

        print("-" * 55)

        # show main diagnosis or a placeholder if nothing entered yet
        if self.diagnosis:
            print(f"  MAIN DIAGNOSIS : {self.diagnosis}")
        else:
            print("  MAIN DIAGNOSIS : Not recorded yet")

        # show secondary diagnoses if there are any
        if self.secondary_diagnoses:
            print("  OTHER DIAGNOSES:")
            for diag in self.secondary_diagnoses:
                print(f"    - {diag}")

        print("=" * 55)

    def to_dict(self):
        """
        Converts the consultation into a dictionary for saving to JSON.
        """
        return {
            'consultation_id': self.consultation_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'patient_name': self.patient_name,
            'doctor_name': self.doctor_name,
            'date_time': self.date_time,
            'reason': self.reason,
            'vital_signs': self.vital_signs,
            'diagnosis': self.diagnosis,
            'secondary_diagnoses': self.secondary_diagnoses,
            'status': self.status,
            # save the prescription ID if there is one, otherwise save None
            'prescription_id': self.prescription.prescription_id if self.prescription else None
        }

    def __str__(self):
        """
        Short text description of the consultation.
        """
        return (
            f"Consultation {self.consultation_id} - "
            f"Patient: {self.patient_name} - "
            f"Doctor: Dr. {self.doctor_name} - "
            f"Status: {self.status}"
        )


# this block only runs when we run this file directly
if __name__ == '__main__':
    print("=== TEST - Consultation class ===\n")

    # create a test consultation
    consultation = Consultation(
        patient_id='BF-2026-00142',
        doctor_id='DOC-001',
        patient_name='Ouedraogo Ibrahim',
        doctor_name='Traore Fatimata',
        reason='Fever and headaches for 3 days'
    )

    # record the vital signs
    consultation.record_vital_signs(
        blood_pressure='120/80',
        temperature=38.6,
        weight=72.5,
        height=1.75,
        heart_rate=88,
        spo2=98
    )

    # set the diagnosis
    consultation.diagnosis = 'Simple malaria (Plasmodium falciparum)'
    consultation.add_secondary_diagnosis('Mild anaemia')
    consultation.add_secondary_diagnosis('Moderate dehydration')

    # show the BMI
    bmi, label = consultation.calculate_bmi()
    print(f"\nBMI: {bmi} - {label}")

    # print the full summary
    consultation.display_summary()

    # create a prescription and add medicines
    prescription = consultation.generate_prescription()
    prescription.add_medicine('Coartem 20/120mg', 24, '4 tablets morning and evening for 3 days')
    prescription.add_medicine('Paracetamol 500mg', 20, '2 tablets every 6 hours when fever')
    prescription.print_prescription()

    # close the consultation
    consultation.close()
    print(f"\nFinal status: {consultation.status}")
      
