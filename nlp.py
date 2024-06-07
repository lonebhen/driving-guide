import os
from dotenv import load_dotenv
import requests

from model.models import NLPAPICache, db


load_dotenv()


api_key = os.getenv('NLP_API_KEY')


def translate_traffic_sign_predict_to_local_dialect(traffic_sign):
    print(traffic_sign)
    cached_data = NLPAPICache.query.filter_by(api_key = traffic_sign).first()
    
    if cached_data:
        print("Returning cache from db")
        
        return cached_data.value
    
    url = 'https://translation-api.ghananlp.org/v1/translate'
    
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-SUbscription-Key': api_key
    }
    
    data = {
        "in": traffic_sign,
        "lang": "en-tw"
    }
    
    response = requests.post(url, headers=headers, json=data)
    print(response)
    
    if response.status_code == 200:
        try:
            json_response = response.json()
            if isinstance(json_response, str):
                translated_data = json_response
            else:
                translated_data = json_response.get('data')
            
            if translated_data:
                new_cache_entry = NLPAPICache(api_key=traffic_sign, value=translated_data)
                db.session.add(new_cache_entry)
                db.session.commit()
                print("Cached new translation in db")
                
            return translated_data 
        
        except Exception as e:
            print(f"Error decoding response JSON: {e}")
            return None
    
    else:
        print(f"API request failed with status code: {response.status_code}")
        return None