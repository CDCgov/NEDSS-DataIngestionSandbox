# This file builds a dataset of synthetic patient data to simulate incoming fields
# derived from Synthea data that could be used to link records. Names, addresses,
# and DOBs have been intentionally scrambled and misspelled. The output will be a csv file
# containing duplicate recrds
import random
from random import shuffle
from string import ascii_letters
import json
import os

import numpy as np
import pandas as pd
from faker import Faker
from datetime import datetime
import re

SCENARIO_NUM = "Scenario #"
MATCH = "Match"
NO_MATCH = "No Match"

faker = Faker()

ABBREVIATIONS: dict[str, str] = json.load(open('source/assets/address_abbreviations.json'))

# Set up proportions of scramble
PROPORTION_NO_ERRORS = 0
PROPORTION_BAD_FIRST_NAME = 0
PROPORTION_BAD_LAST_NAME = 0
PROPORTION_BAD_DOB = 0
PROPORTION_BAD_ZIP = 0
# Name
PROPORTION_SWAPPED_NAMES = 0.01 # Swap FIRST and LAST name
PROPORTION_TWINS = 0.01 # Alter FIRST and MRN
PROPORTION_PLACEHOLDER = 0.01 # FIRST and LAST -> Jane/John/Baby Doe/Girl/Boy
PROPORTION_COMMONLY_SHORT_NAMES = 0 # Alter FIRST to a short name from a list of short names
PROPORTION_COMPOUND_NAMES = 0
PROPORTION_UNKOWN = 0.01
PROPORTION_HYPHENATED = 0.01 # Add a hyphen and add another name
PROPORTION_PUNCTUATED = 0 # Add O' before FIRST
PROPORTION_PUNCTUATED_LAST = 0 # Add D' before LAST
PROPORTION_SHORT_NAMES = 0
PROPORTION_UPDATE_LASTNAME = 0 # Change LAST
PROPORTION_PREFIX = 0 # need to write code
PROPORTION_NICKNAME = 0
# DOB
PROPORTION_REVERSED_DOB = 0 # Reverse if Month<12
# SSN
PROPORTION_SSN_LAST_FOUR = 0.01
# Address
PROPORTION_PO_BOX = 0
PROPORTION_GENERAL_DELIVERY = 0
PROPORTION_EMERGENCY_MAIL = 0
PROPORTION_USPS_STORE = 0.01
PROPORTION_COMMUNITY_SERVICES = 0
# Scenario 19
PROPORTION_CONGREGATE_SETTINGS = 0
# Other scenarios
PROPORTION_UPPER_LOWER_CASE = 0
PROPORTION_LEADING_ZERO = 0
PROPORTION_ABBREVIATIONS = 0
PROPORTION_PUNCTUATION = 0
PROPORTION_SPACED = 0
PROPORTION_APT_UNIT = 0

PROPORTION_MISSING_ADDRESS_LAC = 0
PROPORTION_MISSING_EMAIL_LAC = 0
PROPORTION_MISSING_MRN_LAC = 0

def insert_punctuation(name):
    punctuations = ['.', ',', '!', '?', '-', "'", '"']
    # Insert punctuation at random position
    position = random.randint(0, len(name))
    punctuation = random.choice(punctuations)
    return name[:position] + punctuation + name[position:]

def load_nicknames(file_path):
    nickname_dict = {}
    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        name = row['Name']
        nicknames = row.drop(['Letter', 'Name']).dropna().tolist()
        nickname_dict[name] = nicknames
    return nickname_dict

def replace_names_with_nicknames(df, nickname_dict, proportion, seed=42):
    random.seed(seed)
    sampled_data = df.sample(frac=proportion, random_state=seed)

    new_rows = []
    for index, row in sampled_data.iterrows():
        first_name = row['FIRST']
        if first_name in nickname_dict:
            nicknames = nickname_dict[first_name]
            for nickname in nicknames:
                new_row = row.copy()
                new_row['FIRST'] = nickname
                new_rows.append(new_row)

    return pd.DataFrame(new_rows)

def reverse_date(date_str):
    try:
        # Parse the date string with the format MM-DD-YYYY
        dob = datetime.strptime(date_str, '%m-%d-%Y')
        
        # Swap month and day
        reversed_dob = dob.replace(day=dob.month, month=dob.day)
        
        # Validate if the new date is correct (e.g., not swapping to an invalid date)
        reversed_dob.strftime('%m/%d/%Y')  # this will raise ValueError if invalid
        
        # Return the reversed date in MM-DD-YYYY format
        return reversed_dob.strftime('%m-%d-%Y')
    except ValueError as e:
        print(f"Error converting date: {date_str}, Error: {e}")
        return None

def update_apartment_number(address: str) -> str:
    """
    Updates or adds an apartment/unit number in the address.
    
    :param address: The original address string.
    :return: The address string with updated or added apartment/unit number.
    """
    if 'Apt' in address or 'Suite' in address or 'Unit' in address:
        # Replace existing apartment/unit number
        address = re.sub(r'(Apt|Suite|Unit)\s*\d+', lambda x: f"{x.group(1)} {random.randint(1, 999)}", address)
    else:
        # Add a new apartment/unit number
        address += f" Apt {random.randint(1, 999)}"
    return address

def random_case_address(address):
    if isinstance(address, str):
        return address.upper() if random.choice([True, False]) else address.lower()
    return address

