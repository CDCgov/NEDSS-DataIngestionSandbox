import datetime
import random
import uuid
from faker import Faker

fake = Faker()

def generate_effective_time():
    random_datetime = fake.date_time(tzinfo=None)
    return random_datetime.strftime('%Y%m%d%H%M%S+0000')


def generate_hospital_name():
    return fake.company() + random.choice([" Hospital", " Lab"])


def generate_unique_root():
    return f"1.22.333.4444.5555.{random.randint(1000, 9999)}"


def generate_patient_id():
    return f"PT-{random.randint(10000000, 99999999)}"


def generate_title():
    return random.choice(["Ms", "Mr", "Mrs", "Dr"])


def generate_gender():
    gender_code = random.choice(["M", "F"])
    gender = "Male" if gender_code == "M" else "Female"
    return gender_code, gender


def generate_birthtime():
    return fake.date_of_birth(minimum_age=0, maximum_age=120).strftime("%Y%m%d")


def generate_phone_number():
    area_code = random.randint(200, 999)
    prefix = random.randint(200, 999)
    line_number = random.randint(1000, 9999)
    return f"+1({area_code}){prefix}-{line_number}"


def generate_race_and_ethnicity():
    races = [{"code": "2076-8", "displayName": "Native Hawaiian or Other Pacific Islander"},
        {"code": "2028-9", "displayName": "Asian"}, {"code": "2054-5", "displayName": "Black or African American"},
        {"code": "2106-3", "displayName": "White"}, ]
    ethnicities = [{"code": "2135-2", "displayName": "Hispanic or Latino"},
        {"code": "2076-8", "displayName": "Native Hawaiian/Pacific Islander"},
        {"code": "2106-3", "displayName": "White"}, {"code": "2186-5", "displayName": "Not Hispanic or Latino"}, ]
    race = random.choice(races)
    ethnicity = random.choice(ethnicities)
    return race, ethnicity


def generate_extension_id():
    return f"{random.randint(10000000, 99999999)}"


def generate_uuid():
    return f"{str(uuid.uuid4())}"


def generate_social_history(gender_code, gender):
    observation = "Birth Sex"
    observation_result = gender_code
    uuid_value = str(uuid.uuid4())
    table_html = f"""
        <text>
            <table border="1" width="100%">
                <thead>
                    <tr>
                        <th>Social History Observation</th>
                        <th>Social History Observation Result</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <content ID="socContent0">{observation}</content>
                        </td>
                        <td>
                            <content ID="socObservationResult0">{observation_result}</content>
                        </td>
                    </tr>
                </tbody>
            </table>
        </text>
        """
    entry_xml = f"""
        <entry>
            <observation classCode="OBS" moodCode="EVN">
                <templateId extension="2016-06-01"
                    root="2.16.840.1.113883.10.20.22.4.200" />
                <id root="{uuid_value}" />
                <code code="76689-9" codeSystem="2.16.840.1.113883.6.1"
                    codeSystemName="LOINC" displayName="{observation}" />
                <statusCode code="completed" />
                <value code="{observation_result}" codeSystem="2.16.840.1.113883.5.1"
                    codeSystemName="Administrative Gender" displayName="{gender}"
                    xsi:type="CD" />
            </observation>
        </entry>
        """
    return table_html + entry_xml


def generate_html_table(data, headers):
    html_table = """
    <table border="1" width="100%">
        <thead>
            <tr>
    """
    for header in headers:
        html_table += f"<th>{header}</th>"
    html_table += """
            </tr>
        </thead>
        <tbody>
    """
    for row in data:
        html_table += "<tr>"
        for value in row.values():
            html_table += f"<td>{value}</td>"
        html_table += "</tr>"
    html_table += """
        </tbody>
    </table>
    """
    return html_table


def generate_reason_for_visit_data(num_rows):
    reasons = ["Routine Checkup", "Flu Symptoms", "Back Pain", "Headache", "Allergy Testing", "Diabetes Management",
        "Cardiac Screening", "Skin Rash", "Fever", "Post-Surgery Follow-up", "Vaccination", "Physical Examination"]
    data = []
    if (num_rows == 0):
        return f"No Reason for Visit information available"
    for _ in range(num_rows):
        data.append({"reason": random.choice(reasons)})
    return generate_html_table(data, ["Reason"])


