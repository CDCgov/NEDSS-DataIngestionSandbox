# EICR Generator

This Python script generates Electronic Initial Case Reports (EICRs) based on a provided XML template. The generated EICRs are saved to a specified directory, and all fields in the EICR are dynamically populated using randomized data for testing purposes.

---

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Setup Instructions](#setup-instructions)
4. [Usage](#usage)
5. [Example Commands](#example-commands)
6. [Input Validation](#input-validation)
7. [Customization](#customization)
8. [Field Generation](#field-generation)
9. [Output Files](#output-files)

---

## Features
- **Dynamic Data Generation**: Uses the `Faker` library to populate patient and author information such as names, addresses, SSNs, and email addresses.
- **Template-Based EICRs**: Generates sample eICRs using an XML template with all the required components, ensuring consistent structure.
- **Input Validation**: Restricts the number of eICRs to generate between 1 and 10,000.
- **Customizable Output**: Save eICRs to a specified directory or use the default output directory.

---

## Prerequisites
- Python 3.7 or higher
- pip installer
- Install required Python libraries:
  ```bash
  pip install faker

---

## Setup Instructions
- Clone the repository:
  ```bash
  git clone https://github.com/CDCgov/NEDSS-DataIngestionSandbox.git
  cd <project_directory>/NEDSS-DataIngestionSandbox/eICRGenerator

- Ensure the template folder exists within the project directory and the `eICR-CCDA-template.xml` file is present.

---

## Usage
Run the script with the following command-line arguments:

- `--num_eicrs`: Number of EICRs to generate (required; integer between 1 and 10,000).
- `--output_dir`: Directory to save the generated EICRs (optional; defaults to the output directory).

---

## Example Commands
- Generate 5 EICRs and save them in the output directory:
  ```bash
  python eICRGenerator.py --num_eicrs 5

- Generate 100 EICRs and save them to a specific directory:
  ```bash
  python eICRGenerator.py --num_eicrs 100 --output_dir /path/to/output

---

## Input Validation
- `--num_eicrs`: Must be an integer between 1 and 10,000. An error is raised if the input is out of range or invalid.
- `--output_dir`: If specified, the directory is validated, and it will be created if it does not exist.

---

## Customization
- The generated sample eICRs structure is based on the `eICR-CCDA-template.xml` file. Update this file in the template folder to customize the eICR format or add any extra components.

---

## Field Generation
- The script uses the Faker library to generate data for various fields. Modify the `generate_eicr()` function in the script to adjust the data generation logic.

---

## Output Files
- Generated sample eICRs are saved as XML files in the specified or default directory.
- Filenames are constructed using the format: `<FirstName>_<LastName>_CDA_eICR.xml`

