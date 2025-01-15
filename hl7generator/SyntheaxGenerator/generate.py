import pyodbc
import pandas as pd
import sqlalchemy as sa
import re
import sys
import os
import random
import string
from faker import Faker
from sqlalchemy.engine import URL
from sqlalchemy.sql import text
from sqlalchemy import create_engine
#from decouple import config
from datetime import datetime, timedelta, date
from functools import cache


# To run the code, update the username and password under 'Creating a connection' for DTS1
# go to ./SyntheaxGenerator and run python3 generate.py 10 10101 34703-9

numoELRs = int(sys.argv[1])
conditionCode = str(sys.argv[2])
loincCode = str(sys.argv[3])

# numELRs=1 #default number of messages
# conditionCode=10101 #default condition code

 
#Creating a connection with the database
host = 'cdc-nbs-classic.czya31goozkz.us-east-1.rds.amazonaws.com'
user = ''
password = ''
database = 'NBS_MSGOUTE'
 
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={host};"
    f"DATABASE={database};"
    f"UID={user};"
    f"PWD={password}"
)
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
try:
    engine = create_engine(connection_url)
    with engine.connect() as connection:
        print("Connected to database successfully!")
except Exception as e:
    print("Failed to connect to the database.")
    print(f"Error: {e}")
 
discode = str(conditionCode)
loincode = str(loincCode)
 
Start_time = datetime.now()
print("Code Gen Starttime", Start_time)
 
# Caching all the SQL queries:
@cache
def queries():
 
    #racesql = """select concat (code, ' : ', code_desc_txt) from nbs_srte.dbo.Race_code;"""
    racesql = "select concat (code, ' : ', code_desc_txt) from HL7_Generator..RACE;"
    race_df= pd.read_sql(racesql, engine)
 
    # assigning_authority = """select concat(eid.root_extension_txt, ' : ', o.display_nm)
    #                         from nbs_odse..Organization o
    #                         inner join nbs_odse..entity_id eid
    #                         on eid.entity_uid = o.organization_uid
    #                         inner join [nbs_odse].[dbo].[Organization_name] org
    #                         on o.organization_uid = org.organization_uid
    #                         where cd = 'LAB' and standard_industry_class_cd = 'CLIA';"""
    assigning_authority = "select concat(root_extension_txt, ' : ', display_nm) from HL7_Generator..ASSIGNING_FILLER_FACILITY;"
    assign_df= pd.read_sql(assigning_authority, engine)
 
    # sending_facility = """select concat(eid.root_extension_txt, ' : ', o.display_nm)
    #                         from nbs_odse..Organization o
    #                         inner join nbs_odse..entity_id eid
    #                         on eid.entity_uid = o.organization_uid
    #                         inner join [nbs_odse].[dbo].[Organization_name] org
    #                         on o.organization_uid = org.organization_uid
    #                         where cd = 'ORG';"""   
    sending_facility = "select concat(root_extension_txt, ' : ', display_nm) from HL7_Generator..SENDING_FACILITY;"
    sending_df= pd.read_sql(sending_facility, engine)
 
    # programArea = "SELECT concat (loc.loinc_cd, ' : ', loc.component_name) FROM nbs_srte..loinc_code loc inner join  nbs_srte..loinc_condition locd ON loc.loinc_cd = locd.loinc_cd inner join nbs_srte..condition_code cond ON locd.condition_cd = cond.condition_cd where locd.condition_cd = '" + discode +"';"
    programArea = "SELECT concat (loinc_cd, ' : ',component_name) FROM HL7_Generator..DISEASE_CODE where condition_cd = '" + discode +"' and loinc_cd = '" + loincode +"';"
    disease_df= pd.read_sql(programArea, engine)
 
    # studyReason = "SELECT concat (reason_cd, ' : ', reason_desc_txt) FROM nbs_odse..Observation_reason;"
    studyReason = "SELECT concat (reason_cd, ' : ', reason_desc_txt) FROM HL7_Generator..REASON_CODE;"
    reason_df = pd.read_sql(studyReason, engine)
 
    #specimenSql = "select concat (code, ' : ', code_desc_txt) from nbs_srte.dbo.code_value_general where code_set_nm = 'SPECMN_SRC' and code LIKE '%[a-z]%';"
    specimenSql = "select concat (code, ' : ', code_desc_txt) from HL7_Generator..SPECIMEN where code LIKE '%[a-z]%';"
    specimen_df = pd.read_sql(specimenSql, engine)
 
    #AltspecimenSql = "select concat (code, ' : ', code_desc_txt) from nbs_srte.dbo.code_value_general where code_set_nm = 'SPECMN_SRC' and code LIKE '%[0-9]%';"
    AltspecimenSql = "select concat (code, ' : ', code_desc_txt) from HL7_Generator..SPECIMEN where code LIKE '%[a-z]%';"
    alt_spm_df = pd.read_sql(AltspecimenSql, engine)
 
    return race_df, assign_df, sending_df, disease_df, reason_df, specimen_df, alt_spm_df
 
# Assiging the tupples to the queries function
race_df, assign_df, sending_df, disease_df, reason_df, specimen_df, alt_spm_df = queries()
 
#################################################################################################################################################################
### Notes: Still need to work on bringing the Specimen and Alternate Specimen code to show for the same Text, Currently the code is putting 2 different values:
    ### |PUS^Pus^HL70487^258482009^Vesicle fluid sample ^SCT^2.5.1^Pus|
#################################################################################################################################################################
 
 
 