def generate_history_of_present_illness_data(num_rows):
    reasons = ["Chest Pain", "Shortness of Breath", "Cough (Productive/Non-productive)", "Fever and Chills",
        "Abdominal Pain", "Headache", "Dizziness or Lightheadedness", "Fatigue or Weakness", "Nausea and Vomiting",
        "Diarrhea or Constipation", "Muscle or Joint Pain", "Skin Rash or Lesion", "Unexplained Weight Loss",
        "Palpitations", "Sore Throat", "Urinary Frequency or Burning", "Vision Changes or Eye Pain",
        "Hearing Loss or Ear Pain", "Anxiety or Depression", "Memory Loss or Cognitive Decline",
        "Insomnia or Sleep Disturbances", "Back Pain", "Leg Swelling", "Numbness or Tingling", "Bleeding or Bruising",
        "Allergic Reaction", "Post-surgical Pain", "Follow-up for Chronic Illness", "Loss of Appetite",
        "Difficulty Swallowing (Dysphagia)"]
    data = []
    if (num_rows == 0):
        return f"No History of Present Illness information available"
    for _ in range(num_rows):
        data.append({"reason": random.choice(reasons)})
    return generate_html_table(data, ["Narrative Text"])


def generate_treatment_entries(treatment_code_data, num_rows):
    selected_treatments = random.sample(treatment_code_data, num_rows)
    treatments = []
    entries = []

    for test in selected_treatments:
        treatment_entry = f"""
            <entry typeCode="DRIV">
                <observation classCode="OBS" moodCode="RQO">
                    <templateId root="2.16.840.1.113883.10.20.22.4.44"/>
                    <templateId extension="2014-06-09" root="2.16.840.1.113883.10.20.22.4.44"/>
                    <id root="{uuid.uuid4()}"/>
                    <code code="{test['code']}" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="{test['treatment_name']}"/>
                    <statusCode code="active"/>
                    <effectiveTime value="{generate_effective_time()}"/>
                </observation>
            </entry>
                    """
        treatments.append(
            {"Name": test["treatment_name"], "Type": "Lab", "Priority": random.choice(["STAT", "Routine"]),
             "Associated Diagnoses": "", "Date/Time": fake.date_time()})
        entries.append(treatment_entry)
    return treatments, entries


def generate_plan_of_treatment_data(num_rows):
    treatment_code_data = [{"code": "101653-4", "treatment_name": "Prenatal hepatitis B and C panel"},
        {"code": "16129-9", "treatment_name": "Hepatitis C virus Ab.IgG"},
        {"code": "16936-7", "treatment_name": "Hepatitis C virus Ab.IgG"},
        {"code": "24363-4", "treatment_name": "Acute hepatitis 2000 panel"},
        {"code": "33462-3", "treatment_name": "Hepatitis C virus Ab.IgG"},
        {"code": "40726-2", "treatment_name": "Hepatitis C virus Ab.IgG"},
        {"code": "45690-5", "treatment_name": "Viral hepatitis"},
        {"code": "55264-6", "treatment_name": "Hepatitis A virus immunization status"},
        {"code": "57006-9", "treatment_name": "Hepatitis C virus Ab.IgG"},
        {"code": "61156-6", "treatment_name": "Hepatitis B virus codon V173L"},
        {"code": "61159-0", "treatment_name": "Hepatitis B virus codon M204S"},
        {"code": "72840-2", "treatment_name": "Hepatitis B virus codon 250"},
        {"code": "82381-5", "treatment_name": "Hepatitis C virus genotype 1 NS5b gene mutations detected"},
        {"code": "89359-4", "treatment_name": "Hepatitis C virus Ab.IgG"},
        {"code": "92889-5", "treatment_name": "Chronic hepatitis differentiation between B and C virus panel"},
        {"code": "105066-5", "treatment_name": "SARS coronavirus+SARS coronavirus 2 Ag"},
        {"code": "41460-7", "treatment_name": "SARS coronavirus Ab.IgG"},
        {"code": "41991-1", "treatment_name": "SARS coronavirus Ab.IgM"},
        {"code": "42956-3", "treatment_name": "SARS coronavirus Ab.IgM"},
        {"code": "42957-1", "treatment_name": "SARS coronavirus Ab.IgG"},
        {"code": "94562-6", "treatment_name": "SARS coronavirus 2 Ab.IgA"},
        {"code": "94720-0", "treatment_name": "SARS coronavirus 2 Ab.IgA"},
        {"code": "94768-9", "treatment_name": "SARS coronavirus 2 Ab.IgA"},
        {"code": "95209-3", "treatment_name": "SARS coronavirus+SARS coronavirus 2 Ag"},
        {"code": "95427-1", "treatment_name": "SARS coronavirus 2 Ab.IgA"}]

    if (num_rows == 0):
        return f"No Plan of Treatment information available"

    treatments, entries = generate_treatment_entries(treatment_code_data, num_rows)
    html_data = generate_html_table(treatments, ["Name", "Type", "Priority", "Associated Diagnoses", "Date/Time"])
    return "<text>" + html_data + "</text>" + "".join(entries)


