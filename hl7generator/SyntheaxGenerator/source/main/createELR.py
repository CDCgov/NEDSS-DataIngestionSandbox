import csv
import os

# Function to replace placeholders in the HL7 message
def find_and_replace_hl7(hl7_message, csv_row):
    replacements = {
        "lastname": csv_row['LAST'] if csv_row['LAST'] else '',
        "firstname": csv_row['FIRST'] if csv_row['FIRST'] else '',
        "dob": csv_row['BIRTHDATE'] if csv_row['BIRTHDATE'] else '',
        "patSex": csv_row['GENDER'] if csv_row['GENDER'] else '',
        "address": csv_row['ADDRESS'] if csv_row['ADDRESS'] else '',
        "city": csv_row['CITY'] if csv_row['CITY'] else '',
        "state_abbr": csv_row['STATE'] if csv_row['STATE'] else '',
        "zip_code": csv_row['ZIP'] if csv_row['ZIP'] else '',
        "race": csv_row['RACE'] if csv_row['RACE'] else '',
        "ethnic": csv_row['ETHNICITY'] if csv_row['ETHNICITY'] else '',
        "ssn": csv_row['SSN'] if csv_row['SSN'] else ''
    }
    
    for placeholder, value in replacements.items():
        hl7_message = hl7_message.replace(placeholder, value)

    return hl7_message

# Function to process HL7 files and rename them based on new first and last names
def update_hl7_files_with_csv(csv_file, hl7_folder):
    # Read the CSV file into a list of dictionaries
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        csv_rows = list(reader)
    
    # Get all HL7 files in the folder
    hl7_files = [f for f in os.listdir(hl7_folder) if f.endswith('.txt')]
    
    # Iterate through the HL7 files and apply updates using the CSV rows
    for i, hl7_file in enumerate(hl7_files):
        hl7_file_path = os.path.join(hl7_folder, hl7_file)
        
        with open(hl7_file_path, 'r') as hl7file:
            hl7_message = hl7file.read()
        
        # Use the corresponding CSV row for the current HL7 file
        csv_row = csv_rows[i % len(csv_rows)]
        updated_hl7_message = find_and_replace_hl7(hl7_message, csv_row)
        
        # Construct a new file name based on first and last names
        first_name = csv_row['FIRST'].replace(' ', '_') if csv_row['FIRST'] else 'Unknown'
        last_name = csv_row['LAST'].replace(' ', '_') if csv_row['LAST'] else 'Unknown'
        new_file_name = f"{first_name}_{last_name}.txt"
        new_file_path = os.path.join(hl7_folder, new_file_name)
        
        # Save the updated HL7 message to the new file
        with open(new_file_path, 'w') as hl7file:
            hl7file.write(updated_hl7_message)
        
        os.remove(hl7_file_path)
        print(f"Updated and renamed: {hl7_file_path} -> {new_file_path}")

# Usage
script_dir = os.path.dirname(os.path.abspath(__file__))
home_dir = os.path.expanduser("~")
csv_file = os.path.join(script_dir, '../assets/data/patients-scrambled.csv')
hl7_folder = os.path.join(home_dir, "Desktop/IH")  # Folder containing the HL7 files

update_hl7_files_with_csv(csv_file, hl7_folder)
