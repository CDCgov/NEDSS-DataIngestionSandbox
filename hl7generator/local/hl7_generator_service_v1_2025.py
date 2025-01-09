import os
import zipfile
from datetime import datetime
from hl7_generator_v1 import *


numELRs=10 #default number of messages
conditionCode=10020 #default condition code


instance = HL7Generator()
instance.set_condition_code(conditionCode)
instance.queries()  ## Call queries method to populate dataframes

def generate_and_store_messages(numELRs, conditionCode, save_as_zip=False):
    """
    Generate HL7 messages and store them locally.

    :param numELRs: Number of HL7 messages to generate
    :param conditionCode: Condition code for HL7 messages
    :param save_as_zip: Boolean indicating whether to save all messages in a zip file
    """
    local_folder = "generated_hl7_messages"
    os.makedirs(local_folder, exist_ok=True)  # Ensure the folder exists

    if save_as_zip:
        zip_file_path = os.path.join(local_folder, "hl7_messages.zip")
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i in range(numELRs):
                hl7_text_message = instance.generateELR(numELRs, conditionCode)
                filename = f"hl7_message_{i+1}.txt"
                zipf.writestr(filename, hl7_text_message)
            print(f"All HL7 messages saved in zip file: {zip_file_path}")
    else:
        for i in range(numELRs):
            hl7_text_message = instance.generateELR(numELRs, conditionCode)
            filename = f"hl7_message_{i+1}.txt"
            file_path = os.path.join(local_folder, filename)
            with open(file_path, "w") as file:
                file.write(hl7_text_message)
            print(f"HL7 message saved to: {file_path}")


if __name__ == "__main__":
    # Set `save_as_zip` to True if you want all files in a zip archive
    generate_and_store_messages(numELRs, conditionCode, save_as_zip=False)