def generate_immunizations_data(num_rows):
    vaccines = ["DTaP, 5 pertussis antigens vaccine (DAPTACEL)", "Hep B, adult vaccine (Engerix/Recombivax)",
        "SARS-COV-2 (COVID-19) RED CAP +BLUE LABEL VACCINE, MODERNA 12+YO", "Polio Vaccine (IPV)",
        "MMR (Measles, Mumps, Rubella) Vaccine", "Varicella (Chickenpox) Vaccine", "Pneumococcal Vaccine (PCV13)",
        "Flu Vaccine", "HPV Vaccine (Gardasil)", "Tetanus, Diphtheria, Pertussis (Tdap) Vaccine", "Hepatitis A Vaccine",
        "Meningococcal Vaccine"]
    if (num_rows == 0):
        return f"No Immunizations information available"
    immunizations = []
    for _ in range(num_rows):
        admin_date = fake.date_this_year().strftime("%m/%d/%Y")
        next_due_date = datetime.datetime.today() + datetime.timedelta(days=random.randint(365, 1095))
        next_due = next_due_date.strftime("%m/%d/%Y")
        immunization = {"name": random.choice(vaccines), "administration dates": admin_date, "next due": next_due, }
        immunizations.append(immunization)
    return generate_html_table(immunizations, ["Name", "Administration Dates", "Next Due"])


def generate_results_entries(lonic_code_data, num_rows):
    selected_tests = random.sample(lonic_code_data, num_rows)
    results = []
    entries = []

    for test in selected_tests:
        result_entry = f"""
<entry typeCode="DRIV">
    <organizer classCode="BATTERY" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.22.4.1"/>
        <templateId extension="2015-08-01" root="2.16.840.1.113883.10.20.22.4.1"/>
        <id root="{uuid.uuid4()}"/>
        <code code="{test['code']}" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="{test['test_name']}"/>
        <statusCode code="completed"/>
        <effectiveTime>
            <low value="{generate_effective_time()}"/>
            <high value="{generate_effective_time()}"/>
        </effectiveTime>
        <component>
            <observation classCode="OBS" moodCode="EVN">
                <templateId root="2.16.840.1.113883.10.20.22.4.2"/>
                <templateId extension="2015-08-01" root="2.16.840.1.113883.10.20.22.4.2"/>
                <templateId extension="2016-12-01" root="2.16.840.1.113883.10.20.15.2.3.2"/>
                <id root="{uuid.uuid4()}"/>
                <code code="{test['code']}" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="{test['test_name']}" sdtc:valueSet="2.16.840.1.114222.4.11.7508" sdtc:valueSetVersion="20200429" xsi:type="CD"/>
                <statusCode code="completed"/>
                <effectiveTime value="{generate_effective_time()}"/>
                <value code="260373001" codeSystem="2.16.840.1.113883.6.96" codeSystemName="SNOMED-CT" displayName="Detected (qualifier value)" xsi:type="CD"/>
            </observation>
        </component>
    </organizer>
</entry>
"""
        results.append(
            {"Lab Test Name": test["test_name"], "Lab Test Result Value": random.choice(["Yes", "No", "UNK"]),
             "Lab Test Result Date": generate_effective_time()})
        entries.append(result_entry)
    return results, entries


def generate_results_data(num_rows):
    lonic_code_data = [{"code": "102048-6", "test_name": "SARS coronavirus 2 and Respiratory syncytial virus Ag"},
        {"code": "105066-5", "test_name": "SARS coronavirus+SARS coronavirus 2 Ag"},
        {"code": "41459-9", "test_name": "SARS coronavirus"}, {"code": "94763-0", "test_name": "SARS coronavirus 2"},
        {"code": "95209-3", "test_name": "SARS coronavirus+SARS coronavirus 2 Ag"},
        {"code": "15868-3", "test_name": "Mussel Ab.IgE.RAST class"}, {"code": "6184-6", "test_name": "Mussel Ab.IgE"},
        {"code": "104651-5",
         "test_name": "Herpes simplex virus 1 and 2 and Varicella zoster virus and Treponema pallidum DNA panel"},
        {"code": "51874-6", "test_name": "Varicella zoster virus immune globulin ordered"},
        {"code": "57322-0", "test_name": "Varicella zoster virus Ab.IgM^1st specimen"},
        {"code": "62454-4", "test_name": "Herpes simplex virus and Varicella zoster virus identified"},
        {"code": "101203-8", "test_name": "Herpes simplex virus 1+2 Ab.IgG index"},
        {"code": "51666-6", "test_name": "Japanese encephalitis virus RNA"},
        {"code": "7936-8", "test_name": "Japanese encephalitis virus RNA"},
        {"code": "24363-4", "test_name": "Acute hepatitis 2000 panel"}, ]

    if (num_rows == 0):
        return f"No Lab Test Results information available"

    results, entries = generate_results_entries(lonic_code_data, num_rows)
    html_data = generate_html_table(results, ["Lab Test Name", "Lab Test Result Value", "Lab Test Result Date"])
    return "<text>" + html_data + "</text>" + "".join(entries)


