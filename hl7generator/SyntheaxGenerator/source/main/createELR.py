import csv
import os
import re
from datetime import datetime

# Function to clean up the CSV by keeping only the desired columns, removing trailing numbers, and reformatting DOB
def clean_csv(input_csv, output_csv, columns_to_keep):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        # Create a new list of fieldnames that only includes the columns to keep
        fieldnames = [field for field in reader.fieldnames if field in columns_to_keep]
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            # Clean 'FIRST' and 'LAST' columns to remove trailing numbers
            if 'FIRST' in row:
                row['FIRST'] = re.sub(r'\d+$', '', row['FIRST']).strip()
            if 'LAST' in row:
                row['LAST'] = re.sub(r'\d+$', '', row['LAST']).strip()
            
            # Reformat the 'BIRTHDATE' to 'YYYYMMDD' format if it's in 'YYYY-MM-DD' format
            if 'BIRTHDATE' in row and row['BIRTHDATE']:
                try:
                    dob = datetime.strptime(row['BIRTHDATE'], '%Y-%m-%d')
                    row['BIRTHDATE'] = dob.strftime('%Y%m%d')
                except ValueError:
                    # Handle the case where the date might not be in the expected format
                    row['BIRTHDATE'] = ''  # or some fallback value
            
            # Write each row with only the desired columns
            filtered_row = {key: value for key, value in row.items() if key in columns_to_keep}
            writer.writerow(filtered_row)

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
csv_file = os.path.join(script_dir, '/data/csv/patients.csv')
cleaned_csv_file = os.path.join(script_dir, '../assets/data/patients_cleaned.csv')

# Columns you want to keep in the CSV
columns_to_keep = ['LAST', 'FIRST', 'BIRTHDATE', 'GENDER', 'ADDRESS', 'CITY', 'STATE', 'ZIP', 'RACE', 'ETHNICITY', 'SSN']

# Clean the CSV
clean_csv(csv_file, cleaned_csv_file, columns_to_keep)

# After cleaning, update the HL7 files with the cleaned CSV
hl7_folder = os.path.join(home_dir, "Desktop/IH")  # Folder containing the HL7 files
update_hl7_files_with_csv(cleaned_csv_file, hl7_folder)