def split_word_in_address(address: str) -> str:
    """
    Randomly splits a word in the address by adding a space.
    
    :param address: The original address string.
    :return: The address string with a word split by a space.
    """
    words = address.split(' ')
    if len(words) > 1:
        word_to_split = random.choice(words[1:-1])  # avoid splitting the first or last word
        if len(word_to_split) > 1:
            split_pos = random.randint(1, len(word_to_split) - 1)
            words[words.index(word_to_split)] = word_to_split[:split_pos] + ' ' + word_to_split[split_pos:]
    return ' '.join(words)

def insert_punctuation(address: str) -> str:
    """
    Randomly inserts punctuation into the address string.
    
    :param address: The original address string.
    :return: The address string with punctuation.
    """
    parts = address.split(' ')
    if len(parts) > 1:
        pos = random.randint(1, len(parts) - 1)
        parts[pos] = parts[pos] + random.choice([',', '.'])
    return ' '.join(parts)

def contains_abbreviation(address: str, abbreviations: dict) -> bool:
    return any(word in address for word in abbreviations.keys())

def abbreviate_address(address: str) -> str:
    """
    Replaces parts of the address with common abbreviations.
    
    :param address: The original address string.
    :return: The address string with abbreviations.
    """
    
    for word, abbr in ABBREVIATIONS.items():
        address = address.replace(word, abbr)
    return address


def add_leading_zeros(address: str) -> str:
    """
    Adds leading zeros to an address number.
    
    :param address: The original address string.
    :return: The address string with leading zeros.
    """
    parts = address.split(' ')
    if parts[0].isdigit():
        parts[0] = parts[0].zfill(len(parts[0]) + random.randint(1, 3))
    return ' '.join(parts)
# 25	Living houseless addresses
# 26	ID Type (?)
# 27	SSN and last 4
def retain_last_four_ssn(ssn: str) -> str:
    return f"{ssn[-4:]}"

# 28	One to many potential matching detection
# 29	Incorrect DOB format



# Set seeds
seed = 123
Faker.seed(414)

# Functions

# Helper function to generate new unique IDs
def generate_new_ids(start_id, count):
    return list(range(start_id, start_id + count))

def scramble_dob(dob: str) -> str:
    """
    Scrambles a date of birth (DOB) that is in the form YYYY-MM-DD. DOBs can be
    scrambled by year (last two digits are swapped), month (two digits are swapped),
    day (digits are swapped), or diff. For diff, the year, month, or day are randomly
    increased or decreased by a value of 1, e.g. 1984 could become 1983 or 1984.

    :param dob: Date of birth string in the format YYYY-MM-DD.
    :return: Scrambled date of birth string in the format YYYY-MM-DD.
    """

    # Check if dob is in the correct format
    if not isinstance(dob, str) or len(dob) != 10 or dob[4] != '-' or dob[7] != '-':
        return dob  # Return the original dob if it's not in the correct format

    # Randomly select how DOB will be scrambled.
    method = random.choice(["year", "month", "day", "diff"])

    # Swap last two digits of the year
    if method == "year":
        scrambled_dob = dob[:2] + dob[3] + dob[2] + dob[4:]
    # Swap the two digits of the month
    elif method == "month":
        scrambled_dob = dob[:5] + dob[6] + dob[5] + dob[7:]
    # Swap the two digits of the day
    elif method == "day":
        scrambled_dob = dob[:-2] + dob[-1] + dob[-2]
    # Add or subtract 1 from a DOB's year, month, or day value
    elif method == "diff":
        scrambled_dob = change_dob(dob)
    return scrambled_dob

def change_dob(dob: str):
    time = random.choice(["year", "month", "day"])
    plus_minus = random.choice([-1, 1])
    year, month, day = dob.split("-")
    if time == "year":
        scrambled_dob = str(int(year) + plus_minus) + "-" + month + "-" + day
    elif time == "month":
        new_month = str(int(month) + plus_minus).zfill(2)
        if int(new_month) < 1:
            new_month = "01"
        elif int(new_month) > 12:
            new_month = "12"
        scrambled_dob = year + "-" + new_month + "-" + day
    elif time == "day":
        new_day = str(int(day) + plus_minus).zfill(2)
        if int(new_day) < 1:
            new_day = "01"
        elif int(new_day) > 31:
            new_day = "31"
        scrambled_dob = year + "-" + month + "-" + new_day
    return scrambled_dob

# This is not used
def scramble_zip(zip: str) -> str:
    """
    Scrambles all digits of a zip code except for the first one.

    :param zip: Zip code containing only numbers, as a string.
    :return: Zip code with the last [1:] digits scrambled.

    """
    zip_list = list(zip[1:])
    shuffle(zip_list)
    scrambled_zip = zip[0] + "".join(zip_list)
    return scrambled_zip

# This is not used
def add_missing_values(data: pd.DataFrame, missingness: dict) -> pd.DataFrame:
    """
    Randomly changes values in a column to missing (nan).

    :param data: A DataFrame object.
    :param missingness: Dictionary containing the percent missing (as a float) to
        introduce for each column, e.g., "BIRTHDATE": 0.02.
    :return: DataFrame with randomly missing data from the input column.

    """
    for column, perc_missing in missingness.items():
        data[column] = data[column].sample(frac=(1 - perc_missing))
    return data

def add_copies(data: pd.DataFrame, num_copies: int) -> pd.DataFrame:
    """
    Adds duplicate rows to a DataFrame.

    :param data: A DataFrame object.
    :param num_copies: The number of duplicate rows to add for each existing row.
    :return: A DataFrame object with duplicate rows.

    """
    data_with_copies = pd.DataFrame(np.repeat(data.values, num_copies, axis=0))
    data_with_copies.columns = data.columns

    return data_with_copies