def generate_encounters_data(num_rows):
    reasons = ["Emergency Room Visit", "Routine Checkup", "Follow-up", "Surgical Procedure", "Diagnostic Imaging",
        "Lab Testing", "Vaccination Appointment", "Specialist Consultation"]
    encounters = []
    encounter_reason = random.choice(reasons)
    encounter_date = generate_effective_time()
    entry = f"""
    <entry typeCode="DRIV">
                        <encounter classCode="ENC" moodCode="EVN">
                            <templateId root="2.16.840.1.113883.10.20.22.4.49"/>
                            <templateId extension="2015-08-01" root="2.16.840.1.113883.10.20.22.4.49"/>
                            <id root="{uuid.uuid4()}"/>
                            <code code="99213" codeSystem="2.16.840.1.113883.6.12" codeSystemName="CPT-4" displayName="{encounter_reason}"/>
                            <effectiveTime value="{encounter_date}"/>
                        </encounter>
                    </entry>
                    """
    for _ in range(num_rows):
        encounters.append({"encounter_reason": encounter_reason, "encounter_date": encounter_date})
    html_data = generate_html_table(encounters, ["Encounter Reason", "Encounter Date"])
    return "<text>" + html_data + "</text>" + entry


def generate_problems_data():
    return f"No problems reported as of {fake.date_time()}"


def generate_medicine_entries_results(medicines, num_rows):
    selected_meds = random.sample(medicines, num_rows)
    results = []
    entries = []

    for med in selected_meds:
        result_entry = f"""
<entry typeCode="DRIV">
    <substanceAdministration classCode="SBADM" moodCode="INT">
        <templateId root="2.16.840.1.113883.10.20.22.4.16"/>
        <templateId extension="2014-06-09" root="2.16.840.1.113883.10.20.22.4.16"/>
        <id root="{uuid.uuid4()}"/>
        <statusCode code="active"/>
        <effectiveTime value="{generate_effective_time()}"/>
        <effectiveTime institutionSpecified="true" operator="A" xsi:type="PIVL_TS">
            <period unit="h" value="0"/>
        </effectiveTime>
        <doseQuantity unit="Tabs" value="1.0"/>
        <consumable>
            <manufacturedProduct classCode="MANU">
                <templateId root="2.16.840.1.113883.10.20.22.4.23"/>
                <templateId extension="2014-06-09" root="2.16.840.1.113883.10.20.22.4.23"/>
                <id root="{uuid.uuid4()}"/>
                <manufacturedMaterial>
                    <code code="{med['code']}" codeSystem="2.16.840.1.113883.6.88"
                          codeSystemName="rxnorm" displayName="{med['name']}"/>
                </manufacturedMaterial>
            </manufacturedProduct>
        </consumable>
    </substanceAdministration>
</entry>
"""
        results.append({"Medication Name": med["name"], "Medication Administered Time": generate_effective_time()})
        entries.append(result_entry)
    return results, entries


def generate_medications_administered_data(num_rows):
    medicines = [{"code": "161", "name": "Acetaminophen"}, {"code": "281", "name": "Acyclovir"},
        {"code": "15202", "name": "Argatroban"}, {"code": "1399", "name": "Benzocaine"},
        {"code": "1808", "name": "Bumetanide"}, {"code": "2187", "name": "Cefotetan (Cefotan)"},
        {"code": "59038", "name": "Chitosan"}, {"code": "3322", "name": "Diazepam"},
        {"code": "3498", "name": "Diphenhydramine / Benadryl"}, {"code": "328316", "name": "Epi 1:10,000"},
        {"code": "4441", "name": "Flecainide (Tambocor)"}, {"code": "152926", "name": "Gelofusine"},
        {"code": "5224", "name": "Heparin"}, {"code": "3423", "name": "Hydromorphone/Dilaudid"},
        {"code": "5640", "name": "Ibuprofen (Motrin)"}, {"code": "6130", "name": "Ketamine"},
        {"code": "237159", "name": "Levalbuterol"}, {"code": "6915", "name": "Metaclopramide / Reglan"},
        {"code": "61381", "name": "Olanzapine"}, {"code": "8183", "name": "Phenytoin"},
        {"code": "34345", "name": "Pralidoxime / 2-Pam"}, {"code": "8700", "name": "Procainamide"},
        {"code": "227778", "name": "Proparacaine"}, {"code": "9068", "name": "Quinidine"},
        {"code": "9143", "name": "Ranitidine (Zantac)"}, {"code": "763140", "name": "Reteplase (Retavase)"},
        {"code": "10154", "name": "Succinylcholine"}, {"code": "876421", "name": "Torsemide"},
        {"code": "71535", "name": "Vecuronium"}, {"code": "115698", "name": "Ziprasidone"}]
    if (num_rows == 0):
        return f"No Medications Administered or information not available"

    results, entries = generate_medicine_entries_results(medicines, num_rows)
    html_data = generate_html_table(results, ["Medication Name", "Medication Administered Time"])
    return "<text>" + html_data + "</text>" + "".join(entries)


