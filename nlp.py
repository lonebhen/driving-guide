import os
from dotenv import load_dotenv
import requests
import uuid

from model.models import NLPAPICache, db, DialectEnum
from io import BytesIO

load_dotenv()


# //TODO: Remove duplicate blocks

api_key = os.getenv('NLP_API_KEY')

headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-SUbscription-Key': api_key
    }


def translate_traffic_sign_predict_to_local_dialect(traffic_sign, local_dialect):
    print(traffic_sign)
    
    lang = DialectEnum[local_dialect.upper()].value
    cached_data = NLPAPICache.query.filter_by(api_key = traffic_sign, local_dialect = local_dialect).first()
    
    if cached_data:
        print("Returning cache from db")
        
        return cached_data.value
    
    url = 'https://translation-api.ghananlp.org/v1/translate'
    
    
    data = {
        "in": traffic_sign,
        "lang": "en-" + lang
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
                new_cache_entry = NLPAPICache(api_key=traffic_sign, value=translated_data, local_dialect = local_dialect)
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
    
    
    
def text_to_speech(text: str, local_dialect):
    
    lang = DialectEnum[local_dialect.upper()].value
    url = 'https://translation-api.ghananlp.org/tts/v1/tts'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "text": text,
        "language": lang
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
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
    
    
    
def translate_text(text, local_dialect):
    lang = DialectEnum[local_dialect].value
    
    url = 'https://translation-api.ghananlp.org/v1/translate'
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': api_key
    }
    payload = {
        "in": text,
        "lang": "en-" + lang
    }
    
    print(payload)

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        print(f"API request failed with status code: {response.status_code}")
        return None
    
    json_response = response.json()
    
    if isinstance(json_response, str):
        translated_text = json_response
    else:
        translated_text = json_response.get('data')
    print("Translated text " + translated_text)
    return translated_text


def convert_text_to_speech(text, local_dialect):
    lang = DialectEnum[local_dialect].value
    
    url = 'https://translation-api.ghananlp.org/tts/v1/tts'
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-SUbscription-Key': api_key
    }
    payload = {
        "text": text,
        "language": lang
    }
    
    print(payload)

    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Response from tts: {response}")

    if response.status_code != 200:
        print(f"TTS API request failed with status code: {response.status_code}")
        return None

    return response.content
    
    