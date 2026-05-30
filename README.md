# SanteConnect BF

**Integrated Mobile Clinic Management System**

SanteConnect BF is a Python command-line application designed to digitalise the complete management of a clinic in Burkina Faso. It handles patients, medical consultations, medicine stock, billing, and statistical reports — entirely offline, making it suitable for areas with limited internet connectivity.

---

## How to Run the Project

**Requirements:** Python 3.8 or higher. No external libraries needed.

```bash
# 1. Clone the repository
git clone https://github.com/[GROUP-NAME]/SanteConnect-BF.git

# 2. Navigate into the folder
cd SanteConnect-BF

# 3. Run the program
python main.py
```

**Demo credentials:**
- Username: `admin`
- Password: `admin123`

---

## Features

- Register and manage patient records with a unique ID number
- Track complete medical history (visits, diagnoses, vaccinations)
- Record consultations with vital signs entry and automatic BMI calculation
- Automatically generate medical prescriptions
- Manage medicine stock with low-stock and expiry alerts
- Billing with partial payments and receipt generation
- Medical and financial reports exportable to CSV
- Automatic JSON data backup with timestamped history
- Role-based authentication with lockout after 3 failed attempts
- Colour-coded terminal interface with menu-driven navigation

---

## Technologies Used

| Technology | Version / Details |
|------------|------------------|
| Python     | 3.8+             |
| `json`     | Storing patients, medicines, and invoices |
| `datetime` | Age calculation, expiry dates, timestamps |
| `os`       | Folder and file management |
| `hashlib`  | Secure password hashing |
| `csv`      | Exporting statistical reports |
| `shutil`   | Copying backup files |
| `abc`      | Abstract classes (Personne base class) |
| `random`   | Generating unique record IDs |

No installation required — only the Python standard library is used.

---

## Project Structure

```
SanteConnect-BF/
│
├── main.py                      # Entry point — main menu and navigation
│
├── models/                      # Domain model classes
│   ├── personne.py              # Abstract parent class (Member 1)
│   ├── patient.py               # Patient class, inherits from Personne (Member 1)
│   ├── medecin.py               # Doctor class, inherits from Personne (Member 1)
│   ├── personnel.py             # Staff class, inherits from Personne (Member 1)
│   ├── medicament.py            # Medicine class with stock management (Member 2)
│   ├── consultation.py          # Consultation class with vital signs (Member 2)
│   ├── ordonnance.py            # Prescription class linked to Consultation (Member 2)
│   ├── facture.py               # Invoice class and payments (Member 3)
│   ├── rapport.py               # Parent Report class (Member 3)
│   ├── rapportmedical.py        # MedicalReport, inherits from Rapport (Member 3)
│   └── rapportfinancier.py      # FinancialReport, inherits from Rapport (Member 3)
│
├── services/                    # Business logic and data operations
│   ├── auth.py                  # Authentication and role management (Member 1)
│   ├── pharmacie.py             # Pharmacy and stock operations (Member 2)
│   └── sauvegarde.py            # JSON read/write and backups (Member 3)
│
├── utils/                       # Cross-cutting utility functions
│   ├── validation.py            # User input validation (Member 4)
│   ├── formatage.py             # Terminal display, colours, tables (Member 4)
│   └── date_utils.py            # Date calculations, age, expiry (Member 4)
│
├── data/                        # JSON data files (created automatically)
│   ├── patients.json
│   ├── medicaments.json
│   ├── consultations.json
│   ├── factures.json
│   └── personnel.json
│
├── logs/                        # Action audit log (created automatically)
│   └── audit.log
│
├── backups/                     # Timestamped backups (created automatically)
│
├── .gitignore                   # Files ignored by Git
└── README.md                    # This file
```

---

## OOP Structure

| Class | Inherits From | Key Methods |
|-------|---------------|-------------|
| `Personne` (abstract) | — | `display_info()` (abstract), `calculate_age()`, `get_full_name()`, `validate_phone()` |
| `Patient` | `Personne` | `add_medical_history()`, `add_visit()`, `get_history()`, `to_dict()` |
| `Medecin` | `Personne` | `get_speciality()`, `get_schedule()`, `calculate_stats()` |
| `Personnel` | `Personne` | `get_role()`, `get_hours()`, `clock_in()` |
| `Medicament` | — | `check_stock()`, `expiry_alert()`, `deduct_stock()`, `to_dict()` |
| `Consultation` | — | `calculate_bmi()`, `generate_prescription()`, `close()`, `display_summary()` |
| `Ordonnance` | — | `add_medicine()`, `print_prescription()`, `validate()`, `to_dict()` |
| `Facture` | — | `calculate_total()`, `record_payment()`, `get_balance()`, `generate_receipt()` |
| `Rapport` | — | `generate()`, `export_csv()`, `display_stats()` |
| `RapportMedical` | `Rapport` | `top_diseases()`, `epidemio_stats()` |
| `RapportFinancier` | `Rapport` | `cash_summary()`, `revenue_by_period()` |

### The 4 OOP Principles in SanteConnect BF

- **Encapsulation** — Private attributes `__password` in `auth.py`, `__discount` in `Facture`
- **Abstraction** — `Personne` is an abstract class (ABC); `display_info()` hides internal complexity
- **Inheritance** — `Patient`, `Medecin`, `Personnel` all inherit from `Personne`; `RapportMedical` and `RapportFinancier` inherit from `Rapport`
- **Polymorphism** — `display_info()` returns different output per class; `generate()` produces a different report depending on the type

---

## Group Members

| Member | Contribution | GitHub Profile |
|--------|-------------|----------------|
| TAMINI Dofinizoumou Jean Esaïe | Patient, Doctor, Staff classes and authentication | https://github.com/TAMINIDofinizoumouJeanEsaie |
| LAMINE Aïssa Toubba| Main menu, utility functions and README | https://github.com/Toubaai |
| BAMA Olivia| Invoice, Report classes, backup and data saving | https://github.com/olivi67 |
| DABIRE Prisca| Consultation, Medicine, Prescription classes and pharmacy | https://github.com/PriscaDabire |

---

## Acknowledgements

- **Programming I with Python** course — Burkina Institute of Technology
- Official Python documentation: [docs.python.org](https://docs.python.org/3/)
- Lecturer: Kweyakie Afi Blebo — course 3PRG1205
- Python `abc` module: [docs.python.org/3/library/abc.html](https://docs.python.org/3/library/abc.html)
- PEP 8 — Python Style Guide: [peps.python.org/pep-0008](https://peps.python.org/pep-0008/)

---

*Burkina Institute of Technology — Course 3PRG1205 — 2025/2026*