# Main function to generate the full eICR
def generate_eicr(template):
    gender_code, gender = generate_gender()
    race, ethnicity = generate_race_and_ethnicity()
    first_name = fake.first_name()
    last_name = fake.last_name()
    author_name = generate_hospital_name()
    author_first_name = fake.first_name()
    author_last_name = fake.last_name()
    # social_history_data = generate_social_history(gender_code,gender)
    # reason_for_visit_data = generate_reason_for_visit_data(random.randint(0,1))
    # history_of_present_illness_data = generate_history_of_present_illness_data(random.randint(0,5))
    # plan_of_treatment_data = generate_plan_of_treatment_data(random.randint(0,5))
    # immunizations_data = generate_immunizations_data(random.randint(0,5))
    # results_data = generate_results_data(random.randint(0,5))
    # encounters_data = generate_encounters_data(1)
    # problems_data = generate_problems_data()
    # medications_administered_data = generate_medications_administered_data(random.randint(0,5))

    return first_name, last_name, template.format(id_extension=generate_extension_id(), uuid=generate_uuid(),
        setid_extension_uuid=generate_uuid(), setid_root=generate_unique_root(), patient_id=generate_patient_id(),
        patient_root=generate_unique_root(), ssn=fake.ssn(), title=generate_title(), first_name=first_name,
        last_name=last_name, birth_time=generate_birthtime(), gender_code=gender_code, gender=gender,
        street_address=fake.street_address(), city=fake.city(), state=fake.state_abbr(), zip=fake.zipcode(),
        country="USA", phone_number=generate_phone_number(), email=first_name + "." + last_name + "@example.com",
        race_code=race['code'], race_display_name=race['displayName'], ethnicity_code=ethnicity['code'],
        ethnicity_display_name=ethnicity['displayName'], visit_date=generate_effective_time(),
        assigned_author_id=generate_unique_root(), author_name=author_name, author_id=generate_uuid(),
        author_first_name=author_first_name, author_last_name=author_last_name,
        author_street_address=fake.street_address(), author_city=fake.city(), author_state=fake.state_abbr(),
        author_zip=fake.zipcode(), author_country="USA", author_phone_number=generate_phone_number(),
        author_email=author_first_name + "." + author_last_name + "@example.com",
        effective_time=generate_effective_time(), location_uuid=generate_uuid(), location_code=generate_extension_id(),
        encounter_uuid=generate_uuid(), encounter_extension=generate_extension_id(),
        social_history_data=generate_social_history(gender_code, gender),
        reason_for_visit_data=generate_reason_for_visit_data(random.randint(0, 1)),
        history_of_present_illness_data=generate_history_of_present_illness_data(random.randint(0, 5)),
        plan_of_treatment_data=generate_plan_of_treatment_data(random.randint(0, 5)),
        immunizations_data=generate_immunizations_data(random.randint(0, 5)),
        results_data=generate_results_data(random.randint(0, 5)), encounters_data=generate_encounters_data(1),
        problems_data=generate_problems_data(),
        medications_administered_data=generate_medications_administered_data(random.randint(0, 5)))


if __name__ == "__main__":
    template_file = "/Users/RagulShanmugam/Desktop/eICR-CCDA-template.xml"

    with open(template_file, 'r') as file_template:
        template = file_template.read()

    first_name, last_name, eicr_data = generate_eicr(template.strip())

    with open(first_name + "_" + last_name + "_CDA_eICR.xml", "w", newline="") as f:
        f.write(eicr_data)

    print("eICR generated and saved to: " + first_name + "_" + last_name + "_CDA_eICR.xml")
