import os
from dotenv import load_dotenv
import requests
import uuid

from model.models import NLPAPICache, db

load_dotenv()


api_key = os.getenv('NLP_API_KEY')

headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-SUbscription-Key': api_key
    }


def translate_traffic_sign_predict_to_local_dialect(traffic_sign):
    print(traffic_sign)
    cached_data = NLPAPICache.query.filter_by(api_key = traffic_sign).first()
    
    if cached_data:
        print("Returning cache from db")
        
        return cached_data.value
    
    url = 'https://translation-api.ghananlp.org/v1/translate'
    
    
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
    
    
    
def text_to_speech(text: str):
    url = 'https://translation-api.ghananlp.org/tts/v1/tts'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "in": text,
        "lang": "en-tw"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        # Assuming the API returns audio content directly
        audio_content = response.content
        
        # Save the audio content to a file with a unique name
        unique_filename = f'output_{uuid.uuid4()}.wav'
        output_path = os.path.join('audio_files', unique_filename)
        
        with open(output_path, 'wb') as audio_file:
            audio_file.write(audio_content)
        
        return output_path
    
    except requests.exceptions.RequestException as e:
        # Handle any request exceptions
        print(f"Error fetching TTS: {e}")
        return None