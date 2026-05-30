"""
Module: medicament.py
This file contains the Medicine class.
It handles medicine info, stock levels and expiry dates.
Author  : Member 2 - ESA STONE
Course  : Programming I with Python (3PRG1205)
"""

import json
from datetime import datetime


# List of forms a medicine can come in (tuple because it never changes)
POSSIBLE_FORMS = ('tablet', 'syrup', 'injectable', 'ointment', 'capsule', 'suppository', 'solution')

# If a medicine expires in less than 90 days, we show a warning
EXPIRY_ALERT_DAYS = 90


class Medicine:
    """
    This class represents one medicine in the pharmacy.
    It stores all the info about the medicine and has methods to manage it.
    """

    def __init__(self, inn, brand_name, form, dosage, stock_quantity, minimum_quantity, expiry_date, unit_price):
        """
        This runs when we create a new Medicine object.
        We pass in all the details about the medicine here.
        """

        self.inn = inn                          # generic name (e.g. Paracetamol)
        self.brand_name = brand_name            # commercial name (e.g. Doliprane)
        self.dosage = dosage                    # strength (e.g. 500mg)
        self.stock_quantity = stock_quantity    # how many units we have right now
        self.minimum_quantity = minimum_quantity  # minimum before we raise an alert
        self.expiry_date = expiry_date          # date the medicine expires (YYYY-MM-DD)
        self.unit_price = unit_price            # price per unit in CFA francs

        # check if the form given is valid, if not we use tablet as default
        if form in POSSIBLE_FORMS:
            self.form = form
        else:
            self.form = 'tablet'
            print("WARNING: unknown form given, using tablet as default.")

    def check_stock(self):
        """
        Returns True if stock is above the minimum, False if not.
        """
        return self.stock_quantity > self.minimum_quantity

    def check_expiry(self):
        """
        Checks the expiry date and prints a warning if needed.
        """

        # convert the expiry date string into a real date object so we can compare
        expiry = datetime.strptime(self.expiry_date, '%Y-%m-%d')
        today = datetime.now()

        # calculate how many days are left before expiry
        days_remaining = (expiry - today).days

        if days_remaining < 0:
            # the medicine is already expired
            print(f"EXPIRED: {self.brand_name} expired {abs(days_remaining)} day(s) ago!")
        elif days_remaining <= EXPIRY_ALERT_DAYS:
            # expires soon, show a warning
            print(f"EXPIRY WARNING: {self.brand_name} expires in {days_remaining} day(s).")
        else:
            # all good
            print(f"OK: {self.brand_name} expires in {days_remaining} day(s).")

    def deduct_stock(self, quantity):
        """
        Removes a certain number of units from the stock.
        Raises an error if we don't have enough.
        """

        # make sure we have enough before removing
        if quantity > self.stock_quantity:
            raise ValueError(
                f"Not enough stock for {self.brand_name}. "
                f"Requested: {quantity}, Available: {self.stock_quantity}"
            )

        # remove the units from stock
        self.stock_quantity -= quantity
        print(f"{quantity} unit(s) of {self.brand_name} dispensed. Stock left: {self.stock_quantity}")

        # warn if stock is now below minimum
        if not self.check_stock():
            print(f"WARNING: {self.brand_name} is below the minimum stock level ({self.minimum_quantity})!")

    def to_dict(self):
        """
        Turns the medicine into a dictionary so we can save it to a JSON file.
        """
        return {
            'inn': self.inn,
            'brand_name': self.brand_name,
            'form': self.form,
            'dosage': self.dosage,
            'stock_quantity': self.stock_quantity,
            'minimum_quantity': self.minimum_quantity,
            'expiry_date': self.expiry_date,
            'unit_price': self.unit_price
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Medicine object from a dictionary.
        We use this when loading medicines from the JSON file.
        """
        return cls(
            inn=data['inn'],
            brand_name=data['brand_name'],
            form=data['form'],
            dosage=data['dosage'],
            stock_quantity=data['stock_quantity'],
            minimum_quantity=data['minimum_quantity'],
            expiry_date=data['expiry_date'],
            unit_price=data['unit_price']
        )

    def __str__(self):
        """
        This is what gets printed when we print a Medicine object.
        """
        return (
            f"[{self.form.upper()}] {self.brand_name} ({self.inn}) - "
            f"{self.dosage} | Stock: {self.stock_quantity} | Price: {self.unit_price:.0f} CFA"
        )


# this block only runs when we run this file directly (not when it is imported)
if __name__ == '__main__':
    print("=== TEST - Medicine class ===\n")

    # create two medicine objects to test with
    paracetamol = Medicine(
        inn='Paracetamol',
        brand_name='Doliprane 500',
        form='tablet',
        dosage='500mg',
        stock_quantity=150,
        minimum_quantity=30,
        expiry_date='2025-08-15',
        unit_price=25.0
    )

    amoxicillin = Medicine(
        inn='Amoxicillin',
        brand_name='Amoxil 250',
        form='syrup',
        dosage='250mg/5ml',
        stock_quantity=10,
        minimum_quantity=20,
        expiry_date='2026-12-31',
        unit_price=1500.0
    )

    print(paracetamol)
    print(amoxicillin)
    print()

    print("--- Expiry check ---")
    paracetamol.check_expiry()
    amoxicillin.check_expiry()
    print()

    print("--- Stock check ---")
    print(f"Doliprane enough stock: {paracetamol.check_stock()}")
    print(f"Amoxil enough stock: {amoxicillin.check_stock()}")
    print()

    print("--- Deduct stock ---")
    paracetamol.deduct_stock(5)

    print("\n--- Save to dict ---")
    print(json.dumps(paracetamol.to_dict(), ensure_ascii=False, indent=2))
      