def add_emails(data: pd.DataFrame) -> pd.DataFrame:
    """
    Adds an "EMAIL" column with a synthetic email address for each row of data. The
    email address domains are limited to the most common providers in the US (gmail,
    yahoo, and hotmail).

    :param data: A DataFrame object.
    :return: A DataFrame object with an EMAIL column of synthetic email addresses.
    """
    emails = [
        "".join(random.choice(ascii_letters) for x in range(10))
        for _ in range(len(data))
    ]
    emails = [
        (email + random.choice(["@gmail.com", "@yahoo.com", "@hotmail.com"]))
        for email in emails
    ]

    data["EMAIL"] = emails

    return data

def scramble_data(
    source_data: pd.DataFrame, seed: int, missingness: dict
) -> pd.DataFrame:
    """
    Scrambles a dataset including names, dates of birth, and zip codes. This function
    assumes the dataset contains the following columns:
    - BIRTHDATE
    - ZIP
    - FIRST (first name)
    - LAST (last name)
    - Id
    - SSN
    - ADDRESS
    - BIRTHDATE

    :param source_data: DataFrame object.
    :param seed: Seed.
    :names_to_nicknames: Dictionary containing first names and their associated
        nicknames.
    :missingness: Dictionary containing the percent missing (as a float) to
        introduce for each column, e.g., "BIRTHDATE": 0.02.
    :return: DataFrame object that has been scrambled.

    """

    global PROPORTION_UNKOWN
    global PROPORTION_PLACEHOLDER
    global PROPORTION_NO_ERRORS, PROPORTION_BAD_FIRST_NAME, PROPORTION_BAD_LAST_NAME
    global PROPORTION_NICKNAME, PROPORTION_BAD_DOB, PROPORTION_BAD_ZIP
    global PROPORTION_SWAPPED_NAMES, PROPORTION_TWINS, PROPORTION_PLACEHOLDER
    global PROPORTION_COMMONLY_SHORT_NAMES, PROPORTION_COMPOUND_NAMES, PROPORTION_UNKOWN
    global PROPORTION_HYPHENATED, PROPORTION_PUNCTUATED, PROPORTION_PUNCTUATED_LAST
    global PROPORTION_SHORT_NAMES, PROPORTION_UPDATE_LASTNAME, PROPORTION_PREFIX
    global PROPORTION_REVERSED_DOB, PROPORTION_SSN_LAST_FOUR, PROPORTION_PO_BOX
    global PROPORTION_GENERAL_DELIVERY, PROPORTION_EMERGENCY_MAIL, PROPORTION_USPS_STORE
    global PROPORTION_COMMUNITY_SERVICES, PROPORTION_CONGREGATE_SETTINGS
    global PROPORTION_UPPER_LOWER_CASE, PROPORTION_LEADING_ZERO, PROPORTION_ABBREVIATIONS
    global PROPORTION_PUNCTUATION, PROPORTION_SPACED, PROPORTION_APT_UNIT

    source_data["ZIP"] = source_data["ZIP"].astype(str).str.split(".").str[0]

    # Add synthetic emails
    source_data = add_emails(source_data)

    # Use SSN as MRN
    source_data["MRN"] = source_data["SSN"]

    good_data = source_data.sample(frac=PROPORTION_NO_ERRORS, random_state=seed)

    # Scramble DOB in subsample
    bad_dob = source_data.sample(frac=PROPORTION_BAD_DOB, random_state=seed)
    bad_dob["BIRTHDATE"] = bad_dob["BIRTHDATE"].apply(lambda x: scramble_dob(x))

    # Scramble zip in subsample
    bad_zip = source_data.sample(frac=PROPORTION_BAD_ZIP, random_state=seed)
    bad_zip["ZIP"] = bad_zip["ZIP"].apply(lambda x: scramble_zip(x))

    # -------------Scrambling NAMES------------
    # Swap First and Last name
    # Twins
    twins = source_data.sample(frac=PROPORTION_TWINS, random_state=seed)
    # Generate new first names and SSNs for twins
    faker = Faker()
    twins["FIRST"] = twins["FIRST"].apply(lambda x: faker.first_name())
    twins["SSN"] = twins["SSN"].apply(lambda x: faker.ssn())
    twins['GroundTruth'] = NO_MATCH
    twins['Description'] = "twins"
    twins[SCENARIO_NUM] = "1"

    # Swap first and last names
    swap_first_last = source_data.sample(frac=PROPORTION_SWAPPED_NAMES, random_state=seed)
    swap_first_last["FIRST"], swap_first_last["LAST"] = swap_first_last["LAST"], swap_first_last["FIRST"]
    swap_first_last['GroundTruth']= MATCH
    swap_first_last['Description'] = "swapFirstLast"
    swap_first_last[SCENARIO_NUM] = "3"


    # Hyphenated Last Names
    hyphenated_last_names = source_data.sample(frac=PROPORTION_HYPHENATED, random_state=seed).copy()
    hyphenated_last_names["FIRST"] = hyphenated_last_names["FIRST"] + "-" + hyphenated_last_names["LAST"].apply(lambda x: faker.last_name())
    hyphenated_last_names['GroundTruth'] = MATCH   
    hyphenated_last_names['Description'] = "hyphenatedLastNames"
    hyphenated_last_names[SCENARIO_NUM] = "4"

    # Punctuated FIRST Names
    punctuated_name = source_data.sample(frac=PROPORTION_PUNCTUATED, random_state=seed).copy()
    punctuated_name['FIRST'] = punctuated_name['FIRST'].apply(lambda x: x[0] + "'" + x[1:] if len(x) > 1 else x + "'")
    punctuated_name['GroundTruth'] = MATCH
    punctuated_name['Description'] = "punctuatedFirstName"
    punctuated_name[SCENARIO_NUM] = "5.1"

    # Punctuated LAST Names
    punctuate_last_name = source_data.sample(frac=PROPORTION_PUNCTUATED_LAST, random_state=seed).copy()
    punctuate_last_name['LAST'] = punctuate_last_name['LAST'].apply(lambda x: x[0] + "'" + x[1:] if len(x) > 1 else x + "'")
    punctuate_last_name['GroundTruth'] = MATCH
    punctuate_last_name['Description'] = "punctuatedLastName"
    punctuate_last_name[SCENARIO_NUM] = "5.2"


    # Compound Names
    compound_names = source_data.sample(frac= PROPORTION_COMPOUND_NAMES, random_state = seed).copy()
    compound_names['FIRST']= compound_names['FIRST'] + compound_names["LAST"].apply(lambda x: faker.last_name())
    compound_names['GroundTruth'] = MATCH
    compound_names['Description'] = "compoundNames"
    compound_names[SCENARIO_NUM] = "6"

    # Alias
    bad_name_nickname = source_data.sample(frac=PROPORTION_NICKNAME, random_state=seed)
    bad_name_nickname["FIRST"] = bad_name_nickname["FIRST"].apply(lambda x: faker.last_name())
    bad_name_nickname['LAST'] = bad_name_nickname["LAST"].apply(lambda x: faker.last_name())
    bad_name_nickname['GroundTruth'] = MATCH
    bad_name_nickname['Description'] = "Alias"
    bad_name_nickname[SCENARIO_NUM] = "7"
    
    # Commonly Shortened Names/Nicknames
    # Shortened Names -- cutss off the first half of the name 
    short_names = source_data.sample(frac=PROPORTION_NICKNAME, random_state=seed).copy()
    num_letters = [3, 4]
    for index, row in short_names.iterrows():
        i = random.choice(num_letters)
        short_names.at[index, 'FIRST'] = row['FIRST'][:i]
    short_names['GroundTruth'] = MATCH
    short_names['Description'] = "Commonly Shortened Names"
    short_names[SCENARIO_NUM] = "8.1"

    #Read the short names data (short-names.csv)
    nickname_file = 'source/assets/short-names.csv'
    nickname_dict = load_nicknames(nickname_file)
    commonly_short_names = replace_names_with_nicknames(source_data, nickname_dict, PROPORTION_COMMONLY_SHORT_NAMES, seed)
    commonly_short_names['GroundTruth'] = 'Match'
    commonly_short_names['Description'] = "Nicknames"
    commonly_short_names[SCENARIO_NUM] = "8.2"

    # Short Names
    short_names = source_data.sample(frac=PROPORTION_SHORT_NAMES, random_state=seed).copy()
    num_letters = [2, 3]
    for index, row in short_names.iterrows():
        i = random.choice(num_letters)
        short_names.at[index, 'FIRST'] = row['FIRST'][:i]
    short_names['GroundTruth'] = MATCH
    short_names['Description'] = "shortNames"
    short_names[SCENARIO_NUM] = "10"

    # Placeholder Names
    total_proportion = PROPORTION_PLACEHOLDER
    PROPORTION_PLACEHOLDER = total_proportion/2
    PROPORTION_PLACEHOLDER_NO_MATCH = total_proportion/2
    place_holder_name = source_data.sample(frac=PROPORTION_PLACEHOLDER, random_state=seed).copy()
    place_holder_list = [('Baby', 'Boy'), ('Baby', 'Girl'), ('Jane', 'Doe'), ('John', 'Doe')]
    for index, row in place_holder_name.iterrows():
        selected_placeholder = random.choice(place_holder_list)
        place_holder_name.at[index, 'FIRST'] = selected_placeholder[0]
        place_holder_name.at[index, 'LAST'] = selected_placeholder[1]
    place_holder_name['GroundTruth'] = MATCH
    place_holder_name['Description'] = "place_holder_name"
    place_holder_name[SCENARIO_NUM] = "11.1"
    # ---- No Match Logic -----
    place_holder_name_no_match = source_data.sample(frac=PROPORTION_PLACEHOLDER_NO_MATCH, random_state=seed).copy()
    place_holder_list = [('Baby', 'Boy'), ('Baby', 'Girl'), ('Jane', 'Doe'), ('John', 'Doe')]
    for index, row in place_holder_name_no_match.iterrows():
        selected_placeholder = random.choice(place_holder_list)
        place_holder_name_no_match.at[index, 'FIRST'] = selected_placeholder[0]
        place_holder_name_no_match.at[index, 'LAST'] = selected_placeholder[1]
    place_holder_name_no_match['SSN'] = faker.ssn()
    place_holder_name_no_match['BIRTHDATE']= faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    place_holder_name_no_match['GroundTruth'] = NO_MATCH
    place_holder_name_no_match['Description'] = "place_holder_name"
    place_holder_name_no_match[SCENARIO_NUM] = "11.2"

    # Anon/Unknown Names
    total_anon = PROPORTION_UNKOWN
    PROPORTION_UNKOWN = PROPORTION_UNKOWN/2
    PROPORTION_UNKOWN_NO_MATCH = total_anon/2
    anon_names_list = ['Unk', 'Anonymous', 'Anon', 'Unknown']
    unknown_names = source_data.sample(frac=PROPORTION_UNKOWN, random_state=seed).copy()
    for index, row in unknown_names.iterrows():
        selected_unknown = random.choice(anon_names_list)
        unknown_names.at[index, 'FIRST'] = selected_unknown
        unknown_names.at[index, 'LAST'] = selected_unknown
    unknown_names['GroundTruth'] = MATCH
    unknown_names['Description'] = "UnkownNames"
    unknown_names[SCENARIO_NUM] = "12.1"
    #----- No Match -----
    anon_names_list = ['Unk', 'Anonymous', 'Anon', 'Unknown']
    unknown_names_no_match = source_data.sample(frac=PROPORTION_UNKOWN_NO_MATCH, random_state=seed).copy()
    for index, row in unknown_names.iterrows():
        selected_unknown = random.choice(anon_names_list)
        unknown_names_no_match.at[index, 'FIRST'] = selected_unknown
        unknown_names_no_match.at[index, 'LAST'] = selected_unknown
    unknown_names_no_match['SSN'] = faker.ssn()
    unknown_names_no_match['BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    unknown_names_no_match['GroundTruth'] = NO_MATCH
    unknown_names_no_match['Description'] = "UnkownNames"
    unknown_names_no_match[SCENARIO_NUM] = "12.2"

    # Name change due to cultural specific reasons
    # Filter records with 'F' in the GENDER column
    filtered_data = source_data[source_data['GENDER'] == 'F']
    # Sample from the filtered data
    update_last_name = filtered_data.sample(frac=PROPORTION_UPDATE_LASTNAME, random_state=seed).copy()
    # Apply transformations
    update_last_name['LAST'] = update_last_name["LAST"].apply(lambda x: faker.last_name())
    update_last_name['GroundTruth'] = MATCH
    update_last_name['Description'] = "CultureSpecificNameChange"
    update_last_name[SCENARIO_NUM] = "13"


    # -------------Scrambling DOB------------
    source_data['BIRTHDATE_DT'] = pd.to_datetime(source_data['BIRTHDATE'], format='%m/%d/%Y', errors='coerce')
    valid_dates = source_data[source_data['BIRTHDATE_DT'].dt.day <= 12]

    # Switch month for date if month <12
    total_reversed_dob = PROPORTION_REVERSED_DOB
    PROPORTION_REVERSED_DOB = PROPORTION_REVERSED_DOB / 2
    PROPORTION_REVERSED_DOB_NO_MATCH = total_reversed_dob / 2

    reversed_dob = valid_dates.sample(frac=PROPORTION_REVERSED_DOB, random_state=seed).copy()
    reversed_dob['BIRTHDATE'] = reversed_dob['BIRTHDATE'].apply(reverse_date)
    reversed_dob[SCENARIO_NUM] = "14.1"
    reversed_dob['Description'] = "reversedDOB"
    reversed_dob['GroundTruth'] = MATCH

    reversed_dob_no_match = valid_dates.sample(frac=PROPORTION_REVERSED_DOB_NO_MATCH, random_state=seed).copy()
    reversed_dob_no_match['BIRTHDATE'] = reversed_dob_no_match['BIRTHDATE'].apply(reverse_date)
    reversed_dob_no_match['SSN'] = reversed_dob_no_match['SSN'].apply(lambda x: faker.ssn())
    reversed_dob_no_match['GroundTruth'] = NO_MATCH
    reversed_dob_no_match['Description'] = "reversedDOB"
    reversed_dob_no_match[SCENARIO_NUM] = "14.2"

    # -------------Scrambling Address--------
    # Apartment/Unit Number Addresses
    total_apt_unit = PROPORTION_APT_UNIT
    PROPORTION_APT_UNIT = PROPORTION_APT_UNIT / 2
    PROPORTION_APT_UNIT_NO_MATCH = total_apt_unit / 2

    apt_unit = source_data.sample(frac=PROPORTION_APT_UNIT, random_state=seed).copy()
    apt_unit['ADDRESS'] = apt_unit['ADDRESS'].apply(update_apartment_number)
    apt_unit[SCENARIO_NUM] = "18.1"
    apt_unit['Description'] = "aptUnitDifferentAddress"
    apt_unit['GroundTruth'] = MATCH

    apt_unit_no_match = source_data.sample(frac=PROPORTION_APT_UNIT_NO_MATCH, random_state=seed).copy()
    apt_unit_no_match['ADDRESS'] = apt_unit_no_match['ADDRESS'].apply(update_apartment_number)
    apt_unit_no_match['SSN'] = faker.ssn()
    apt_unit_no_match['BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    apt_unit_no_match[SCENARIO_NUM] = "18.2"
    apt_unit_no_match['Description'] = "aptUnitDifferentAddress"
    apt_unit_no_match['GroundTruth'] = NO_MATCH

    # Congregate Settings Addresses
    total_congregate_settings = PROPORTION_CONGREGATE_SETTINGS
    PROPORTION_CONGREGATE_SETTINGS = PROPORTION_CONGREGATE_SETTINGS / 2
    PROPORTION_CONGREGATE_SETTINGS_NO_MATCH = total_congregate_settings / 2
    congregate_settings = source_data.sample(frac=PROPORTION_CONGREGATE_SETTINGS, random_state=seed).copy()
    congregate_settings[SCENARIO_NUM] = "19.1"
    congregate_settings['Description'] = "congregateSettingsAddress"
    congregate_settings['GroundTruth'] = MATCH
    num_letters = [2, 3]
    for index, row in congregate_settings.iterrows():
        i = random.choice(num_letters)
        congregate_settings.at[index, 'FIRST'] = row['FIRST'][:i]

    congregate_settings_no_match = source_data.sample(frac=PROPORTION_CONGREGATE_SETTINGS_NO_MATCH, random_state=seed).copy()
    congregate_settings_no_match['SSN'] = faker.ssn()
    congregate_settings_no_match['BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    congregate_settings_no_match[SCENARIO_NUM] = "19.2"
    congregate_settings_no_match['Description'] = "congregateSettingsAddress"
    congregate_settings_no_match['GroundTruth'] = NO_MATCH

    # Uppercase/Lowercase Addresses
    total_upper_lower_address = PROPORTION_UPPER_LOWER_CASE
    PROPORTION_UPPER_LOWER_CASE = PROPORTION_UPPER_LOWER_CASE / 2
    PROPORTION_UPPER_LOWER_CASE_NO_MATCH = total_upper_lower_address / 2
    upper_lower_address = source_data.sample(frac=PROPORTION_UPPER_LOWER_CASE, random_state=seed).copy()
    upper_lower_address['ADDRESS'] = upper_lower_address['ADDRESS'].apply(random_case_address)
    upper_lower_address[SCENARIO_NUM] = "20.1"
    upper_lower_address['Description'] = "upperLowerAddress"
    upper_lower_address['GroundTruth'] = MATCH
    
    # ---- No Match Logic----
    upper_lower_address_no_match = source_data.sample(frac=PROPORTION_UPPER_LOWER_CASE_NO_MATCH, random_state=seed).copy()
    upper_lower_address_no_match['ADDRESS'] = upper_lower_address_no_match['ADDRESS'].apply(random_case_address)
    upper_lower_address_no_match['SSN'] = faker.ssn()
    upper_lower_address_no_match['BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    upper_lower_address_no_match[SCENARIO_NUM] = "20.2"
    upper_lower_address_no_match['Description'] = "upperLowerAddress"
    upper_lower_address_no_match['GroundTruth'] = NO_MATCH
    
    # Spaced Addresses
    total_spaced = PROPORTION_SPACED
    PROPORTION_SPACED = PROPORTION_SPACED / 2
    PROPORTION_SPACED_NO_MATCH = total_spaced / 2
    spaced_address = source_data.sample(frac=PROPORTION_SPACED, random_state=seed).copy()
    spaced_address['ADDRESS'] = spaced_address['ADDRESS'].apply(split_word_in_address)
    spaced_address[SCENARIO_NUM] = "21.1"
    spaced_address['Description'] = "spacedAddress"
    spaced_address['GroundTruth'] = MATCH
    
    # ----- No Match Logic --- 
    spaced_address_no_match = source_data.sample(frac=PROPORTION_SPACED_NO_MATCH, random_state=seed).copy()
    spaced_address_no_match['ADDRESS'] = spaced_address_no_match['ADDRESS'].apply(split_word_in_address)
    spaced_address_no_match['SSN'] = faker.ssn()
    spaced_address_no_match['BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    spaced_address_no_match[SCENARIO_NUM] = "21.2"
    spaced_address_no_match['Description'] = "spacedAddress"
    spaced_address_no_match['GroundTruth'] = NO_MATCH

    # Punctuation Addresses
    total_punctuated = PROPORTION_PUNCTUATION
    PROPORTION_PUNCTUATION = PROPORTION_PUNCTUATION / 2
    PROPORTION_PUNCTUATION_NO_MATCH = total_punctuated / 2
    punctuated = source_data.sample(frac=PROPORTION_PUNCTUATION, random_state=seed).copy()
    punctuated['ADDRESS'] = punctuated['ADDRESS'].apply(insert_punctuation)
    punctuated[SCENARIO_NUM] = "22.1"
    punctuated['Description'] = "punctuatedAddress"
    punctuated['GroundTruth'] = MATCH
    
    # --- No Match Logic--- 
    punctuated_no_match = source_data.sample(frac=PROPORTION_PUNCTUATION_NO_MATCH, random_state=seed).copy()
    punctuated_no_match['ADDRESS'] = punctuated_no_match['ADDRESS'].apply(insert_punctuation)
    punctuated_no_match['SSN'] = faker.ssn()
    punctuated_no_match['BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    punctuated_no_match[SCENARIO_NUM] = "22.2"
    punctuated_no_match['Description'] = "punctuatedAddress"
    punctuated_no_match['GroundTruth'] = NO_MATCH

    # Scenario #25 Living Houseless
    # PO BOX
    po_box = source_data.sample(frac=PROPORTION_PO_BOX, random_state=seed).copy()
    po_box[SCENARIO_NUM] = "25.5.1"
    po_box['Description'] = "poBoxAddress"
    po_box['GroundTruth'] = MATCH
    num_letters = [2, 3]
    for index, row in po_box.iterrows():
        i = random.choice(num_letters)
        po_box.at[index, 'FIRST'] = row['FIRST'][:i]

    PROPORTION_PO_BOX_NO_MATCH = PROPORTION_PO_BOX
    po_box_no_match = source_data.sample(frac=PROPORTION_PO_BOX_NO_MATCH, random_state=seed).copy()
    for index, row in po_box_no_match.iterrows():
        po_box_no_match.at[index, 'SSN'] = faker.ssn()
        po_box_no_match.at[index, 'BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')

    po_box_no_match[SCENARIO_NUM] = "25.5.2"
    po_box_no_match['Description'] = "poBoxAddress"
    po_box_no_match['GroundTruth'] = NO_MATCH

    # General Delivery Addresses
    PROPORTION_GENERAL_DELIVERY_NO_MATCH = PROPORTION_GENERAL_DELIVERY

    general_delivery = source_data.sample(frac=PROPORTION_GENERAL_DELIVERY, random_state=seed).copy()
    general_delivery[SCENARIO_NUM] = "25.3.1"
    general_delivery['Description'] = "generalDeliveryAddress"
    general_delivery['GroundTruth'] = MATCH
    num_letters = [2, 3]
    for index, row in general_delivery.iterrows():
        i = random.choice(num_letters)
        general_delivery.at[index, 'FIRST'] = row['FIRST'][:i]

    general_delivery_no_match = source_data.sample(frac=PROPORTION_GENERAL_DELIVERY_NO_MATCH, random_state=seed).copy()
    for index, row in general_delivery_no_match.iterrows():
        general_delivery_no_match.at[index, 'SSN'] = faker.ssn()
        general_delivery_no_match.at[index, 'BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    general_delivery_no_match[SCENARIO_NUM] = "25.3.2"
    general_delivery_no_match['Description'] = "generalDeliveryAddress"
    general_delivery_no_match['GroundTruth'] = NO_MATCH

    # Emergency Mail Program Addresses
    PROPORTION_EMERGENCY_MAIL_NO_MATCH = PROPORTION_EMERGENCY_MAIL

    emergency_mail = source_data.sample(frac=PROPORTION_EMERGENCY_MAIL, random_state=seed).copy()
    emergency_mail[SCENARIO_NUM] = "25.4.1"
    emergency_mail['Description'] = "emergencyMailAddress"
    emergency_mail['GroundTruth'] = MATCH
    num_letters = [2, 3]
    for index, row in emergency_mail.iterrows():
        i = random.choice(num_letters)
        emergency_mail.at[index, 'FIRST'] = row['FIRST'][:i]

    emergency_mail_no_match = source_data.sample(frac=PROPORTION_EMERGENCY_MAIL_NO_MATCH, random_state=seed).copy()
    for index, row in emergency_mail_no_match.iterrows():
        emergency_mail_no_match.at[index, 'SSN'] = faker.ssn()
        emergency_mail_no_match.at[index, 'BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    emergency_mail_no_match[SCENARIO_NUM] = "25.4.2"
    emergency_mail_no_match['Description'] = "emergencyMailAddress"
    emergency_mail_no_match['GroundTruth'] = NO_MATCH

    # USPS Store Location

    usps_store = source_data.sample(frac=PROPORTION_USPS_STORE, random_state=seed).copy()
    usps_store[SCENARIO_NUM] = "25.2.1"
    usps_store['Description'] = "uspsStoreAddress"
    usps_store['GroundTruth'] = MATCH
    num_letters = [2, 3]
    for index, row in usps_store.iterrows():
        i = random.choice(num_letters)
        usps_store.at[index, 'FIRST'] = row['FIRST'][:i]

    usps_store['Address']= "USPS Store"

    usps_store_no_match = source_data.sample(frac=PROPORTION_USPS_STORE, random_state=seed).copy()
    for index, row in usps_store_no_match.iterrows():
        usps_store_no_match.at[index, 'SSN'] = faker.ssn()
        usps_store_no_match.at[index, 'BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')

    usps_store_no_match[SCENARIO_NUM] = "25.2.2"
    usps_store_no_match['Description'] = "uspsStoreAddress"
    usps_store_no_match['GroundTruth'] = NO_MATCH

    # Community Services Addresses
    PROPORTION_COMMUNITY_SERVICES_NO_MATCH = PROPORTION_COMMUNITY_SERVICES

    community_services = source_data.sample(frac=PROPORTION_COMMUNITY_SERVICES, random_state=seed).copy()
    community_services[SCENARIO_NUM] = "25.1.1"
    community_services['Description'] = "communityServicesAddress"
    community_services['GroundTruth'] = MATCH
    num_letters = [2, 3]
    for index, row in community_services.iterrows():
        i = random.choice(num_letters)
        community_services.at[index, 'FIRST'] = row['FIRST'][:i]

    community_services_no_match = source_data.sample(frac=PROPORTION_COMMUNITY_SERVICES_NO_MATCH, random_state=seed).copy()
    community_services_no_match['SSN'] = faker.ssn()
    community_services_no_match['BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    community_services_no_match[SCENARIO_NUM] = "25.1.2"
    community_services_no_match['Description'] = "communityServicesAddress"
    community_services_no_match['GroundTruth'] = NO_MATCH

    # Leading Zero Addresses
    TOTAL_LEADING_ZERO = PROPORTION_LEADING_ZERO
    PROPORTION_LEADING_ZERO = PROPORTION_LEADING_ZERO / 2
    PROPORTION_LEADING_ZERO_NMO_MATCH = TOTAL_LEADING_ZERO / 2

    leading_zero = source_data.sample(frac=PROPORTION_LEADING_ZERO, random_state=seed).copy()
    leading_zero['ADDRESS'] = leading_zero['ADDRESS'].apply(add_leading_zeros)
    leading_zero[SCENARIO_NUM] = "24.1"
    leading_zero['Description'] = "leadingZeroAddress"
    leading_zero['GroundTruth'] = MATCH

    leading_zero_no_match = source_data.sample(frac=PROPORTION_LEADING_ZERO_NMO_MATCH, random_state=seed).copy()
    leading_zero_no_match['ADDRESS'] = leading_zero_no_match['ADDRESS'].apply(add_leading_zeros)
    leading_zero_no_match['SSN'] = faker.ssn()
    leading_zero_no_match['BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    leading_zero_no_match[SCENARIO_NUM] = "24.2"
    leading_zero_no_match['Description'] = "leadingZeroAddress"
    leading_zero_no_match['GroundTruth'] = NO_MATCH

    # Abbreviated Addresses
    TOTAL_ABBREVIATED = PROPORTION_ABBREVIATIONS
    PROPORTION_ABBREVIATIONS = PROPORTION_ABBREVIATIONS / 2
    PROPORTION_ABBREVIATIONS_NO_MATCH = TOTAL_ABBREVIATED / 2
    filtered_data = source_data[source_data['ADDRESS'].apply(lambda x: contains_abbreviation(x, ABBREVIATIONS))]
    abbreviated = filtered_data.sample(frac=PROPORTION_ABBREVIATIONS, random_state=seed).copy()
    abbreviated['ADDRESS'] = abbreviated['ADDRESS'].apply(abbreviate_address)
    abbreviated[SCENARIO_NUM] = "23.1"
    abbreviated['Description'] = "abbreviatedAddress"
    abbreviated['GroundTruth'] = MATCH
    # ---- No Match Logic---- 
    abbreviated_no_match = filtered_data.sample(frac=PROPORTION_ABBREVIATIONS_NO_MATCH, random_state=seed).copy()
    abbreviated_no_match['ADDRESS'] = abbreviated_no_match['ADDRESS'].apply(abbreviate_address)
    abbreviated_no_match['SSN'] = faker.ssn()
    abbreviated_no_match['BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    abbreviated_no_match[SCENARIO_NUM] = "23.2"
    abbreviated_no_match['Description'] = "abbreviatedAddress"
    abbreviated_no_match['GroundTruth'] = NO_MATCH

    # SSN Last Four Digits
    TOTAL_SSN_LAST_FOUR = PROPORTION_SSN_LAST_FOUR
    PROPORTION_SSN_LAST_FOUR = PROPORTION_SSN_LAST_FOUR / 2
    PROPORTION_SSN_LAST_FOUR_NO_MATCH = TOTAL_SSN_LAST_FOUR / 2

    ssn_last_four = source_data.sample(frac=PROPORTION_SSN_LAST_FOUR, random_state=seed).copy()
    ssn_last_four['SSN'] = ssn_last_four['SSN'].apply(retain_last_four_ssn)
    ssn_last_four[SCENARIO_NUM] = "27"
    ssn_last_four['Description'] = "ssnLastFour"
    ssn_last_four['GroundTruth'] = MATCH

    ssn_last_four_no_match = source_data.sample(frac=PROPORTION_SSN_LAST_FOUR_NO_MATCH, random_state=seed).copy()
    ssn_last_four_no_match['SSN'] = ssn_last_four_no_match['SSN'].apply(retain_last_four_ssn)
    ssn_last_four_no_match['BIRTHDATE'] = faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%m/%d/%Y')
    ssn_last_four_no_match[SCENARIO_NUM] = "27.2"
    ssn_last_four_no_match['Description'] = "ssnLastFour"
    ssn_last_four_no_match['GroundTruth'] = NO_MATCH


    # Compile data
    data = pd.concat(
        [
            good_data,
            bad_dob,
            bad_zip,
            bad_name_nickname,
            swap_first_last,
            twins,
            hyphenated_last_names,
            punctuated_name,
            punctuate_last_name,
            compound_names,
            unknown_names,
            short_names,
            place_holder_name,
            place_holder_name_no_match,
            unknown_names_no_match,
            commonly_short_names,
            update_last_name,
            reversed_dob,
            po_box,
            general_delivery,
            emergency_mail,
            usps_store,
            community_services,
            congregate_settings,
            upper_lower_address,
            leading_zero,
            abbreviated,
            punctuated,
            apt_unit,
            ssn_last_four,
            po_box_no_match,
            general_delivery_no_match,
            emergency_mail_no_match,
            usps_store_no_match,
            community_services_no_match,
            congregate_settings_no_match,
            upper_lower_address_no_match,
            leading_zero_no_match,
            abbreviated_no_match,
            punctuated_no_match,
            spaced_address,
            spaced_address_no_match,
            apt_unit_no_match,
            ssn_last_four_no_match
        ],
        ignore_index=True,
    ).sort_values(by="Id")
    data = data.fillna(0)

    # Count number of true matches per Id
    data["num_matches"] = data.groupby("Id")["Id"].transform("count")

     # Generate new random ID for each row
    data['MatchID'] = data['Id']

    data['Id'] = [random.randint(1000000, 9999999) for _ in range(len(data))]

    return data


# ----------------------- Main function -----------------------------
def main():
  # Intialize LAC-specific missingness
  lac_missingness = {
      "ADDRESS": PROPORTION_MISSING_ADDRESS_LAC,
      "EMAIL": PROPORTION_MISSING_EMAIL_LAC,
      "MRN": PROPORTION_MISSING_MRN_LAC,
  }
  script_dir = os.path.dirname(os.path.abspath(__file__))
  csv_file = os.path.join(script_dir, '../assets/data/patients-synthea-1000.csv')
  # Get source data
  df = pd.read_csv(csv_file)
  # Check if 'BIRTHDATE' column exists and convert its format

  if 'BIRTHDATE' in df.columns:
    df['BIRTHDATE'] = pd.to_datetime(df['BIRTHDATE']).dt.strftime('%m/%d/%Y')
  df.to_csv(csv_file, index=False)

  source_data = df.copy()

  scrambled_data = scramble_data(
      source_data,
      seed=123,
      missingness=lac_missingness,
  )

  scrambled_data.to_csv(
      "hl7generator/SyntheaxGenerator/source/assets/data/patients-scrambled.csv",
      index=False,
  )
    

if __name__ == "__main__":
    main()