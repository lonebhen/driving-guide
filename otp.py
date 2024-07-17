import requests
import json
import os
from logging import log
from utils import phone_number_format
from dotenv import load_dotenv

load_dotenv()

client = requests.Session()


api_key = os.getenv('ARKESEL_OTP_KEY')

headers = {
    "api-key": api_key
}

request_otp_url = "https://sms.arkesel.com/api/otp/generate"
validate_otp_url = "https://sms.arkesel.com/api/otp/verify"

    
    
def generate_otp(msisdn):
    print(api_key)
    formatted_number = phone_number_format(msisdn)

    if not formatted_number:
        return {"error": "Invalid phone number"}, 400

    request_body = {
        "expiry": "5",
        "length": "6",
        "medium": "sms",
        "message": "This is OTP from Driving Guide, %otp_code%",
        "number": str(formatted_number),
        "sender_id": "Driving",
        "type": "numeric"
    }

    try:
        response = client.post(request_otp_url, headers=headers, json=request_body)
        print(response)
        response.raise_for_status()
        return response.json(), 200
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500



def validate_otp(code, msisdn):
    formatted_number = phone_number_format(msisdn)

    if not formatted_number:
        return {"error": "Invalid phone number"}, 400
    
    request_body = {
        "code": code,
        "number": formatted_number
    }
    
    
    
    try:
        response = requests.post(validate_otp_url, headers=headers, json=request_body)
        response.raise_for_status()
        print(response.text)
        return response.json(), 200
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return {"error": "Failed to validate OTP"}, 500