def generateELR(numoELRs, conditionCode, loincCode, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for i in range(int(numoELRs)):       
        
        curr_time = datetime.now()
 
        curr_date=curr_time.strftime("%Y%m%d")
 
        # Initializing Faker
        fake = Faker()
 
        # Generating Patient details using Faker
        patID = fake.random_int(min = 100000000, max = 999999999)
        firstname = fake.first_name()
        lastname = fake.last_name()
        middlename = fake.first_name()
        fullname = firstname + " " + lastname
        suffix = ["Sr", "Jr", "II", "III", "IV", "V", "ESQ"]
        prefix = ["Dr", "Mr", "Ms", "Mrs"]
        #degree = ["APRN", "CRNP", "NP", "PA"]
        docDegree = ["MD", "DO"]
        degree= ["APN", "BA", "BS", "BSN", "CNM", "CNP", "CPA", "DD", "DDS", "DMD", "DO", "DRN", "DVM", "JD", "LLB", "LLP", "LDN", "MA", "MBA", "MD", "MED", "MPH", "MS", "MSN", "NP", "PA", "Phd", "RN"]
        #prefix = ["Bishop", "Brother", "Cardinal", "Doctor/Dr.", "Father", "Honorable", "Miss", "Mother", "Mrs", "Monsignor", "Ms", "Mr", "Pastor", "Professor", "Rabbi", "Reverend", "Sister", "Swami"]
        #name_prefix = random.choice(prefix)
        #name_suffix = random.choice(suffix)
        #name_degree = random.choice(degree)
        sex = ["M", "F", "U"]
        patSex = random.choice(sex)
        first_part = fake.random_int(min=10000, max=99999)
        second_part = fake.random_int(min=0, max=9)
        letter = random.choice(string.ascii_uppercase)
        formatted_number = f"{first_part}{letter}-{second_part}"
        mails= ['gmail.com', 'hotmail.com', 'yahoo.com', 'icloud.com']
        numberrn = str(random.randint(10, 99))
        email = firstname + lastname + numberrn + "@" + random.choice(mails)
        #phone = fake.phone_number()
        new_ethnicity = ["2135-2^Hispanic or Latino^CDCREC", "2186-5^Not Hispanic or Latino", "UNK^Unknown"]
        new_race = ["2076-8^Native Hawaiian or Other Pacific Islander^CDCREC","2028-9^Asian^CDCREC"]
        race = random.choice(new_race)
        ethnicity = random.choice(new_ethnicity)
        homephone = fake.bothify(text='#######')
        workphone = fake.bothify(text='#######')
        phone = fake.bothify(text='##########')
        extension = fake.random_int(min=1000, max=9999)
        date_time = fake.date_time()
        current_time = datetime.now()
        weeks_ago = 3
        past_time = current_time - timedelta(weeks=weeks_ago)
        deceaseddatetime = past_time.strftime("%Y%m%d%H%M")
        countryofbirth = fake.country()
        def generate_alphanumeric_value(pattern):return fake.bothify(pattern)
        # Example: '##??##??' generates a string with 2 digits, 2 letters, 2 digits, and 2 letters
        pattern = '#########?'
        random_alphanumeric_value = generate_alphanumeric_value(pattern)
        def generate_random_phrase():return fake.sentence()
        specimen_details = generate_random_phrase()
 
        def generate_random_phrase_two():return fake.sentence()
        clinical_information = generate_random_phrase_two()
 
 
        #random_date_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
 
        ssn = fake.ssn()
 
     
        Drivers_License = fake.random_number(digits=9, fix_len=True)
 
# Generate a random driver's license number
       
        random_state_code = fake.state_abbr()
 
        # Creating a function to generate a fake birthday in the format: YYYY[MM[DD[HH[MM[SS[.S[S[S[S]]]]]]]]][+/-ZZZZ]
        #def generate_random_birthday():
        #    # Generate random date of birth using Faker
        #    dob = fake.date_of_birth(minimum_age=0, maximum_age=100)
        #    formatted_dob = dob.strftime("%Y%m%d%H%M%S")
        #    formatted_dob += f".{random.randint(0, 9999):04d}"
        #    timezone_offset_sign = random.choice(['+', '-'])
        #    timezone_offset_hours = random.randint(0, 12)
        #    timezone_offset_minutes = random.randint(0, 59)
        #    timezone_offset = f"{timezone_offset_sign}{timezone_offset_hours:02d}{timezone_offset_minutes:02d}"
 
        #    formatted_dob += timezone_offset
        #   
        #    return formatted_dob
       
        # dob = generate_random_birthday()
 
        dob_rn = fake.date_of_birth(minimum_age=0, maximum_age=100)
        dob = dob_rn.strftime("%Y%m%d%H%M")
 
        # Generating Address using Faker
        address = fake.street_address()
        unitnumber = fake.building_number()
        building_number = fake.building_number()
        city = fake.city()
        state_abbr = fake.state_abbr()
        zip_code = fake.zipcode()
        zips = [30004, 30309, 30311, 30329, 30331, 30338, 30342, 31106, 31107, 31126, 31131, 31139, 30029, 78613, 30004, 30322, 30329, 30338, 30004]
        zip_code = random.choice(zips)
        country = fake.country()
 
        # -------- Lab Report -----------
       
        # ---- Time ----
        # Generate HL7 datetime
        time = datetime.now()
        # char_time = time.strftime("%Y%m%d%H%M%S")
        char_time = time.strftime("%Y%m%d%H%M")
        # timezone_offset = random.randint(-1200, 1200)
        # sign = "-" if timezone_offset < 0 else "+"
        # hl7_datetime = f"{char_time}.{random.randint(0, 999):03d}{sign}{abs(timezone_offset):04d}"
 
        hl7_datetime = char_time
        original_date = datetime.strptime(hl7_datetime[:14], "%Y%m%d%H%M")
 
        # original_date = datetime.strptime(hl7_datetime[:14], "%Y%m%d%H%M%S")
 
        # Add 5 days to the original datetime
        future_date = original_date + timedelta(days=5)
        # future_char_time = future_date.strftime("%Y%m%d%H%M%S")
        future_char_time = future_date.strftime("%Y%m%d%H%M")
        # future_timezone_offset = random.randint(-1200, 1200)
        # future_sign = "-" if future_timezone_offset < 0 else "+"
        # future_time_hl7_datetime = f"{future_char_time}.{random.randint(0, 999):03d}{future_sign}{abs(future_timezone_offset):04d}"
        future_time_hl7_datetime = future_char_time
 
 
       
        # add_time = time + timedelta(days=10)
        # formatted_time = time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        # char_time = time.strftime("%Y%m%d%H%M%S")[:-3]
        # future_time = add_time.strftime("%Y%m%d%H%M%S")[:-3]
 
        # resultStatus = ["A", "D", "I", "L", "N", "P", "S", "T", "U", "W", "X", ]
        resultStatus = ["C", "F", "P"]
 
        # Parsing the data from SQL queries:
 
        # ---- Patient Race -----       
 
        #race_random_row = race_df.sample(n=1)
        #race = race_random_row.to_string(index=False)
 
        #patRace = re.sub("^[^_]* : ", "", race)
        #patRaceCode = re.sub(" : [^_]*", "", race).lstrip()
 
        # ----- Assigning Authority/Filler Facility ------       
 
        auth_random_row = assign_df.sample(n=1)
        authority = auth_random_row.to_string(index=False)
 
        assigning_authority_txt = re.sub("^[^_]* : ", "", authority)
        assigning_authority_id = re.sub(" : [^_]*", "", authority).lstrip()
 
        # ----- Sending or Placer Facility ------
       
        send_auth_random_row = sending_df.sample(n=1)
        facility = send_auth_random_row.to_string(index=False)
 
        sending_facility_txt = re.sub("^[^_]* : ", "", facility)
        sending_facility_id = re.sub(" : [^_]*", "", facility).lstrip()
 
        # ----- Disese/Condition Code ------
 
        disease_random_row = disease_df.sample(n=1)
        disease = disease_random_row.to_string(index=False)
 
        patDisease = re.sub("^[^_]* : ", "", disease)
        patDiseaseCode = re.sub(" : [^_]*", "", disease).lstrip()
 
        # -------- Reason for Study -----------
 
 
        reason_random_row = reason_df.sample(n=1)
        reason = reason_random_row.to_string(index=False)
 
        reasonTxt = re.sub("^[^_]* : ", "", reason)
        reasonCode = re.sub(" : [^_]*", "", reason).lstrip()
 
        # ------------ Specimen Data -------------
 
 
        specimen_random_row = specimen_df.sample(n=1)
        specimen = specimen_random_row.to_string(index=False)
 
        specimenTxt = re.sub("^[^_]* : ", "", specimen)
        specimenCode = re.sub(" : [^_]*", "", specimen).lstrip()
 
 
        # ------------ Alternate Specimen Data -------------
 
        alt_specimen_random_row = alt_spm_df.sample(n=1)
        alt_specimen = alt_specimen_random_row.to_string(index=False)
 
        AltspecimenTxt = re.sub("^[^_]* : ", "", alt_specimen)
        AltspecimenCode = re.sub(" : [^_]*", "", alt_specimen).lstrip()
 
 
 
        # ------ Creating Segments and Fields ------
 
 
        # ----- MSH ---------
        # Message Header. This segment is a mandatory part of an ORU message,
        # and contains information about the message sender and receiver,
        # the date and time that the message was created.
        # This segment is required.
 
        msh1 = "" # MSH.1 - Field Separator -- R
        msh2 = "^~\&" # MSH.2 - Encoding Characters -- R
       
        msh3_1 = "HL7 Generator" # MSH.3.1 - Namespace Id ---- Sending Application
        msh3_2 = "" # MSH.3.2 - Universal Id
        msh3_3 = "" # MSH.3.3 - Universal Id Type
        msh3 = (f"{msh3_1}^{msh3_2}^{msh3_3}")
       
        msh4_1 = assigning_authority_txt # MSH.4.1 - Namespace Id ---- Sending Facility
        msh4_2 = assigning_authority_id # MSH.4.2 - Universal Id
        msh4_3 = "CLIA" # MSH.4.3 - Universal Id Type
        msh4 = (f"{msh4_1}^{msh4_2}^{msh4_3}")
       
        msh5_1 = "ALDOH" # MSH.5.1 - Namespace Id ---- Recieving Application
        msh5_2 = "OID" # MSH.5.2 - Universal Id
        msh5_3 = "ISO" # MSH.5.3 - Universal Id Type
        msh5 = (f"{msh5_1}^{msh5_2}^{msh5_3}")
       
        msh6_1 = "AL" # MSH.6.1 - Namespace Id ---- Recieving Facility
        msh6_2 = "OID" # MSH.6.2 - Universal Id
        msh6_3 = "ISO" # MSH.6.3 - Universal Id Type
        msh6 = (f"{msh6_1}^{msh6_2}^{msh6_3}")
       
        msh7 = hl7_datetime # MSH.7.1 - Time ---- R
        #msh7_2 = "" # MSH.7.2 - Degree Of Precision
       
        msh8 = "" # MSH.8 - Security
        
        msh9_1 = 'ORU' # MSH.9.1 - Message Code ---- R
        msh9_2 = 'R01' # MSH.9.2 - Trigger Event ---- R
        msh9_3 = 'ORU_R01' # MSH.9.3 - Message Structure ---- R
        msh9 = (f"{msh9_1}^{msh9_2}^{msh9_3}")
       
        msh10 = (f"{hl7_datetime}{numberrn}") # MSH.10 - Message Control ID ---- R
       
        msh11_1 = "P" # MSH.11.1 - Processing Id ---- R
        msh11_2 = "T" # MSH.11.2 - Processing Mode ---- R
        msh11 = (f"{msh11_1}")
       
        msh12_1 = "2.5.1" # MSH.12.1 - Version Id
        msh12_2 = "" # MSH.12.2 - Internationalization Code
        msh12_3 = "" # MSH.12.3 - International Version Id
        msh12 = (f"{msh12_1}")
       
        msh13 = "" # MSH.13 - Sequence Number
        msh14 = "" # MSH.14 - Continuation Pointer
        msh15 = "" # MSH.15 - Accept Acknowledgment Type
        msh16 = "" # MSH.16 - Application Acknowledgment Type
        msh17 = "" # MSH.17 - Country Code
        msh18 = "" # MSH.18 - Character Set
        msh19_1 = "" # MSH.19.1 - Identifier ----- Principal Language Of Message
        msh19_2 = "" # MSH.19.2 - Text
        msh19_3 = "" # MSH.19.3 - Name Of Coding System
        msh19_4 = "" # MSH.19.4 - Alternate Identifier
        msh19_5 = "" # MSH.19.5 - Alternate Text
        msh19_6 = "" # MSH.19.6 - Name Of Alternate Coding System
        msh19 = ""
        msh20 = "" #MSH20 - Alternate Character Set Handling Scheme
        msh21_1 = "" # MSH.21.1 - Entity Identifier ----- Message Profile Identifier
        msh21_2 = "" # MSH.21.2 - Namespace Id
        msh21_3 = "" # MSH.21.3 - Universal Id
        msh21_4 = "" # MSH.21.4 - Universal Id Type
        msh21 = ""
 
        MSH = (
        f"MSH|"
        f"{msh2}|{msh3}|{msh4}|{msh5}|{msh6}|{msh7}|{msh8}|{msh9}|{msh10}|{msh11}|{msh12}")
 
        #This segment is used by all applications as the primary means of communicating patient identification information.
        #This segment contains permanent patient identifying and demographic information that, for the most part, is not likely to change frequently.
 
        ## PID.1 - Set ID -PID
        pid1 = "1"  # PID.1 - Set ID - PID
        ## PID.2 - Patient ID
        pid2_1 = patID  # PID.2.1 - Id Number
        pid2_2 = ""  # PID.2.2 - Check Digit
        pid2_3 = ""  # PID.2.3 - Check Digit Scheme
        pid2_4_1 = assigning_authority_txt # PID 2.4.1 - Namespace Id
        pid2_4_2 = assigning_authority_id # PID 2.4.2 - Universal Id
        pid2_4_3 = "CLIA" # PID 2.4.3 - Universal Id Type
        pid2_4 = (f"{pid2_4_1}&{pid2_4_2}&{pid2_4_3}")  # PID.2.4 - Assigning Authority
        pid2_5 = "U"  # PID.2.5 - Identifier Type Code
        pid2_6 = ""  # PID.2.6 - Assigning Facility
        pid2_6_1 = "" # PID 2.6.1 - Namespace Id
        pid2_6_2 = "" # PID 2.6.2 - Universal Id
        pid2_6_3 = "" # PID 2.6.3 - Universal Id Type
        pid2_7 = ""  # PID.2.7 - Effective Date
        pid2_8 = ""  # PID.2.8 - Expiration Date
        pid2_9 = ""  # PID.2.9 - Assigning Jurisdiction
        pid2_9_1 = "" # PID 2.9.1 - Identifier
        pid2_9_2 = "" # PID 2.9.2 - Text
        pid2_9_3 = "" # PID 2.9.3 - Name of Coading System
        pid2_9_4 = "" # PID 2.9.4 - Alternate Identifier
        pid2_9_5 = "" # PID 2.9.5 - Alternate Text
        pid2_9_6 = "" # PID 2.9.6 - Name Of Alternate Coding System
        pid2_9_7 = "" # PID 2.9.7 - Coding System Version Id
        pid2_9_8 = "" # PID 2.9.8 - Alternate Coding System Version Id
        pid2_9_9 = "" # PID 2.9.9 - Original Text
        pid2_10 = ""  # PID.2.10 - Assigning Agency Or Department
        pid2_10_1 = "" # PID 2.10.1 - Identifier
        pid2_10_2 = "" # PID 2.10.2 - Text
        pid2_10_3 = "" # PID 2.10.3 - Name of Coading System
        pid2_10_4 = "" # PID 2.10.4 - Alternate Identifier
        pid2_10_5 = "" # PID 2.10.5 - Alternate Text
        pid2_10_6 = "" # PID 2.10.6 - Name Of Alternate Coding System
        pid2_10_7 = "" # PID 2.10.7 - Coding System Version Id
        pid2_10_8 = "" # PID 2.10.8 - Alternate Coding System Version Id
        pid2_10_9 = "" # PID 2.10.9 - Original Text
        #pid2 = ("{pid2_1}^{pid2_2}^{pid2_3}^{pid2_4}^{pid2_5}^{pid2_6}^{pid2_7}^{pid2_8}^{pid2_9}^{pid2_10}")
        pid2 = f"{pid2_1}^{pid2_2}^{pid2_3}^{pid2_4}"
        ## PID.3 - Patient Identifier List
        pid3_1 = patID  # PID.3.1 - Id Number
        pid3_2 = ""  # PID.3.2 - Check Digit
        pid3_3 = ""  # PID.3.3 - Check Digit Scheme
        pid3_4_1 = "Social Security Administration" # PID 3.4.1 - Namespace Id
        pid3_4_2 = "SSA"# PID 3.4.2 - Universal Id
        pid3_4_3 = "CLIA" # PID 3.4.3 - Universal Id Type
        pid3_4 = (f"{pid3_4_1}&{pid3_4_2}&{pid3_4_3}")  # PID.3.4 - Assigning Authority
        pid3_5 = "SS"  # PID.3.5 - Identifier Type Code
        pid3_6_1 = "pid3_6_1" # PID 3.6.1 - Namespace Id
        pid3_6_2 = "pid3_6_2" # PID 3.6.2 - Universal Id
        pid3_6_3 = "pid3_6_3" # PID 3.6.3 - Universal Id Type
        #pid3_6 = ("{pid3_6_1}~{pid3_6_2}~{pid3_6_3}")  # PID.3.6 - Assigning Facility
        pid3_6 = ""
        pid3_7 = ""  # PID.3.7 - Effective Date
        pid3_8 = ""  # PID.3.8 - Expiration Date
        pid3_9 = ""  # PID.3.9 - Assigning Jurisdiction
        #pid3_9_1 = "pid3_9_1" # PID 3.9.1 - Identifier
        #pid3_9_2 = "pid3_9_2" # PID 3.9.2 - Text
        #pid3_9_3 = "pid3_9_3" # PID 3.9.3 - Name of Coading System
        #pid3_9_4 = "pid3_9_4" # PID 3.9.4 - Alternate Identifier
        #pid3_9_5 = "pid3_9_5" # PID 3.9.5 - Alternate Text
        #pid3_9_6 = "pid3_9_6" # PID 3.9.6 - Name Of Alternate Coding System
        #pid3_9_7 = "pid3_9_7" # PID 3.9.7 - Coding System Version Id
        #pid3_9_8 = "pid3_9_8" # PID 3.9.8 - Alternate Coding System Version Id
        #pid3_9_9 = "pid3_9_9" # PID 3.9.9 - Original Text
        pid3_10 = ""  # PID.3.10 - Assigning Agency Or Department
        #pid3_10_1 = "pid3_10_1" # PID 3.10.1 - Identifier
        #pid3_10_2 = "pid3_10_2" # PID 3.10.2 - Text
        #pid3_10_3 = "pid3_10_3" # PID 3.10.3 - Name of Coading System
        #pid3_10_4 = "pid3_10_4" # PID 3.10.4 - Alternate Identifier
        #pid3_10_5 = "pid3_10_5" # PID 3.10.5 - Alternate Text
        #pid3_10_6 = "pid3_10_6" # PID 3.10.6 - Name Of Alternate Coding System
        #pid3_10_7 = "pid3_10_7" # PID 3.10.7 - Coding System Version Id
        #pid3_10_8 = "pid3_10_8" # PID 3.10.8 - Alternate Coding System Version Id
        #pid3_10_9 = "pid3_10_9" # PID 3.10.9 - Original Text
        pid3 = (f"{pid3_1}^{pid3_2}^{pid3_3}^{pid3_4}^{pid3_5}")
        ## PID.4 - Alternate Patient ID
        pid4_1 = "pid4_1"  # PID.4.1 - Id Number
        pid4_2 = "pid4_2"  # PID.4.2 - Check Digit
        pid4_3 = "pid4_3"  # PID.4.3 - Check Digit Scheme
        pid4_4 = "pid4_4"  # PID.4.4 - Assigning Authority
        pid4_5 = "pid4_5"  # PID.4.5 - Identifier Type Code
        pid4_6 = "pid4_6" # PID.4.6 - Assigning Facility
        pid4_7 = "pid4_7" # PID.4.7 - Effective Date
        pid4_8 = "pid4_8" # PID.4.8 - Expiration Date
        pid4_9 = "pid4_9" # PID.4.9 - Assigning Jurisdiction
        pid4_10 = "pid4_10" # PID.4.10 - Assigning Agency Or Department
        #pid4 = ("{pid4_1}^{pid4_2}^{pid4_3}^{pid4_4}^{pid4_5}^{pid4_6}^{pid4_7}^{pid4_8}^{pid4_9}^{pid4_10}")
        pid4 = ""
        ## PID.5 - Patient Name
        pid5_1 = "lastname"  # PID.5.1 - Family Name
        pid5_2 = "firstname"  # PID.5.2 - Given Name
        pid5_3 = middlename  # PID.5.3 - Second And Further Given Names Or Initials Thereof
        pid5_4 = random.choice(suffix) # PID.5.4 - Suffix (e.g., Jr Or Iii)
        pid5_5 = random.choice(prefix) # PID.5.5 - Prefix (e.g., Dr)
        pid5_6 = random.choice(degree) # PID.5.6 - Degree (e.g., Md)
        #pid5_7 = "AL"  # PID.5.7 - Name Type Code
        pid5_8 = ""  # PID.5.8 - Name Representation Code
        pid5_9 = ""  # PID.5.9 - Name Context
        pid5_10 = ""  # PID.5.10 - Name Validity Range
        pid5_11 = ""  # PID.5.11 - Name Assembly Order
        pid5_12 = ""  # PID.5.12 - Effective Date
        pid5_13 = ""  # PID.5.13 - Expiration Date
        pid5_14 = ""  # PID.5.14 - Professional Suffix
        pid5 = (f"{pid5_1}^{pid5_2}^{pid5_3}^{pid5_4}^{pid5_5}^{pid5_6}")
        ## PID.6 - Mother's Maiden Name
        pid6_1 = "pid6_1"  # PID.6.1 - Family Name
        pid6_2 = "pid6_2"  # PID.6.2 - Given Name
        pid6_3 = "pid6_3"  # PID.6.3 - Second And Further Given Names Or Initials Thereof
        pid6_4 = "pid6_4"  # PID.6.4 - Suffix (e.g., Jr Or Iii)
        pid6_5 = "pid6_5"  # PID.6.5 - Prefix (e.g., Dr)
        pid6_6 = "pid6_6"  # PID.6.6 - Degree (e.g., Md)
        pid6_7 = "pid6_7"  # PID.6.7 - Name Type Code
        pid6_8 = "pid6_8"  # PID.6.8 - Name Representation Code
        pid6_9 = "pid6_9"  # PID.6.9 - Name Context
        pid6_10 = "pid6_10"  # PID.6.10 - Name Validity Range
        pid6_11 = "pid6_11"  # PID.6.11 - Name Assembly Order
        pid6_12 = "pid6_12"  # PID.6.12 - Effective Date
        pid6_13 = "pid6_13"  # PID.6.13 - Expiration Date
        pid6_14 = "pid6_14"  # PID.6.14 - Professional Suffix
        #pid6 = ("{pid6_1}^{pid6_2}^{pid6_3}^{pid6_4}^{pid6_5}^{pid6_6}^{pid6_7}^{pid6_8}^{pid6_9}^{pid6_10}^{pid6_11}^{pid6_12}^{pid6_13}^{pid6_14}")
        pid6 = fake.last_name()
        ## PID.7 - Date/Time of Birth
        pid7 = "dob" #<yyyymmdd>
        ## PID.8 - Administrative Sex
        pid8 = "patSex"
        ## PID.9 - Patient Alias
        pid9_1 = ""  # PID.9.1 - Family Name
        pid9_2 = ""  # PID.9.2 - Given Name
        pid9_3 = ""  # PID.9.3 - Second And Further Given Names Or Initials Thereof
        pid9_4 = ""  # PID.9.4 - Suffix (e.g., Jr Or Iii)
        pid9_5 = ""  # PID.9.5 - Prefix (e.g., Dr)
        pid9_6 = ""  # PID.9.6 - Degree (e.g., Md)
        pid9_7 = ""  # PID.9.7 - Name Type Code
        pid9_8 = ""  # PID.9.8 - Name Representation Code
        pid9_9 = ""  # PID.9.9 - Name Context
        pid9_10 = ""  # PID.9.10 - Name Validity Range
        pid9_11 = ""  # PID.9.11 - Name Assembly Order
        pid9_12 = ""  # PID.9.12 - Effective Date
        pid9_13 = ""  # PID.9.13 - Expiration Date
        pid9_14 = ""  # PID.9.14 - Professional Suffix
        pid9 = "Deduplication"
        ## PID.10 - Race
        #pid10_1 = patRaceCode  # PID.10.1 - Identifier
        #pid10_2 = patRace  # PID.10.2 - Text
        #pid10_3 = ""  # PID.10.3 - Name Of Coding System
        #pid10_4 = ""  # PID.10.4 - Alternate Identifier
        #pid10_5 = "SIM_TEST"  # PID.10.5 - Alternate Text
       # pid10_6 = ""  # PID.10.6 - Name Of Alternate Coding System
        #pid10 = (f"{pid10_1}^{pid10_2}^{pid10_5}")
        pid10 = "race"
        ## PID.11 - Patient Address
        pid11_1 = "address"  # PID.11.1 - Street Address
        pid11_2 = "unit" + " " + unitnumber  # PID.11.2 - Other Designation
        pid11_3 = "city"  # PID.11.3 - City
        pid11_4 = "state_abbr"  # PID.11.4 - State Or Province
        pid11_5 = "zip_code"  # PID.11.5 - Zip Or Postal Code
        pid11_6 = "USA"  # PID.11.6 - Country
        pid11_7 = ""  # PID.11.7 - Address Type
        pid11_8 = ""  # PID.11.8 - Other Geographic Designation
        pid11_9 = ""  # PID.11.9 - County/Parish Code "13135"
        pid11_10 = ""  # PID.11.10 - Census Tract
        pid11_11 = ""  # PID.11.11 - Address Representation Code
        pid11_12 = ""  # PID.11.12 - Address Validity Range
        pid11_13 = ""  # PID.11.13 - Effective Date
        pid11_14 = ""  # PID.11.14 - Expiration Date
        pid11 = (f"{pid11_1}^{pid11_2}^{pid11_3}^{pid11_4}^{pid11_5}^{pid11_6}") #^^^{pid11_9}
        pid12 = ""
        ## PID.13 - Phone Number - Home
        pid13_1 = ""  # PID.13.1 - Telephone Number
        pid13_2 = ""  # PID.13.2 - Telecommunication Use Code
        pid13_3 = ""  # PID.13.3 - Telecommunication Equipment Type
        pid13_4 = fake.first_name() + fake.last_name() + numberrn + "@" + random.choice(mails)  # PID.13.4 - Email Address
        pid13_5 = ""  # PID.13.5 - Country Code
        pid13_6 = "732"  # PID.13.6 - Area/City Code
        pid13_7 = homephone  # PID.13.7 - Local Number
        pid13_8 = extension # PID.13.8 - Extension
        pid13_9 = ""  # PID.13.9 - Any Text
        pid13_10 = ""  # PID.13.10 - Extension Prefix
        pid13_11 = ""  # PID.13.11 - Speed Dial Code
        pid13_12 = ""  # PID.13.12 - Unformatted Telephone Number
        pid13 = (f"{pid13_1}^{pid13_2}^{pid13_3}^{pid13_4}^{pid13_5}^{pid13_6}^{pid13_7}^{pid13_8}")
        ## PID.14 - Phone Number - Business
        pid14_1 = ""  # PID.14.1 - Telephone Number
        pid14_2 = ""  # PID.14.2 - Telecommunication Use Code
        pid14_3 = ""  # PID.14.3 - Telecommunication Equipment Type
        pid14_4 = email  # PID.14.4 - Email Address
        pid14_5 = ""  # PID.14.5 - Country Code
        pid14_6 = "732"  # PID.14.6 - Area/City Code
        pid14_7 = workphone  # PID.14.7 - Local Number
        pid14_8 = extension  # PID.14.8 - Extension
        pid14_9 = ""  # PID.14.9 - Any Text
        pid14_10 = ""  # PID.14.10 - Extension Prefix
        pid14_11 = ""  # PID.14.11 - Speed Dial Code
        pid14_12 = ""  # PID.14.12 - Unformatted Telephone Number
        #pid14 = ("{pid14_1}^{pid14_2}^{pid14_3}^{pid14_4}^{pid14_5}^{pid14_6}^{pid14_7}^{pid14_8}^{pid14_9}^{pid14_10}^{pid14_11}^{pid14_12}")
        pid14 = (f"^^^{pid14_4}^{pid14_5}^{pid14_6}^{pid14_7}^{pid14_8}")
        ## PID.15 - Primary Language
        pid15_1 = ""  # PID.15.1 - Identifier
        pid15_2 = "pid15_2"  # PID.15.2 - Text
        pid15_3 = "pid15_3"  # PID.15.3 - Name Of Coding System
        pid15_4 = "pid15_4"  # PID.15.4 - Alternate Identifier
        pid15_5 = "pid15_5"  # PID.15.5 - Alternate Text
        pid15_6 = "pid15_6"  # PID.15.6 - Name Of Alternate Coding System
        #pid15 = ("{pid15e1}^{pid15_2}^{pid15_3}^{pid15_4}^{pid15_5}^{pid15_6}")
        pid15 = "ENG"
        ## PID.16 - Marital Status
        pid16_1 = "T"  # PID.16.1 - Identifier
        pid16_2 = ""  # PID.16.2 - Text
        pid16_3 = ""  # PID.16.3 - Name Of Coding System
        pid16_4 = ""  # PID.16.4 - Alternate Identifier
        pid16_5 = ""  # PID.16.5 - Alternate Text
        pid16_6 = ""  # PID.16.6 - Name Of Alternate Coding System
        pid16 = (f"{pid16_1}^{pid16_2}^{pid16_3}^{pid16_4}^{pid16_5}^{pid16_6}")
        ## PID.17 - Religion
        pid17_1 = "pid17_1"  # PID.17.1 - Identifier
        pid17_2 = "pid17_2"  # PID.17.2 - Text
        pid17_3 = "pid17_3"  # PID.17.3 - Name Of Coding System
        pid17_4 = "pid17_4"  # PID.17.4 - Alternate Identifier
        pid17_5 = "pid17_5"  # PID.17.5 - Alternate Text
        pid17_6 = "pid17_6"  # PID.17.6 - Name Of Alternate Coding System
        #pid17 = ("{pid17_1}^{pid17_2}^{pid17_3}^{pid17_4}^{pid17_5}^{pid17_6}")
        pid17 = ""
        ## PID.18 - Patient Account Number
        pid18_1 = ""  # PID.18.1 - Id Number
        pid18_2 = ""  # PID.18.2 - Check Digit
        pid18_3 = ""  # PID.18.3 - Check Digit Scheme
        pid18_4_1 = assigning_authority_txt  # PID.18.4 - Namespace ID
        pid18_4_2 = assigning_authority_id  # PID.18.4 - Universal Id
        pid18_4_3 = "CLIA"  # PID.18.4 - Universal Id Type
        pid18_4 = ("f{pid18_4_1}^{pid18_4_1}^{pid18_4_1}")  # PID.18.4 - Assigning Authority
        pid18_5 = "AN"  # PID.18.5 - Identifier Type Code
        pid18_6 = ""  # PID.18.6 - Assigning Facility
        pid18_7 = ""  # PID.18.7 - Effective Date
        pid18_8 = ""  # PID.18.8 - Expiration Date
        pid18_9 = ""  # PID.18.9 - Assigning Jurisdiction
        pid18_10 = ""  # PID.18.10 - Assigning Agency Or Department
        #pid18 = ("{pid18_1}^{pid18_2}^{pid18_3}^{pid18_4}^{pid18_5}^{pid18_6}^{pid18_7}^{pid18_8}^{pid18_9}^{pid18_10}")
        pid18 = ""
        ## PID.19 - SSN Number - Patient
        pid19 = "ssn"
        ## PID.20 - Driver's License Number - Patient
        pid20_1 = ""  # PID.20.1 - License Number
        pid20_2 = ""  # PID.20.2 - Issuing State, Province, Country
        pid20_3 = ""  # PID.20.3 - Expiration Date
        #pid20 = ("{pid20_1}^{pid20_2}^{pid20_3}")
        #pid20 = (f"{pid20_1}^{pid20_2}^{pid20_3}")
 
        pid20 = ""
        ##PID.21 - Mother's Identifier
        pid21 = ""
        ##PID.22 - Ethnic Group
        pid22 = "ethnic"
        ##PID.23 - Birth Place
        pid23 = fake.city()
        ##PID.24 - Multiple Birth Indicator
        pid24 = "Y"
        ##PID.25 - Birth Order
        pid25 = "3"
        ##PID.26 - Citizenship
        pid26 = ""
        ##PID.27 - Veterans Military Status
        pid27 = ""
        ##PID.28 - Nationality
        pid28 = "USA"
        ##PID.29 - Patient Death Date and Time
        pid29 = deceaseddatetime
        ##PID.30 - Patient Death Indicator
        pid30 = "Y"
        ##PID.31 - Identity Unknown Indicator
        pid31 = ""
        ##PID.32 - Identity Reliability Code
        pid32 = ""
        ##PID.33 - Last Update Date/Time
        pid33 = ""
        ##PID.34 - Last Update Facility
        pid34 = ""
        ##PID.35 - Species Code
        pid35 = ""
        ##PID.36 - Breed Code
        pid36 = ""
        ##PID.37 - Strain
        pid37 = ""
        ##PID.38 - Production Class Code
        pid38 = ""
        ##PID.39 - Tribal Citizenship
        pid39 = ""
       
        # Assigning field values into a template
        PID = (
        f"PID|"
        f"{pid1}|{pid2}|{pid3}|{pid4}|{pid5}|{pid6}|{pid7}|{pid8}|{pid9}|{pid10}|"
        f"{pid11}|{pid12}|{pid13}|{pid14}|{pid15}|{pid16}|{pid17}|{pid18}|{pid19}|{pid20}|{pid21}|{pid22}|{pid23}|{pid24}|{pid25}|{pid26}|{pid27}|{pid28}|{pid29}|{pid30}")
       
        #-------- PV1 ------------
 
        # The PV1 segment is used by Registration/Patient Administration applications to communicate information on an account or visit-specific basis.
       
        # Creating values for PV1_2
        PV1_2_values = {"B", "C", "E", "I", "O", "N", "P", "R", "U"}
        PV1_2_choice = random.choice(list(PV1_2_values))
 
        # Generating variables for PV1 Segemnt
        pv1_1 = "" # PV1.1 - Set ID - PV1
        pv1_2 = PV1_2_choice # PV1.2 - Patient Class ----- R
        pv1_3 = "" # PV1.3 - Assigned Patient Location
        pv1_4 = "" # PV1.4 - Admission Type
        pv1_5 = "" # PV1.5 - Preadmit Number
        pv1_6 = "" # PV1.6 - Prior Patient Location
        pv1_7 = "" # PV1.7 - Attending Doctor
        pv1_8 = "" # PV1.8 - Referring Doctor
        pv1_9 = "" # PV1.9 - Consulting Doctor ----- B
        pv1_10 = "" # PV1.10 - Hospital Service
        pv1_11 = "" # PV1.11 - Temporary Location
        pv1_12 = "" # PV1.12 - Preadmit Test Indicator
        pv1_13 = "" # PV1.13 - Re-admission Indicator
        pv1_14 = "" # PV1.14 - Admit Source
        pv1_15 = "" # PV1.15 - Ambulatory Status
        pv1_16 = "" # PV1.16 - VIP Indicator
        pv1_17 = "" # PV1.17 - Admitting Doctor
        pv1_18 = "" # PV1.18 - Patient Type
        pv1_19 = "" # PV1.19 - Visit Number
        pv1_20 = "" # PV1.20 - Financial Class
        pv1_21 = "" # PV1.21 - Charge Price Indicator
        pv1_22 = "" # PV1.22 - Courtesy Code
        pv1_23 = "" # PV1.23 - Credit Rating
        pv1_24 = "" # PV1.24 - Contract Code
        pv1_25 = "" # PV1.25 - Contract Effective Date
        pv1_26 = "" # PV1.26 - Contract Amount
        pv1_27 = "" # PV1.27 - Contract Period
        pv1_28 = "" # PV1.28 - Interest Code
        pv1_29 = "" # PV1.29 - Transfer to Bad Debt Code
        pv1_30 = "" # PV1.30 - Transfer to Bad Debt Date
        pv1_31 = "" # PV1.31 - Bad Debt Agency Code
        pv1_32 = "" # PV1.32 - Bad Debt Transfer Amount
        pv1_33 = "" # PV1.33 - Bad Debt Recovery Amount
        pv1_34 = "" # PV1.34 - Delete Account Indicator
        pv1_35 = "" # PV1.35 - Delete Account Date
        pv1_36 = "" # PV1.36 - Discharge Disposition
        pv1_37 = "" # PV1.37 - Discharged to Location
        pv1_38 = "" # PV1.38 - Diet Type
        pv1_39 = "" # PV1.39 - Servicing Facility
        pv1_40 = "" # PV1.40 - Bed Status ----- B
        pv1_41 = "" # PV1.41 - Account Status
        pv1_42 = "" # PV1.42 - Pending Location
        pv1_43 = "" # PV1.43 - Prior Temporary Location
        pv1_44 = "" # PV1.44 - Admit Date/Time
        pv1_45 = "" # PV1.45 - Discharge Date/Time
        pv1_46 = "" # PV1.46 - Current Patient Balance
        pv1_47 = "" # PV1.47 - Total Charges
        pv1_48 = "" # PV1.48 - Total Adjustments
        pv1_49 = "" # PV1.49 - Total Payments
        pv1_50 = "" # PV1.50 - Alternate Visit ID
        pv1_51 = "" # PV1.51 - Visit Indicator
        pv1_52 = "" # PV1.52 - Other Healthcare Provider ------ B
 
        # Concatenate all variables with pipe separator
        PV1_body = "|".join([pv1_1, pv1_2])
 
        PV1 = f"PV1|{PV1_body}"
 
        orc1 = "RE"
        orc2 = ""
        orc3_1 = fake.random_number(digits=11, fix_len=True)
        orc3_2 = fake.company()
        authh_random_row = assign_df.sample(n=1)
        authoritynew = authh_random_row.to_string(index=False)
        orc3_3 = re.sub(" : [^_]*", "", authoritynew).lstrip()
        orc3_4 = "CLIA"
        orc3 = (f"{orc3_1}^{orc3_2}^{orc3_3}^{orc3_4}")
        orc4 = ""
        orc5 = "N"
        orc6 = ""
        orc7 = ""
        orc8 = ""
        orc9 = ""
        orc10 = ""
        orc11 = ""
        orc12 = ""
        orc13 = ""
        orc14 = ""
        orc15 = ""
        orc16 = ""
        orc17 = ""
        orc18 = ""
        orc19 = ""
        orc20 = ""
        orc21 = fake.company()
        orc22_1 = fake.street_address()
        orc22_2 = "unit" + " " + fake.building_number()
        orc22_3 = fake.city()
        orc22_4 =  fake.state_abbr()
        orc22_5 = fake.zipcode()
        orc22_6 =  "USA"
        orc22 = (f"{orc22_1}^{orc22_2}^{orc22_3}^{orc22_4}^{orc22_5}^{orc22_6}")
        orc23_6 = "979"
        orc23_7 = fake.bothify(text='#######')
        orc23_8 = fake.random_int(min=1000, max=9999)
        orc23 = (f"^^^^^^{orc23_6}^{orc23_7}^{orc23_8}")
        orc24_1 = fake.street_address()
        orc24_2 = "unit" + " " + fake.building_number()
        orc24_3 = fake.city()
        orc24_4 =  fake.state_abbr()
        orc24_5 = fake.zipcode()
        orc24_6 = "USA"
        orc24 = (f"{orc24_1}^{orc24_2}^{orc24_3}^{orc24_4}^{orc24_5}^{orc24_6}")
        ORC = (
        f"ORC|"
        f"{orc1}|{orc2}|{orc3}|{orc4}|{orc5}|{orc6}|{orc7}|{orc8}|{orc9}|{orc10}|{orc11}|{orc12}|{orc13}|{orc14}|{orc15}|{orc16}|{orc17}|{orc18}|{orc19}|{orc20}|{orc21}|{orc22}|{orc23}|{orc24}")
 
       
 
        ## OBR - This segment is used to transmit information specific to an order for a diagnostic study or observation, physical exam, or assessment.
        obr1 = "1"  #OBR_1 - Set ID - OBR -- has to be incremental based on the Observations existing
 
        #obr_2 - Placer Order Number
        obr2_1 = numberrn # obr_2_1 - Entity Identifier
        obr2_2 = sending_facility_txt # obr_2_2 - Namespace Id
        obr2_3 = sending_facility_id # obr_2_3 - Universal Id
        obr2_4 = "" # obr_2_4 - Universal Id Type
        obr2 = (f"{obr2_1}^{obr2_2}^{obr2_3}^{obr2_4}") # obr_2 - Placer Order Number
       
        #obr_3 - Filler Order Number
        obr3_1 = random_alphanumeric_value # obr_3.1 - Entity Identifier
        obr3_2 = assigning_authority_txt # obr_3.2 - Namespace Id
        obr3_3 = assigning_authority_id # obr_3.3 - Universal Id
        obr3_4 = "CLIA" # obr_3.4 - Universal Id Type
        obr3 = (f"{obr3_1}^{obr3_2}^{obr3_3}^{obr3_4}") # obr_2 - Placer Order Number
       
        #obr_4 - Universal Service Identifier
        obr4_1 = patDiseaseCode
        #formatted_number
        #patDiseaseCode # obr_4.1 - Identifier
        obr4_2 = patDisease # obr_4.2 - Text
        obr4_3 = "LN" # obr_4.3 - Name Of Coding System
        obr4_4 = numberrn # obr_4.4 - Alternate Identifier
        obr4_5 = "TestData" # obr_4.5 - Alternate Text
        obr4_6 = "L" # obr_4.6 - Name Of Alternate Coding System
        obr4 = (f"{obr4_1}^{obr4_2}^{obr4_3}^{obr4_4}^{obr4_5}^{obr4_6}")
       
        obr5 = "S" #obr_5 - Priority - OBR
        obr6 = "" #obr_6 - Requested Date/Time
        #obr_6.1 - Time
        #obr_6.2 - Degree Of Precision
       
        obr7 = hl7_datetime # obr_7 - Observation Date/Time
       
        obr8 = future_time_hl7_datetime # obr_8 - Observation End Date/Time
       
        obr9 = "" #obr_9 - Collection Volume
        #obr_9.1 - Quantity
        #obr_9.2 - Units
       
        obr10 = "" #obr_10 - Collector Identifier
        #obr_10.1 - Id Number
        #obr_10.2 - Family Name
        #obr_10.2.1 - Surname
        #obr_10.2.2 - Own Surname Prefix
        #obr_10.2.3 - Own Surname
        #obr_10.2.4 - Surname Prefix From Partner/Spouse
        #obr_10.2.5 - Surname From Partner/Spouse
        #obr_10.3 - Given Name
        #obr_10.4 - Second And Further Given Names Or Initials Thereof
        #obr_10.5 - Suffix (e.g., Jr Or Iii)
        #obr_10.6 - Prefix (e.g., Dr)
        #obr_10.7 - Degree (e.g., Md)
        #obr_10.8 - Source Table
        #obr_10.9 - Assigning Authority
        #obr_10.9.1 - Namespace Id
        #obr_10.9.2 - Universal Id
        #obr_10.9.3 - Universal Id Type
        #obr_10.10 - Name Type Code
        #obr_10.11 - Identifier Check Digit
        #obr_10.12 - Check Digit Scheme
        #obr_10.13 - Identifier Type Code
        #obr_10.14 - Assigning Facility
        #obr_10.14.1 - Namespace Id
        #obr_10.14.2 - Universal Id
        #obr_10.14.3 - Universal Id Type
        #obr_10.15 - Name Representation Code
        #obr_10.16 - Name Context
        #obr_10.16.1 - Identifier
        #obr_10.16.2 - Text
        #obr_10.16.3 - Name Of Coding System
        #obr_10.16.4 - Alternate Identifier
        #obr_10.16.5 - Alternate Text
        #obr_10.16.6 - Name Of Alternate Coding System
        #obr_10.17 - Name Validity Range
        #obr_10.17.1 - Range Start Date/Time
        #obr_10.17.1.1 - Time
        #obr_10.17.1.2 - Degree Of Precision
        #obr_10.17.2 - Range End Date/Time
        #obr_10.17.2.1 - Time
        #obr_10.17.2.2 - Degree Of Precision
        #obr_10.18 - Name Assembly Order
        #obr_10.19 - Effective Date
        #obr_10.19.1 - Time
        #obr_10.19.2 - Degree Of Precision
        #obr_10.20 - Expiration Date
        #obr_10.20.1 - Time
        #obr_10.20.2 - Degree Of Precision
        #obr_10.21 - Professional Suffix
        #obr_10.22 - Assigning Jurisdiction
        #obr_10.22.1 - Identifier
        #obr_10.22.2 - Text
        #obr_10.22.3 - Name Of Coding System
        #obr_10.22.4 - Alternate Identifier
        #obr_10.22.5 - Alternate Text
        #obr_10.22.6 - Name Of Alternate Coding System
        #obr_10.22.7 - Coding System Version Id
        #obr_10.22.8 - Alternate Coding System Version Id
        #obr_10.22.9 - Original Text
        #obr_10.23 - Assigning Agency Or Department
        #obr_10.23.1 - Identifier
        #obr_10.23.2 - Text
        #obr_10.23.3 - Name Of Coding System
        #obr_10.23.4 - Alternate Identifier
        #obr_10.23.5 - Alternate Text
        #obr_10.23.6 - Name Of Alternate Coding System
        #obr_10.23.7 - Coding System Version Id
        #obr_10.23.8 - Alternate Coding System Version Id
        #obr_10.23.9 - Original Text
       
        obr11 = "" #obr_11 - Specimen Action Code
        obr12 = "BLD" #obr_12 - Danger Code
        #obr_12.1 - Identifier
        #obr_12.2 - Text
        #obr_12.3 - Name Of Coding System
        #obr_12.4 - Alternate Identifier
        #obr_12.5 - Alternate Text
        #obr_12.6 - Name Of Alternate Coding System
       
        obr13 = clinical_information #obr_13 - Relevant Clinical Information
       
        obr14 = hl7_datetime # obr_14 - Specimen Received Date/Time
       
        obr15 = "" #obr_15 - Specimen Source
        #obr_15.1 - Specimen Source Name Or Code
        #obr_15.1.1 - Identifier
        #obr_15.1.2 - Text
        #obr_15.1.3 - Name Of Coding System
        #obr_15.1.4 - Alternate Identifier
        #obr_15.1.5 - Alternate Text
        #obr_15.1.6 - Name Of Alternate Coding System
        #obr_15.1.7 - Coding System Version Id
        #obr_15.1.8 - Alternate Coding System Version Id
        #obr_15.1.9 - Original Text
        #obr_15.2 - Additives
        #obr_15.2.1 - Identifier
        #obr_15.2.2 - Text
        #obr_15.2.3 - Name Of Coding System
        #obr_15.2.4 - Alternate Identifier
        #obr_15.2.5 - Alternate Text
        #obr_15.2.6 - Name Of Alternate Coding System
        #obr_15.2.7 - Coding System Version Id
        #obr_15.2.8 - Alternate Coding System Version Id
        #obr_15.2.9 - Original Text
        #obr_15.3 - Specimen Collection Method
        #obr_15.4 - Body Site
        #obr_15.4.1 - Identifier
        #obr_15.4.2 - Text
        #obr_15.4.3 - Name Of Coding System
        #obr_15.4.4 - Alternate Identifier
        #obr_15.4.5 - Alternate Text
        #obr_15.4.6 - Name Of Alternate Coding System
        #obr_15.4.7 - Coding System Version Id
        #obr_15.4.8 - Alternate Coding System Version Id
        #obr_15.4.9 - Original Text
        #obr_15.5 - Site Modifier
        #obr_15.5.1 - Identifier
        #obr_15.5.2 - Text
        #obr_15.5.3 - Name Of Coding System
        #obr_15.5.4 - Alternate Identifier
        #obr_15.5.5 - Alternate Text
        #obr_15.5.6 - Name Of Alternate Coding System
        #obr_15.5.7 - Coding System Version Id
        #obr_15.5.8 - Alternate Coding System Version Id
        #obr_15.5.9 - Original Text
        #obr_15.6 - Collection Method Modifier Code
        #obr_15.6.1 - Identifier
        #obr_15.6.2 - Text
        #obr_15.6.3 - Name Of Coding System
        #obr_15.6.4 - Alternate Identifier
        #obr_15.6.5 - Alternate Text
        #obr_15.6.6 - Name Of Alternate Coding System
        #obr_15.6.7 - Coding System Version Id
        #obr_15.6.8 - Alternate Coding System Version Id
        #obr_15.6.9 - Original Text
        #obr_15.7 - Specimen Role
        #obr_15.7.1 - Identifier
        #obr_15.7.2 - Text
        #obr_15.7.3 - Name Of Coding System
        #obr_15.7.4 - Alternate Identifier
        #obr_15.7.5 - Alternate Text
        #obr_15.7.6 - Name Of Alternate Coding System
        #obr_15.7.7 - Coding System Version Id
        #obr_15.7.8 - Alternate Coding System Version Id
        #obr_15.7.9 - Original Text
       
        # obr_16 - Ordering Provider
        obr16_1 = str(random.randint(1000000, 9999999)) # obr_16.1 - Id Number
        obr16_2 = fake.last_name() #obr_16.2 - Family Name
        #obr_16.2.1 - Surname
        #obr_16.2.2 - Own Surname Prefix
        #obr_16.2.3 - Own Surname
        #obr_16.2.4 - Surname Prefix From Partner/Spouse
        #obr_16.2.5 - Surname From Partner/Spouse
        obr16_3 = fake.first_name() #obr_16.3 - Given Name
        #obr_16.4 - Second And Further Given Names Or Initials Thereof
        obr16_5 = random.choice(suffix) #obr_16.5 - Suffix (e.g., Jr Or Iii)
        obr16_6 = random.choice(prefix) #obr_16.6 - Prefix (e.g., Dr)
        if obr16_6 == "Dr":
            obr16_7 = random.choice(docDegree)
        else:
            obr16_7 = random.choice(degree) #obr_16.7 - Degree (e.g., Md)
        #obr_16.8 - Source Table
        #obr_16.9 - Assigning Authority
        #obr_16.9.1 - Namespace Id
        #obr_16.9.2 - Universal Id
        #obr_16.9.3 - Universal Id Type
        #obr_16.10 - Name Type Code
        #obr_16.11 - Identifier Check Digit
        #obr_16.12 - Check Digit Scheme
        #obr_16.13 - Identifier Type Code
        #obr_16.14 - Assigning Facility
        #obr_16.14.1 - Namespace Id
        #obr_16.14.2 - Universal Id
        #obr_16.14.3 - Universal Id Type
        #obr_16.15 - Name Representation Code
        #obr_16.16 - Name Context
        #obr_16.16.1 - Identifier
        #obr_16.16.2 - Text
        #obr_16.16.3 - Name Of Coding System
        #obr_16.16.4 - Alternate Identifier
        #obr_16.16.5 - Alternate Text
        #obr_16.16.6 - Name Of Alternate Coding System
        #obr_16.17 - Name Validity Range
        #obr_16.17.1 - Range Start Date/Time
        #obr_16.17.1.1 - Time
        #obr_16.17.1.2 - Degree Of Precision
        #obr_16.17.2 - Range End Date/Time
        #obr_16.17.2.1 - Time
        #obr_16.17.2.2 - Degree Of Precision
        #obr_16.18 - Name Assembly Order
        #obr_16.19 - Effective Date
        #obr_16.19.1 - Time
        #obr_16.19.1 - Degree Of Precision
        #obr_16.20 - Expiration Date
        #obr_16.20.1 - Time
        #obr_16.20.1 - Degree Of Precision       
        #obr_16.21 - Professional Suffix
        #obr_16.22 - Assigning Jurisdiction
        #obr_16.22.1 - Identifier
        #obr_16.22.2 - Text
        #obr_16.22.3 - Name Of Coding System
        #obr_16.22.4 - Alternate Identifier
        #obr_16.22.5 - Alternate Text
        #obr_16.22.6 - Name Of Alternate Coding System
        #obr_16.22.7 - Coding System Version Id
        #obr_16.22.8 - Alternate Coding System Version Id
        #obr_16.22.9 - Original Text
        #obr_16.23 - Assigning Agency Or Department
        #obr_16.23.1 - Identifier
        #obr_16.23.2 - Text
        #obr_16.23.3 - Name Of Coding System
        #obr_16.23.4 - Alternate Identifier
        #obr_16.23.5 - Alternate Text
        #obr_16.23.6 - Name Of Alternate Coding System
        #obr_16.23.7 - Coding System Version Id
        #obr_16.23.8 - Alternate Coding System Version Id
        #obr_16.23.9 - Original Text
        obr16 = (f"{obr16_1}^{obr16_2}^{obr16_3}^{obr16_5}^{obr16_6}^{obr16_7}")
       
        # obr_17 - Order Callback Phone Number
        obr17_1 = phone # obr_17.1 - Telephone Number
        obr17_2 = "" #obr_17.2 - Telecommunication Use Code
        obr17_3 = "" #obr_17.3 - Telecommunication Equipment Type
        obr17_4 = fake.first_name() + fake.last_name() + numberrn + "@" + random.choice(mails) # obr_17.4 - Email Address
        #obr_17.5 - Country Code
        #obr_17.6 - Area/City Code
        #obr_17.7 - Local Number
        #obr_17.8 - Extension
        #obr_17.9 - Any Text
        #obr_17.10 - Extension Prefix
        #obr_17.11 - Speed Dial Code
        #obr_17.12 - Unformatted Telephone Number
        obr17 = (f"{obr17_1}^{obr17_2}^{obr17_3}^{obr17_4}")
       
        obr18 = "" #obr_18 - Placer Field 1
        obr19 = "" #obr_19 - Placer Field 2
        obr20 = "" #obr_20 - Filler Field 1
        obr21 = "" #obr_21 - Filler Field 2
       
        obr22 = future_time_hl7_datetime # obr_22 - Results Rpt/Status Chng - Date/Time
        #obr_22.1 - Time
        #obr_22.1 - Degree Of Precision
       
        obr23 = "" #obr_23 - Charge to Practice
        #obr_23.1 - Monetary Amount
        #obr_23.1.1 - Quantity
        #obr_23.1.2 - Denomination
        #obr_23.2 - Charge Code
        #obr_23.2.1 - Identifier
        #obr_23.2.2 - Text
        #obr_23.2.3 - Name Of Coding System
        #obr_23.2.4 - Alternate Identifier
        #obr_23.2.5 - Alternate Text
        #obr_23.2.6 - Name Of Alternate Coding System
       
        obr24 = "" #obr_24 - Diagnostic Serv Sect ID
       
        obr25 = random.choice(resultStatus) # obr_25 - Result Status
       
        obr26 = "" #obr_26 - Parent Result
        #obr_26.1 - Parent Observation Identifier
        #obr_26.1.1 - Identifier
        #obr_26.1.2 - Text
        #obr_26.1.3 - Name Of Coding System
        #obr_26.1.4 - Alternate Identifier
        #obr_26.1.5 - Alternate Text
        #obr_26.1.6 - Name Of Alternate Coding System
        #obr_26.2 - Parent Observation Sub-identifier
        #obr_26.3 - Parent Observation Value Descriptor
       
        obr27 = "" #obr_27 - Quantity/Timing
        #obr_27.1 - Quantity
        #obr_27.1.1 - Quantity
        #obr_27.1.2 - Units
        #obr_27.1.1 - Identifier
        #obr_27.1.2 - Text
        #obr_27.1.3 - Name Of Coding System
        #obr_27.1.4 - Alternate Identifier
        #obr_27.1.5 - Alternate Text
        #obr_27.1.6 - Name Of Alternate Coding System
        #obr_27.2 - Interval
        #obr_27.2.1 - Repeat Pattern
        #obr_27.2.2 - Explicit Time Interval
        #obr_27.3 - Duration
        #obr_27.4 - Start Date/Time
        #obr_27.4.1 - Time
        #obr_27.4.2 - Degree Of Precision
        #obr_27.5 - End Date/Time
        #obr_27.5.1 - Time
        #obr_27.5.2 - Degree Of Precision
        #obr_27.6 - Priority
        #obr_27.7 - Condition
        #obr_27.8 - Text
        #obr_27.9 - Conjunction
        #obr_27.10 - Order Sequencing
        #obr_27.10.1 - Sequence/Results Flag
        #obr_27.10.2 - Placer Order Number: Entity Identifier
        #obr_27.10.3 - Placer Order Number: Namespace Id
        #obr_27.10.4 - Filler Order Number: Entity Identifier
        #obr_27.10.5 - Filler Order Number: Namespace Id
        #obr_27.10.6 - Sequence Condition Value
        #obr_27.10.7 - Maximum Number Of Repeats
        #obr_27.10.8 - Placer Order Number: Universal Id
        #obr_27.10.9 - Placer Order Number: Universal Id Type
        #obr_27.10.10 - Filler Order Number: Universal Id
        #obr_27.10.11 - Filler Order Number: Universal Id Type
        #obr_27.11 - Occurrence Duration
        #obr_27.11.1 - Identifier
        #obr_27.11.2 - Text
        #obr_27.11.3 - Name Of Coding System
        #obr_27.11.4 - Alternate Identifier
        #obr_27.11.5 - Alternate Text
        #obr_27.11.6 - Name Of Alternate Coding System
        #obr_27.12 - Total Occurrences
       
        # obr_28 - Result Copies To
        obr28_1 = str(random.randint(1000000, 9999999)) # obr_28.1 - Id Number
        obr28_2 = fake.last_name() # obr_28.2 - Family Name
        #obr_28.2.1 - Surname
        #obr_28.2.2 - Own Surname Prefix
        #obr_28.2.3 - Own Surname
        #obr_28.2.4 - Surname Prefix From Partner/Spouse
        #obr_28.2.5 - Surname From Partner/Spouse
        obr28_3 = fake.first_name() # obr_28.3 - Given Name
        #obr_28.4 - Second And Further Given Names Or Initials Thereof
        obr28_5 = random.choice(suffix) #obr_28.5 - Suffix (e.g., Jr Or Iii)
        obr28_6 = random.choice(prefix) #obr_28.6 - Prefix (e.g., Dr)
        if obr28_6 == "Dr":
            obr28_7 = random.choice(docDegree)
        else:
            obr28_7 = random.choice(degree) #obr_16.7 - Degree (e.g., Md)
        #obr_28.8 - Source Table
        #obr_28.9 - Assigning Authority
        #obr_28.9.1 - Namespace Id
        #obr_28.9.2 - Universal Id
        #obr_28.9.3 - Universal Id Type
        #obr_28.10 - Name Type Code
        #obr_28.11 - Identifier Check Digit
        #obr_28.12 - Check Digit Scheme
        #obr_28.13 - Identifier Type Code
        #obr_28.14 - Assigning Facility
        #obr_28.14.1 - Namespace Id
        #obr_28.14.2 - Universal Id
        #obr_28.14.3 - Universal Id Type
        #obr_28.15 - Name Representation Code
        #obr_28.16 - Name Context
        #obr_28.16.1 - Identifier
        #obr_28.16.2 - Text
        #obr_28.16.3 - Name Of Coding System
        #obr_28.16.4 - Alternate Identifier
        #obr_28.16.5 - Alternate Text
        #obr_28.16.6 - Name Of Alternate Coding System
        #obr_28.17 - Name Validity Range
        #obr_28.17.1 - Range Start Date/Time
        #obr_28.17.1.1 - Time
        #obr_28.17.1.2 - Degree Of Precision
        #obr_28.17.2 - Range End Date/Time
        #obr_28.17.2.1 - Time
        #obr_28.17.2.2 - Degree Of Precision
        #obr_28.18 - Name Assembly Order
        #obr_28.19 - Effective Date
        #obr_28.19.1 - Time
        #obr_28.19.2 - Degree Of Precision
        #obr_28.20 - Expiration Date
        #obr_28.20.1 - Time
        #obr_28.20.2 - Degree Of Precision
        #obr_28.21 - Professional Suffix
        #obr_28.22 - Assigning Jurisdiction
        #obr_28.22.1 - Identifier
        #obr_28.22.2 - Text
        #obr_28.22.3 - Name Of Coding System
        #obr_28.22.4 - Alternate Identifier
        #obr_28.22.5 - Alternate Text
        #obr_28.22.6 - Name Of Alternate Coding System
        #obr_28.22.7 - Coding System Version Id
        #obr_28.22.8 - Alternate Coding System Version Id
        #obr_28.22.9 - Original Text
        #obr_28.23 - Assigning Agency Or Department
        #obr_28.23.1 - Identifier
        #obr_28.23.2 - Text
        #obr_28.23.3 - Name Of Coding System
        #obr_28.23.4 - Alternate Identifier
        #obr_28.23.5 - Alternate Text
        #obr_28.23.6 - Name Of Alternate Coding System
        #obr_28.23.7 - Coding System Version Id
        #obr_28.23.8 - Alternate Coding System Version Id
        #obr_28.23.9 - Original Text
        obr28 = (f"{obr28_1}^{obr28_2}^{obr28_3}^{obr28_5}^{obr28_6}^{obr28_7}")
       
        #obr_29 - Parent
        #obr_29.1 - Placer Assigned Identifier
        #obr_29.1.1 - Entity Identifier
        #obr_29.1.2 - Namespace Id
        #obr_29.1.3 - Universal Id
        #obr_29.1.4 - Universal Id Type
        #obr_29.2 - Filler Assigned Identifier
        #obr_29.2.1 - Entity Identifier
        #obr_29.2.2 - Namespace Id
        #obr_29.2.3 - Universal Id
        #obr_29.2.4 - Universal Id Type
        obr29 = ""
 
       
        #obr_30 - Transportation Mode
        obr30 = ""
       
        #obr_31 - Reason for Study
        obr31_1 = str(random.randint(10000, 99999)) # obr_31.1 - Identifier
        obr31_2 = reasonTxt # obr_31.2 - Text
        obr31_3 = reasonCode # obr_31.3 - Name Of Coding System
        #obr_31.4 - Alternate Identifier
        #obr_31.5 - Alternate Text
        #obr_31.6 - Name Of Alternate Coding System
        obr31 = (f"{obr31_1}^{obr31_2}^{obr31_3}")
       
        #obr_32 - Principal Result Interpreter
        obr32_1_1 = str(random.randint(10000, 99999)) # obr_32.1.1 - Id Number
        obr32_1_2 = fake.last_name() # obr_32.1.2 - Family Name
        obr32_1_3 = fake.first_name() # obr_32.1.3 - Given Name
        obr32_1_4 = "" #obr_32.1.4 - Second And Further Given Names Or Initials Thereof
        obr32_1_5 = random.choice(suffix) # obr_32.1.5 - Suffix
        obr32_1_6 = random.choice(prefix) #obr_32.1.6 - Prefix (e.g., Dr)
        if obr32_1_6 == "Dr":
            obr32_1_7 = random.choice(docDegree)
        else:
            obr32_1_7 = random.choice(degree) #obr_32.1.7 - Degree (e.g., Md)
        #obr_32.1.6 - Prefix
        #obr_32.1.7 - Degree
        #obr_32.1.8 - Source Table
        #obr_32.1.9 - Assigning Authority - Namespace Id
        #obr_32.1.10 - Assigning Authority- Universal Id
        #obr_32.1.11 - Assigning Authority - Universal Id Type
        obr32_1 = (f"{obr32_1_1}&{obr32_1_2}&{obr32_1_3}&{obr32_1_4}&{obr32_1_5}&{obr32_1_6}&{obr32_1_7}") # obr_32.1 - Name
       
        obr32_2 = hl7_datetime # obr_32.2 - Start Date/Time
        #obr_32.2.1 - Time
        #obr_32.2.2 - Degree Of Precision
        obr32_3 = future_time_hl7_datetime # obr_32.3 - End Date/Time
        #obr_32.3.1 - Time
        #obr_32.3.2 - Degree Of Precision
        #obr_32.4 - Point Of Care
        #obr_32.5 - Room
        #obr_32.6 - Bed
        #obr_32.7 - Facility
        #obr_32.7.1 - Namespace Id
        #obr_32.7.2 - Universal Id
        #obr_32.7.3 - Universal Id Type
        #obr_32.8 - Location Status
        #obr_32.9 - Patient Location Type
        #obr_32.10 - Building
        #obr_32.11 - Floor
        obr32 = (f"{obr32_1}^{obr32_2}^{obr32_3}")
       
        #obr_33 - Assistant Result Interpreter
        #obr_33.1 - Name
        #obr_33.1.1 - Id Number
        #obr_33.1.2 - Family Name
        #obr_33.1.3 - Given Name
        #obr_33.1.4 - Second And Further Given Names Or Initials Thereof
        #obr_33.1.5 - Suffix
        #obr_33.1.6 - Prefix
        #obr_33.1.7 - Degree
        #obr_33.1.8 - Source Table
        #obr_33.1.9 - Assigning Authority - Namespace Id
        #obr_33.1.10 - Assigning Authority- Universal Id
        #obr_33.1.11 - Assigning Authority - Universal Id Type
        #obr_33.2 - Start Date/Time
        #obr_33.2.1 - Time
        #obr_33.2.2 - Degree Of Precision
        #obr_33.3 - End Date/Time
        #obr_33.3.1 - Time
        #obr_33.3.2 - Degree Of Precision
        #obr_33.4 - Point Of Care
        #obr_33.5 - Room
        #obr_33.6 - Bed
        #obr_33.7 - Facility
        #obr_33.7.1 - Namespace Id
        #obr_33.7.2 - Universal Id
        #obr_33.7.3 - Universal Id Type
        #obr_33.8 - Location Status
        #obr_33.9 - Patient Location Type
        #obr_33.10 - Building
        #obr_33.11 - Floor
       
        #obr_34 - Technician
        #obr_34.1 - Name
        #obr_34.1.1 - Id Number
        #obr_34.1.2 - Family Name
        #obr_34.1.3 - Given Name
        #obr_34.1.4 - Second And Further Given Names Or Initials Thereof
        #obr_34.1.5 - Suffix
        #obr_34.1.6 - Prefix
        #obr_34.1.7 - Degree
        #obr_34.1.8 - Source Table
        #obr_34.1.9 - Assigning Authority - Namespace Id
        #obr_34.1.10 - Assigning Authority- Universal Id
        #obr_34.1.11 - Assigning Authority - Universal Id Type
        #obr_34.2 - Start Date/Time
        #obr_34.2.1 - Time
        #obr_34.2.2 - Degree Of Precision
        #obr_34.3 - End Date/Time
        #obr_34.3.1 - Time
        #obr_34.3.2 - Degree Of Precision
        #obr_34.4 - Point Of Care
        #obr_34.5 - Room
        #obr_34.6 - Bed
        #obr_34.7 - Facility
        #obr_34.7.1 - Namespace Id
        #obr_34.7.2 - Universal Id
        #obr_34.7.3 - Universal Id Type
        #obr_34.8 - Location Status
        #obr_34.9 - Patient Location Type
        #obr_34.10 - Building
        #obr_34.11 - Floor
       
        #obr_35 - Transcriptionist
        #obr_35.1 - Name
        #obr_35.1.1 - Id Number
        #obr_35.1.2 - Family Name
        #obr_35.1.3 - Given Name
        #obr_35.1.4 - Second And Further Given Names Or Initials Thereof
        #obr_35.1.5 - Suffix
        #obr_35.1.6 - Prefix
        #obr_35.1.7 - Degree
        #obr_35.1.8 - Source Table
        #obr_35.1.9 - Assigning Authority - Namespace Id
        #obr_35.1.10 - Assigning Authority- Universal Id
        #obr_35.1.11 - Assigning Authority - Universal Id Type
        #obr_35.2 - Start Date/Time
        #obr_35.2.1 - Time
        #obr_35.2.2 - Degree Of Precision
        #obr_35.3 - End Date/Time
        #obr_35.3.1 - Time
        #obr_35.3.2 - Degree Of Precision
        #obr_35.4 - Point Of Care
        #obr_35.5 - Room
        #obr_35.6 - Bed
        #obr_35.7 - Facility
        #obr_35.7.1 - Namespace Id
        #obr_35.7.2 - Universal Id
        #obr_35.7.3 - Universal Id Type
        #obr_35.8 - Location Status
        #obr_35.9 - Patient Location Type
        #obr_35.10 - Building
        #obr_35.11 - Floor
       
        #obr_36 - Scheduled Date/Time
        #obr_36.1 - Time
        #obr_36.2 - Degree Of Precision
       
        #obr_37 - Number of Sample Containers
       
        #obr_38 - Transport Logistics of Collected Sample
        #obr_38.1 - Identifier
        #obr_38.2 - Text
        #obr_38.3 - Name Of Coding System
        #obr_38.4 - Alternate Identifier
        #obr_38.5 - Alternate Text
        #obr_38.6 - Name Of Alternate Coding System
       
        #obr_39 - Collector's Comment
        #obr_39.1 - Identifier
        #obr_39.2 - Text
        #obr_39.3 - Name Of Coding System
        #obr_39.4 - Alternate Identifier
        #obr_39.5 - Alternate Text
        #obr_39.6 - Name Of Alternate Coding System
       
        #obr_40 - Transport Arrangement Responsibility
        #obr_40.1 - Identifier
        #obr_40.2 - Text
        #obr_40.3 - Name Of Coding System
        #obr_40.4 - Alternate Identifier
        #obr_40.5 - Alternate Text
        #obr_40.6 - Name Of Alternate Coding System
        #obr_41 - Transport Arranged
        #obr_42 - Escort Required
        #obr_43 - Planned Patient Transport Comment
        #obr_43.1 - Identifier
        #obr_43.2 - Text
        #obr_43.3 - Name Of Coding System
        #obr_43.4 - Alternate Identifier
        #obr_43.5 - Alternate Text
        #obr_43.6 - Name Of Alternate Coding System
        #obr_44 - Procedure Code
        #obr_44.1 - Identifier
        #obr_44.2 - Text
        #obr_44.3 - Name Of Coding System
        #obr_44.4 - Alternate Identifier
        #obr_44.5 - Alternate Text
        #obr_44.6 - Name Of Alternate Coding System
        #obr_45 - Procedure Code Modifier
        #obr_45.1 - Identifier
        #obr_45.2 - Text
        #obr_45.3 - Name Of Coding System
        #obr_45.4 - Alternate Identifier
        #obr_45.5 - Alternate Text
        #obr_45.6 - Name Of Alternate Coding System
        #obr_46 - Placer Supplemental Service Information
        #obr_46.1 - Identifier
        #obr_46.2 - Text
        #obr_46.3 - Name Of Coding System
        #obr_46.4 - Alternate Identifier
        #obr_46.5 - Alternate Text
        #obr_46.6 - Name Of Alternate Coding System
        #obr_47 - Filler Supplemental Service Information
        #obr_47.1 - Identifier
        #obr_47.2 - Text
        #obr_47.3 - Name Of Coding System
        #obr_47.4 - Alternate Identifier
        #obr_47.5 - Alternate Text
        #obr_47.6 - Name Of Alternate Coding System
        #obr_48 - Medically Necessary Duplicate Procedure Reason.
        #obr_48.1 - Identifier
        #obr_48.2 - Text
        #obr_48.3 - Name Of Coding System
        #obr_48.4 - Alternate Identifier
        #obr_48.5 - Alternate Text
        #obr_48.6 - Name Of Alternate Coding System
        #obr_48.7 - Coding System Version Id
        #obr_48.8 - Alternate Coding System Version Id
        #obr_48.9 - Original Text
        #obr_49 - Result Handling
        #obr_50 - Parent Universal Service Identifier
        #obr_50.1 - Identifier
        #obr_50.2 - Text
        #obr_50.3 - Name Of Coding System
        #obr_50.4 - Alternate Identifier
        #obr_50.5 - Alternate Text
        #obr_50.6 - Name Of Alternate Coding System
        #obr_50.7 - Coding System Version Id
        #obr_50.8 - Alternate Coding System Version Id
        #obr_50.9 - Original Text
 
        OBR = (
        f"OBR|"
        f"{obr1}|{obr2}|{obr3}|{obr4}|{obr5}|{obr6}|{obr7}|{obr8}|{obr9}|{obr10}|"
        f"{obr11}|{obr12}|{obr13}|{obr14}|{obr15}|{obr16}|{obr17}|{obr18}|{obr19}|{obr20}|"
        f"{obr21}|{obr22}|{obr23}|{obr24}|{obr25}|{obr26}|{obr27}|{obr28}|{obr29}|{obr30}|{obr31}|{obr32}"
        )
 
        ## OBX
        # The OBX segment is used to transmit a single observation or observation
        # fragment. It represents the smallest indivisible unit of a report.
 
        # ------- Observation --------
 
        # Creating variables for OBX segments
        OBX_1 = "1"  # Set ID - OBX (Set ID)
        OBX_2 = "NM"  # Value Type --- C
        OBX3_1 = patDiseaseCode
        OBX3_2 = patDisease
        OBX3_3 = "LN"
        OBX_3 = (f"{OBX3_1}^{OBX3_2}^{OBX3_3}")  # Observation Identifier --- R
        OBX_4 = "1"  # Observation Sub-ID --- C
        OBX_5 = "100^1^:^1"  # Observation Value --- C
        OBX_6 = "mL"  # Units
        OBX_7 = "10-100"  # References Range
        OBX_8 = "H"  # Abnormal Flags
        OBX_9 = ""  # Probability
        OBX_10 = ""  # Nature of Abnormal Test
        OBX_11 = random.choice(resultStatus)  # Observation Result Status ---- R
        OBX_12 = ""  # Effective Date of Reference Range
        OBX_13 = ""  # User Defined Access Checks
        OBX_14 = ""  # Date/Time of the Observation
        OBX_15 = ""  # Producer's ID
        OBX_16 = ""  # Responsible Observer
        OBX_17 = ""  # Observation Method
        OBX_18 = ""  # Equipment Instance Identifier
        OBX_19 = hl7_datetime  # Date/Time of the Analysis ----- R
        OBX_20 = ""  # Reserved for harmonization with V2.6
        OBX_21 = ""  # Reserved for harmonization with V2.6
        OBX_22 = ""  # Reserved for harmonization with V2.6
        OBX_23 = ""  # Performing Organization Name
        OBX_24 = ""  # Performing Organization Address
        OBX_25 = ""  # Performing Organization Medical Director
 
        # Concatenate all variables with pipe separator
        OBX_body = "|".join([OBX_1, OBX_2, OBX_3, OBX_4, OBX_5, OBX_6, OBX_7, OBX_8, OBX_9, OBX_10,
                            OBX_11, OBX_12, OBX_13, OBX_14, OBX_15, OBX_16, OBX_17, OBX_18, OBX_19])
       
        OBX = f"OBX|{OBX_body}"
 
        ## SPM -
        # This segment is to describe the characteristics of a specimen and generalizes the multiple relationships among order(s), results, specimen(s) and specimen container(s).
       
        spm1 = "1" #spm_1 - Set ID - SPM
       
        spm_2_1_1 = str(random.randint(1000000, 9999999)) # spm_2.1.1 - Entity Identifier
        spm_2_1_2 = sending_facility_txt # spm_2.1.2 - Namespace Id
        spm_2_1_3 = sending_facility_id # spm_2.1.3 - Universal Id
        spm_2_1_4 = "" # spm_2.1.4 - Universal Id Type
        spm_2_1 = (f"{spm_2_1_1}&{spm_2_1_2}&{spm_2_1_3}&{spm_2_1_4}") #spm_2.1 - Placer Assigned Identifier
       
        spm_2_2_1 = str(random.randint(1000000, 9999999)) # spm_2.2.1 - Entity Identifier
        spm_2_2_2 = assigning_authority_txt # spm_2.2.2 - Namespace Id
        spm_2_2_3 = assigning_authority_id # spm_2.2.3 - Universal Id
        spm_2_2_4 = "CLIA" # spm_2.2.4 - Universal Id Type
        spm_2_2 = (f"{spm_2_2_1}&{spm_2_2_2}&{spm_2_2_3}&{spm_2_2_4}") #spm_2.2 - Filler Assigned Identifier
        spm2 = (f"{spm_2_1}^{spm_2_2}") # spm_2 - Specimen ID
 
        spm3 = "" #spm_3 - Specimen Parent IDs
        #spm_3.1 - Placer Assigned Identifier
        #spm_3.1.1 - Entity Identifier
        #spm_3.1.2 - Namespace Id
        #spm_3.1.3 - Universal Id
        #spm_3.1.4 - Universal Id Type
        #spm_3.2 - Filler Assigned Identifier
        #spm_3.2.1 - Entity Identifier
        #spm_3.2.2 - Namespace Id
        #spm_3.2.3 - Universal Id
        #spm_3.2.4 - Universal Id Type
       
        # spm_4 - Specimen Type
        spm4_1 = specimenCode # spm_4.1 - Identifier
        spm4_2 = specimenTxt # spm_4.2 - Text
        spm4_3 = "HL70487" # spm_4.3 - Name Of Coding System
       
        # if
        #### Logic ####
 
        ####    if code is an alphabet then code_system_cd = HL70487
        ####        else:
        ####            code_system_cd = SCT
        ####
        ####    specimen collection method --> code_short_desc_txt
       
        spm4_4 = AltspecimenCode #spm_4.4 - Alternate Identifier
        spm4_5 = AltspecimenTxt #spm_4.5 - Alternate Text
        spm4_6 = "SCT" #spm_4.6 - Name Of Alternate Coding System
        spm4_7 = "2.5.1" # spm_4.7 - Coding System Version Id
        #spm_4.8 - Alternate Coding System Version Id
        spm4_9 = specimenTxt # spm_4.9 - Original Text
        spm4 = (f"{spm4_1}^{spm4_2}^{spm4_3}^{spm4_4}^{spm4_5}^{spm4_6}^{spm4_7}^{spm4_9}") # spm_4 - Specimen Type
 
        spm5 = "" #spm_5 - Specimen Type Modifier
        #spm_5.1 - Identifier
        #spm_5.2 - Text
        #spm_5.3 - Name Of Coding System
        #spm_5.4 - Alternate Identifier
        #spm_5.5 - Alternate Text
        #spm_5.6 - Name Of Alternate Coding System
        #spm_5.7 - Coding System Version Id
        #spm_5.8 - Alternate Coding System Version Id
        #spm_5.9 - Original Text
       
        spm6 = "" #spm_6 - Specimen Additives
        #spm_6.1 - Identifier
        #spm_6.2 - Text
        #spm_6.3 - Name Of Coding System
        #spm_6.4 - Alternate Identifier
        #spm_6.5 - Alternate Text
        #spm_6.6 - Name Of Alternate Coding System
        #spm_6.7 - Coding System Version Id
        #spm_6.8 - Alternate Coding System Version Id
        #spm_6.9 - Original Text
       
        # spm_7 - Specimen Collection Method
        spm7_1 = AltspecimenCode # spm_7.1 - Identifier
        spm7_2 = AltspecimenCode # spm_7.2 - Text
        spm7_3 = "TG" # spm_7.3 - Name Of Coding System ---- (TG = Test Generator Data)
        # spm_7.4 - Alternate Identifier
        # spm_7.5 - Alternate Text
        # spm_7.6 - Name Of Alternate Coding System
        # spm_7.7 - Coding System Version Id
        # spm_7.8 - Alternate Coding System Version Id
        # spm_7.9 - Original Text
        spm7 = (f"{spm7_1}^{spm7_2}^{spm7_3}") # spm_7 - Specimen Collection Method
       
        #spm8 = "" # spm_8 - Specimen Source Site
        spm8_1 = fake.random_number(digits=9, fix_len=True)
        spm8_2 = fake.word()
        spm8_3  = "SNM"
        # spm_8.4 - Alternate Identifier
        # spm_8.5 - Alternate Text
        # spm_8.6 - Name Of Alternate Coding System
        # spm_8.7 - Coding System Version Id
        # spm_8.8 - Alternate Coding System Version Id
        # spm_8.9 - Original Text
        spm8 = (f"{spm8_1}^{spm8_2}^{spm8_3}")
       
        spm9 = "" # spm_9 - Specimen Source Site Modifier
        # spm_9.1 - Identifier
        # spm_9.2 - Text
        # spm_9.3 - Name Of Coding System
        # spm_9.4 - Alternate Identifier
        # spm_9.5 - Alternate Text
        # spm_9.6 - Name Of Alternate Coding System
        # spm_9.7 - Coding System Version Id
        # spm_9.8 - Alternate Coding System Version Id
        # spm_9.9 - Original Text
       
        spm10 = "" #spm_10 - Specimen Collection Site
        #spm_10.1 - Identifier
        #spm_10.2 - Text
        #spm_10.3 - Name Of Coding System
        #spm_10.4 - Alternate Identifier
        #spm_10.5 - Alternate Text
        #spm_10.6 - Name Of Alternate Coding System
        #spm_10.7 - Coding System Version Id
        #spm_10.8 - Alternate Coding System Version Id
        #spm_10.9 - Original Text
       
        spm11 = "" # spm_11 - Specimen Role
        # spm_11.1 - Identifier
        # spm_11.2 - Text
        # spm_11.3 - Name Of Coding System
        # spm_11.4 - Alternate Identifier
        # spm_11.5 - Alternate Text
        # spm_11.6 - Name Of Alternate Coding System
        # spm_11.7 - Coding System Version Id
        # spm_11.8 - Alternate Coding System Version Id
        # spm_11.9 - Original Text
       
        # spm_12 - Specimen Collection Amount
        spm12_1 = numberrn # spm_12.1 - Quantity
        spm12_2 = "ML"# spm_12.2 - Units
        # spm_12.2.1 - Identifier
        # spm_12.2.2 - Text
        # spm_12.2.3 - Name Of Coding System
        # spm_12.2.4 - Alternate Identifier
        # spm_12.2.5 - Alternate Text
        # spm_12.2.6 - Name Of Alternate Coding System
        spm12 = (f"{spm12_1}^{spm12_2}")
       
        spm13 = "" #spm_13 - Grouped Specimen Count
        spm14 = specimen_details #spm_14 - Specimen Description
 
        spm15 = "" #spm_15 - Specimen Handling Code
        #spm_15.1 - Identifier
        #spm_15.2 - Text
        #spm_15.3 - Name Of Coding System
        #spm_15.4 - Alternate Identifier
        #spm_15.5 - Alternate Text
        #spm_15.6 - Name Of Alternate Coding System
        #spm_15.7 - Coding System Version Id
        #spm_15.8 - Alternate Coding System Version Id
        #spm_15.9 - Original Text
        spm16 = "" #spm_16 - Specimen Risk Code
        #spm_16.1 - Identifier
        #spm_16.2 - Text
        #spm_16.3 - Name Of Coding System
        #spm_16.4 - Alternate Identifier
        #spm_16.5 - Alternate Text
        #spm_16.6 - Name Of Alternate Coding System
        #spm_16.7 - Coding System Version Id
        #spm_16.8 - Alternate Coding System Version Id
        #spm_16.9 - Original Text
       
        # spm_17 - Specimen Collection Date/Time
        spm17_1 = hl7_datetime # spm_17.1 - Range Start Date/Time
        #spm_17.1.1 - Time
        #spm_17.1.2 - Degree Of Precision
        spm17_2 = future_time_hl7_datetime # spm_17.2 - Range End Date/Time
        #spm_17.2.1 - Time
        #spm_17.2.2 - Degree Of Precision
        spm17 = (f"{spm17_1}^{spm17_2}") # spm_17 - Specimen Collection Date/Time
       
        spm18 = hl7_datetime # spm_18 - Specimen Received Date/Time
               
        spm19 = "" #spm_19 - Specimen Expiration Date/Time
        #spm_19.1 - Time
        #spm_19.2 - Degree Of Precision
        spm20 = "" #spm_20 - Specimen Availability
       
        spm21 = "" # spm_21 - Specimen Reject Reason
        # spm_21.1 - Identifier
        # spm_21.2 - Text
        # spm_21.3 - Name Of Coding System
        # spm_21.4 - Alternate Identifier
        # spm_21.5 - Alternate Text
        # spm_21.6 - Name Of Alternate Coding System
        # spm_21.7 - Coding System Version Id
        # spm_21.8 - Alternate Coding System Version Id
        # spm_21.9 - Original Text
       
        #spm_22 - Specimen Quality
        #spm_22.1 - Identifier
        #spm_22.2 - Text
        #spm_22.3 - Name Of Coding System
        #spm_22.4 - Alternate Identifier
        #spm_22.5 - Alternate Text
        #spm_22.6 - Name Of Alternate Coding System
        #spm_22.7 - Coding System Version Id
        #spm_22.8 - Alternate Coding System Version Id
        #spm_22.9 - Original Text
        #spm_23 - Specimen Appropriateness
        #spm_23.1 - Identifier
        #spm_23.2 - Text
        #spm_23.3 - Name Of Coding System
        #spm_23.4 - Alternate Identifier
        #spm_23.5 - Alternate Text
        #spm_23.6 - Name Of Alternate Coding System
        #spm_23.7 - Coding System Version Id
        #spm_23.8 - Alternate Coding System Version Id
        #spm_23.9 - Original Text
        #spm_24 - Specimen Condition
        #spm_24.1 - Identifier
        #spm_24.2 - Text
        #spm_24.3 - Name Of Coding System
        #spm_24.4 - Alternate Identifier
        #spm_24.5 - Alternate Text
        #spm_24.6 - Name Of Alternate Coding System
        #spm_24.7 - Coding System Version Id
        #spm_24.8 - Alternate Coding System Version Id
        #spm_24.9 - Original Text
        #spm_25 - Specimen Current Quantity
        #spm_25.1 - Quantity
        #spm_25.2 - Units
        #spm_25.2.1 - Identifier
        #spm_25.2.2 - Text
        #spm_25.2.3 - Name Of Coding System
        #spm_25.2.4 - Alternate Identifier
        #spm_25.2.5 - Alternate Text
        #spm_25.2.6 - Name Of Alternate Coding System
        #spm_26 - Number of Specimen Containers
        #spm_27 - Container Type
        #spm_27.1 - Identifier
        #spm_27.2 - Text
        #spm_27.3 - Name Of Coding System
        #spm_27.4 - Alternate Identifier
        #spm_27.5 - Alternate Text
        #spm_27.6 - Name Of Alternate Coding System
        #spm_27.7 - Coding System Version Id
        #spm_27.8 - Alternate Coding System Version Id
        #spm_27.9 - Original Text
        #spm_28 - Container Condition
        #spm_28.1 - Identifier
        #spm_28.2 - Text
        #spm_28.3 - Name Of Coding System
        #spm_28.4 - Alternate Identifier
        #spm_28.5 - Alternate Text
        #spm_28.6 - Name Of Alternate Coding System
        #spm_28.7 - Coding System Version Id
        #spm_28.8 - Alternate Coding System Version Id
        #spm_28.9 - Original Text
        #spm_29 - Specimen Child Role
        #spm_29.1 - Identifier
        #spm_29.2 - Text
        #spm_29.3 - Name Of Coding System
        #spm_29.4 - Alternate Identifier
        #spm_29.5 - Alternate Text
        #spm_29.6 - Name Of Alternate Coding System
        #spm_29.7 - Coding System Version Id
        #spm_29.8 - Alternate Coding System Version Id
        #spm_29.9 - Original Text
 
        # Concatenate all variables with pipe separator
        SPM_body = "|".join([spm1, spm2, spm3, spm4, spm5, spm6, spm7, spm8, spm9, spm10,
                            spm11, spm12, spm13, spm14, spm15, spm16, spm17, spm18, spm19, spm20, spm21])
       
        SPM = f"SPM|{SPM_body}"
 
       
 
        # All segments are arranged here
        HL7 = (f"{MSH}"
            f"\n{PID}"
            f"\n{PV1}"
            f"\n{ORC}"
            f"\n{OBR}"
            f"\n{OBX}"
            f"\n{SPM}")
       
        
        ######################################################################
        #### This code is to Create a separate text file for each message ####
        ######################################################################
 
        file_name = os.path.join(output_folder, f"{firstname}_{lastname}_{patDiseaseCode}_{curr_date}.txt")
        with open(file_name, 'w') as text_file:
            text_file.write(HL7)
        #file_name = os.path.join(output_folder, f"{firstname}_{lastname}_{patDiseaseCode}_{curr_date}.json")
        #with open(file_name, 'w') as json_file:
            #json_file.write(HL7)
  
 
    End_time = datetime.now()
    print("Code Gen Endtime", End_time)
 
#print("Before Clear Cache:", queries.cache_info())
queries.cache_clear()
#print("After Clear Cache:", queries.cache_info())
home_dir = os.path.expanduser("~")
generateELR(numoELRs, conditionCode, loincCode, home_dir+"/Desktop/IH")