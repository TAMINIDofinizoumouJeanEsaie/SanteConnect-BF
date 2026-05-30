"""
Module: pharmacie.py
This file has all the functions to manage the pharmacy.
It handles loading, saving, searching and dispensing medicines.
Author  : Member 2 - ESA STONE
Course  : Programming I with Python (3PRG1205)
"""

import json
import os
from models.medicament import Medicine
from models.ordonnance import Prescription


# the file where we save and load medicines
MEDICINES_FILE = 'data/medicines.json'


def load_medicines():
    """
    Loads all medicines from the JSON file.
    Returns a list of Medicine objects.
    If the file does not exist yet, returns an empty list.
    """

    # check if the file exists before trying to open it
    if not os.path.exists(MEDICINES_FILE):
        print(f"File {MEDICINES_FILE} not found. Starting with empty list.")
        return []

    # open the file and read the data
    with open(MEDICINES_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # convert each dictionary back into a Medicine object
    medicine_list = []
    for item in data:
        medicine = Medicine.from_dict(item)
        medicine_list.append(medicine)

    print(f"{len(medicine_list)} medicine(s) loaded.")
    return medicine_list


def save_medicines(medicine_list):
    """
    Saves the list of medicines to the JSON file.
    We convert each Medicine object to a dictionary first.
    """

    # create the data folder if it does not exist
    os.makedirs('data', exist_ok=True)

    # turn each medicine into a dictionary
    data = [med.to_dict() for med in medicine_list]

    # write everything to the file
    with open(MEDICINES_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"{len(medicine_list)} medicine(s) saved to {MEDICINES_FILE}.")


def search_medicine(name, medicine_list):
    """
    Looks for a medicine by name in the list.
    Searches both the generic name and the brand name.
    Returns the Medicine object if found, or None if not found.
    """

    # make the search lowercase so it works no matter how the user typed it
    search_term = name.lower().strip()

    # go through every medicine and check if the name matches
    for medicine in medicine_list:
        if search_term in medicine.inn.lower() or search_term in medicine.brand_name.lower():
            return medicine

    # nothing found
    return None


def display_stock_alerts(medicine_list):
    """
    Goes through all medicines and prints warnings for:
    - medicines that are low in stock
    - medicines that are close to expiry
    """

    print("\n" + "=" * 55)
    print("     PHARMACY ALERTS - SanteConnect BF")
    print("=" * 55)

    low_stock_count = 0

    # check every medicine one by one
    for medicine in medicine_list:

        # check if stock is below minimum
        if not medicine.check_stock():
            print(f"LOW STOCK: {medicine.brand_name} - "
                  f"stock: {medicine.stock_quantity} (min: {medicine.minimum_quantity})")
            low_stock_count += 1

        # check if it expires soon
        medicine.check_expiry()

    print("-" * 55)
    print(f"  Total low stock alerts: {low_stock_count}")
    print("=" * 55)


def dispense_from_prescription(prescription, medicine_list):
    """
    Takes a prescription and removes the medicines from the stock.
    Returns True if everything went fine, False if something failed.
    """

    print(f"\n--- Dispensing: {prescription.prescription_id} ---")

    # first make sure the prescription is valid
    if not prescription.validate():
        return False

    # we assume everything will work, and set to False if something fails
    all_dispensed = True

    # go through each medicine in the prescription
    for item in prescription.prescribed_medicines:
        name = item['name']
        quantity = item['quantity']

        # try to find the medicine in our stock
        medicine = search_medicine(name, medicine_list)

        if medicine is None:
            # medicine not found in stock
            print(f"ERROR: {name} not found in stock.")
            all_dispensed = False
            continue  # skip to the next medicine

        # try to remove units from stock
        try:
            medicine.deduct_stock(quantity)
        except ValueError as error:
            print(f"ERROR: {error}")
            all_dispensed = False

    if all_dispensed:
        print(f"All medicines dispensed for prescription {prescription.prescription_id}.")
    else:
        print(f"Some medicines could not be dispensed for {prescription.prescription_id}.")

    return all_dispensed


def search_medicine_interactive(medicine_list):
    """
    Lets the user type a medicine name and search for it.
    Keeps asking until the medicine is found or the user types 'quit'.
    Returns the Medicine object or None if the user quit.
    """

    found_medicine = None

    # keep looping until we find something or the user quits
    while found_medicine is None:
        name_input = input("\nEnter medicine name (or type quit to cancel): ").strip()

        # let the user exit if they want
        if name_input.lower() == 'quit':
            print("Search cancelled.")
            return None

        # try to find it
        found_medicine = search_medicine(name_input, medicine_list)

        if found_medicine is None:
            print(f"'{name_input}' not found. Try again.")
        else:
            print(f"Found: {found_medicine}")

    return found_medicine


def display_full_stock(medicine_list):
    """
    Prints a table showing all medicines and their stock levels.
    """

    print("\n" + "=" * 70)
    print("                 PHARMACY STOCK - SanteConnect BF")
    print("=" * 70)
    print(f"  {'BRAND NAME':<25} {'FORM':<12} {'STOCK':>6} {'MIN':>5} {'PRICE (CFA)':>11}")
    print("-" * 70)

    # print one row per medicine
    for med in medicine_list:
        # show a warning tag if stock is low
        if not med.check_stock():
            tag = "[LOW]"
        else:
            tag = "[ OK]"

        print(
            f"  {tag} {med.brand_name:<23} "
            f"{med.form:<12} "
            f"{med.stock_quantity:>6} "
            f"{med.minimum_quantity:>5} "
            f"{med.unit_price:>11.0f}"
        )

    print("=" * 70)
    print(f"  Total: {len(medicine_list)} medicine(s) in catalogue.")
    print("=" * 70)


# this block only runs when we run this file directly
if __name__ == '__main__':
    print("=== TEST - pharmacy module ===\n")

    # create some test medicines
    test_medicines = [
        Medicine('Paracetamol', 'Doliprane 500', 'tablet', '500mg', 150, 30, '2025-08-15', 25.0),
        Medicine('Amoxicillin', 'Amoxil 250', 'syrup', '250mg/5ml', 10, 20, '2026-12-31', 1500.0),
        Medicine('Artemether/Lumefantrine', 'Coartem', 'tablet', '20/120mg', 80, 25, '2027-03-01', 2500.0),
        Medicine('Ibuprofen', 'Advil 400', 'tablet', '400mg', 5, 15, '2026-06-30', 150.0),
    ]

    # show the full stock
    display_full_stock(test_medicines)

    # show any alerts
    display_stock_alerts(test_medicines)

    # test searching
    print("\n--- Search test ---")
    result = search_medicine('coartem', test_medicines)
    if result:
        print(f"Found: {result}")

    # test saving and loading
    print("\n--- Save and reload test ---")
    save_medicines(test_medicines)
    reloaded = load_medicines()
    print(f"Reloaded {len(reloaded)} medicines.")

    # test dispensing
    print("\n--- Dispensing test ---")
    test_prescription = Prescription('CONS-TEST01', 'Sawadogo Ali', 'Kabore Ines')
    test_prescription.add_medicine('Coartem', 6, '4 tablets morning and evening')
    test_prescription.add_medicine('Doliprane 500', 10, '1 tablet every 6 hours')

    dispense_from_prescription(test_prescription, test_medicines)
    display_full_stock(test_medicines)
  
