import requests
import json
import os
from logging import log
from utils import phone_number_format

client = requests.Session()


api_key = os.getenv('ARKESEL_OTP_KEY')

headers = {
    "api-key": api_key,
    "Content-Type": "application/json"
}

url = "https://sms.arkesel.com/api/otp/generate"

    
    
def generate_otp(msisdn):
    print(api_key)
    formatted_number = phone_number_format(msisdn)

    if not formatted_number:
        return {"error": "Invalid phone number"}, 400

    request_body = {
        "expiry": "5",
        "length": "4",
        "medium": "sms",
        "message": "This is OTP from Driving Guide, %otp_code%",
        "number": formatted_number,
        "sender_id": "Driving Guide",
        "type": "numeric"
    }

    try:
        response = client.post(url, headers=headers, json=request_body)
        response.raise_for_status()
        return response.json(), 200
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500
