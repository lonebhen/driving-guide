import random
import requests
import json
import os
from logging import log
from utils import phone_number_format
from dotenv import load_dotenv

load_dotenv()

client = requests.Session()

api_key = os.getenv('ARKESEL_OTP_KEY')


    
    
def generate_otp():
    return random.randint(100000, 999999)

def send_otp(phone_number, otp):
    
    msisdn = phone_number_format(phone_number)
    
    key = api_key
    sender_id = "Driving"
    message = f"Your OTP for Driving Guide is {otp}. It expires in 5 minutes"
    url = f"https://sms.arkesel.com/sms/api?action=send-sms&api_key={key}&to={msisdn}&from={sender_id}&sms={message}"
    
    response = requests.get(url)
    return response.status_code == 200
