import os
from botocore.exceptions import ClientError
from faker import Faker
import json
import boto3
from datetime import datetime, timedelta, date
import requests
import aiohttp
import asyncio
import zipfile
import io
from hl7_generator_v1_43_03182024 import *


numELRs=0 #default number of messages
conditionCode=10020 #default condition code


instance = HL7Generator()
instance.set_condition_code(conditionCode)
instance.queries()  ## Call queries method to populate dataframes



store_in_s3="false" #if 'true', the generated files will be stored in S3 bucket.
call_di_service="false" #if 'true', di service will be called to ingest the hl7 message.

di_api_url=""
auth_client_id=""
auth_client_secret=""
auth_token=""

### For local testing uncomment the following lines. DI api endpoint and auth details are hard coded.
# di_api_url = "https://dataingestion.dts1.nbspreview.com/api/reports"
# auth_client_id='di-keycloak-client'
# auth_client_secret='fcidpwabdQzUrPqEWkSzuGNX6EV4BJ7H1123432'
# auth_token=""

auth_headers ={}    

################
# S3 bucket 
s3_client=None
s3bucket_name="" 

async def generate_unique_patient_messages(numELRs, conditionCode):

    print ("call_di_service flag:",call_di_service)
    print ("store_in_s3 flag:",store_in_s3)

    ##########################################################
    # Create a zip file in-memory and store it in S3 bukcet. #
    ##########################################################
    if store_in_s3=='true':
        global s3bucket_name
        s3bucket_name = "hl7-generator"
        global s3_client
        s3_client = boto3.client('s3')
        zip_buffer = io.BytesIO()
        zipf=zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED)
    
    global auth_headers
    auth_headers = {'msgType':'HL7','accept':'*/*','Content-Type':'text/plain','clientId':auth_client_id,
               'clientSecret':auth_client_secret,'Authorization': f'Bearer {auth_token}'} 
    
    async with aiohttp.ClientSession() as session:

        for i in range(int(numELRs)):
            hl7_text_message = instance.generateELR(numELRs, conditionCode)
            #print(hl7_text_message)
            
            ####################################################
            # Ingest the HL7 message by calling the DI service #
            ####################################################
            if call_di_service=='true':
                coro = ingest_hl7_into_diservice(session,hl7_text_message)
                await coro
            
            ####################################################################################
            # Put the HL7 messages as text files in a zip file, and store it in the S3 bucket. #
            ####################################################################################
            if store_in_s3=='true':
                date_time_now=datetime.now().strftime("%Y%m%d%f")
                filename=date_time_now+".txt"
                zipf.writestr(filename, hl7_text_message)

                
        #################################################
        # Upload the created zip file to the S3 bucket. #
        #################################################
        if store_in_s3=='true':
            zipf.close()
            zip_buffer.seek(0)
            try:
                zip_file_name='hl7testfiles_'+datetime.now().strftime("%Y%m%d%H%M%S")+".zip"
                s3_client.upload_fileobj(zip_buffer, s3bucket_name, zip_file_name)
            except ClientError as cex:
                print(f'Error uploading to s3: {cex} ')
                raise cex

async def ingest_hl7_into_diservice(session,hl7message):
    async with session.post(di_api_url, data=hl7message, headers=auth_headers,ssl=False,raise_for_status=custom_error_handler) as response:
        text = await response.text()
        print(f'Response from di service status: {response.status} ID: {text} ')

async def custom_error_handler(response):
    if response.status >=400:
        text = await response.text()
        raise RuntimeError(text)

def reset_inputparams():
    global numELRs
    numELRs=0
    global store_in_s3
    store_in_s3="" 
    global call_di_service
    call_di_service="" 
    global di_api_url
    di_api_url=""
    global auth_client_id
    auth_client_id=""
    global auth_client_secret
    auth_client_secret=""
    global auth_token
    auth_token=""

###################################################
# AWS Lambda invokes the function lambda_handler. #
###################################################
def lambda_handler(event, context):
    
    #reset the input values on each request.
    reset_inputparams()

    if "queryStringParameters" in event:
        print(event["queryStringParameters"])
        queryParams=event["queryStringParameters"]

        global numELRs
        if "numELRs" in queryParams:
            numELRs=int(queryParams["numELRs"])

        if "store_in_s3" in queryParams:
            global store_in_s3
            store_in_s3=queryParams["store_in_s3"]

        if "call_di_service" in queryParams and queryParams["call_di_service"]=='true':
            global call_di_service
            call_di_service=queryParams["call_di_service"]
            print('input param call_di_service: ',call_di_service)
            global di_api_url
            di_api_url=queryParams["di_api_url"]
            global auth_client_id
            auth_client_id=queryParams["auth_client_id"]
            global auth_client_secret
            auth_client_secret=queryParams["auth_client_secret"]
            global auth_token
            auth_token=queryParams["auth_token"]
    ## For Async call.        
    loop = asyncio.get_event_loop()    
    result = loop.run_until_complete(generate_unique_patient_messages(numELRs,""))
    return {
        'statusCode': 200,
        'body': json.dumps('Process complete!')
    }

# Uncomment the following lines for the local development.
# if __name__ == "__main__":
#     asyncio.run(generate_unique_patient_messages(50, 10030))