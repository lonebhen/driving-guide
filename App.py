from sqlite3 import IntegrityError
from flask import *
import tensorflow as tf
import os
from werkzeug.utils import secure_filename
from keras.models import load_model
import numpy as np
from PIL import Image, ImageOps
from model.models import User, db, DialectEnum
from nlp import translate_traffic_sign_predict_to_local_dialect
from otp import generate_otp

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///driving_guide.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

# traffic class
classes = ['A-1', 'A-11', 'A-11a', 'A-12a', 'A-14', 'A-15', 'A-16', 'A-17', 'A-18b', 'A-2', 'A-20', 'A-21',
                   'A-24', 'A-29', 'A-3', 'A-30', 'A-32', 'A-4', 'A-6a', 'A-6b', 'A-6c', 'A-6d', 'A-6e', 'A-7', 'A-8',
                   'B-1', 'B-18', 'B-2', 'B-20', 'B-21', 'B-22', 'B-25', 'B-26', 'B-27', 'B-33', 'B-34', 'B-36', 'B-41',
                   'B-42', 'B-43', 'B-44', 'B-5', 'B-6-B-8-B-9', 'B-8', 'B-9', 'C-10', 'C-12', 'C-13', 'C-13-C-16',
                   'C-13a', 'C-13a-C-16a', 'C-16', 'C-2', 'C-4', 'C-5', 'C-6', 'C-7', 'C-9', 'D-1', 'D-14', 'D-15',
                   'D-18', 'D-18b', 'D-2', 'D-21', 'D-23', 'D-23a', 'D-24', 'D-26', 'D-26b', 'D-26c', 'D-27', 'D-28',
                   'D-29', 'D-3', 'D-40', 'D-41', 'D-42', 'D-43', 'D-4a', 'D-4b', 'D-51', 'D-52', 'D-53', 'D-6', 'D-6b',
                   'D-7', 'D-8', 'D-9', 'D-tablica', 'G-1a', 'G-3']

class_names = {
                'A-1': 'Dangerous right turn',
                'A-11': 'Uneven road',
                'A-11a': 'Speed bump',
                'A-12a': 'Narrowing of the road - both sides',
                'A-14': 'Roadworks',
                'A-15': 'Slippery road',
                'A-16': 'Pedestrian crossing',
                'A-17': 'Children',
                'A-18b': 'Wild animals',
                'A-2': 'Dangerous left turn',
                'A-20': 'Two-way traffic section',
                'A-21': 'Tram',
                'A-24': 'Cyclists',
                'A-29': 'Traffic lights',
                'A-3': 'Dangerous bends, first right',
                'A-30': 'Other danger',
                'A-32': 'Road may be icy',
                'A-4': 'Dangerous bends, first left',
                'A-6a': 'Intersection with priority road on both sides',
                'A-6b': 'Intersection with priority road on the right side',
                'A-6c': 'Intersection with priority road on the left side',
                'A-6d': 'Entry of one-way road from the right',
                'A-6e': 'Entry of one-way road from the left',
                'A-7': 'Yield',
                'A-8': 'Roundabout',
                'B-1': 'No entry in both directions',
                'B-18': 'No entry for vehicles exceeding ... tons',
                'B-2': 'No entry',
                'B-20': 'STOP',
                'B-21': 'No left turn',
                'B-22': 'No right turn',
                'B-25': 'No overtaking',
                'B-26': 'No overtaking for trucks',
                'B-27': 'End of no overtaking',
                'B-33': 'Speed limit',
                'B-34': 'End of speed limit',
                'B-36': 'No parking',
                'B-41': 'No pedestrian traffic',
                'B-42': 'End of prohibitions',
                'B-43': 'Restricted speed zone',
                'B-44': 'End of restricted speed zone',
                'B-5': 'No entry for trucks',
                'B-6-B-8-B-9': 'No entry for non-motorized vehicles',
                'B-8': 'No entry for horse-drawn vehicles',
                'B-9': 'No entry for bicycles',
                'C-10': 'Drive on the left side of the sign',
                'C-12': 'Roundabout',
                'C-13': 'Cycle path',
                'C-13-C-16': 'Pedestrian and cyclist path',
                'C-13a': 'End of cycle path',
                'C-13a-C-16a': 'End of pedestrian and cyclist path',
                'C-16': 'Pedestrian path',
                'C-2': 'Turn right after the sign',
                'C-4': 'Turn left after the sign',
                'C-5': 'Go straight',
                'C-6': 'Go straight or turn right',
                'C-7': 'Go straight or turn left',
                'C-9': 'Drive on the right side of the sign',
                'D-1': 'Priority road',
                'D-14': 'End of lane',
                'D-15': 'Bus stop',
                'D-18': 'Parking',
                'D-18b': 'Covered parking',
                'D-2': 'End of priority road',
                'D-21': 'Hospital',
                'D-23': 'Gas station',
                'D-23a': 'Gas-only station',
                'D-24': 'Telephone',
                'D-26': 'Service station',
                'D-26b': 'Car wash',
                'D-26c': 'Public toilet',
                'D-27': 'Snack bar or café',
                'D-28': 'Restaurant',
                'D-29': 'Hotel (motel)',
                'D-3': 'One-way road',
                'D-40': 'Residential zone',
                'D-41': 'End of residential zone',
                'D-42': 'Built-up area',
                'D-43': 'End of built-up area',
                'D-4a': 'Road closed to traffic',
                'D-4b': 'Access to closed road',
                'D-51': 'Speed camera',
                'D-52': 'Traffic area',
                'D-53': 'End of traffic area',
                'D-6': 'Pedestrian crossing',
                'D-6b': 'Pedestrian crossing and cyclist path',
                'D-7': 'Expressway',
                'D-8': 'End of expressway',
                'D-9': 'Motorway',
                'D-tablica': 'Information board',
                'G-1a': 'Direction indicator post with three bars, placed on the right side of the road',
                'G-3': 'St. Andrew\'s Cross before a single-track level crossing'
            }


def model_predict(img_path):
    model = load_model('./model/augmented.h5')
    image = Image.open(img_path)
    image = image.resize((32, 32))
    
    image_arr = np.array(image.convert('RGB'))
    image_arr.shape = (1, 32, 32, 3)
    
    result = model.predict(image_arr)
    
    ind = np.argmax(result)
    
    resolved_prediction =  class_names[classes[ind]]
    
    return translate_traffic_sign_predict_to_local_dialect(resolved_prediction)
    
    
    
    
    



@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        file_path = secure_filename(f.filename)
        f.save(file_path)

        # Make prediction
        result = model_predict(file_path)
        print(result)
        return result
    return None


@app.route('/generate-otp', methods=['POST'])
def generate_otp_endpoint():
    data = request.json
    msisdn = data.get('msisdn')
    
    response, status_code = generate_otp(msisdn)
    return jsonify(response), status_code


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    msisdn = data.get('msisdn')
    local_dialect = data.get('local_dialect')
    
    if not msisdn or not local_dialect:
        return jsonify({"error": "msisdn and local_dialect are required"}), 400
    
    try:
        user = User(msisdn=msisdn, local_dialect=DialectEnum[local_dialect.upper()])
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User with this msisdn already exists"}), 400
    except KeyError:
        return jsonify({"error": "Invalid local_dialect"}), 400
    
    
    otp_response, status_code = generate_otp(msisdn)
    
    if status_code != 200:
        return jsonify({"error": otp_response.get('error')}), status_code
    
    return jsonify({"message": "User registered successfully", "otp": otp_response}), 201




app.route('/update_local_dialect', methods=['PUT'])
def update_local_dialect():
    data = request.json
    user_id = data.get('user_id')
    new_local_dialect = data.get('local_dialect')
    
    if not user_id or not new_local_dialect:
        return jsonify({"error": "user_id and local_dialect are required"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    try:
        user.local_dialect = DialectEnum[new_local_dialect.upper()]
        db.session.commit()
        return jsonify({"message": "Local dialect updated successfully"}), 200
    except KeyError:
        return jsonify({"error": "Invalid local_dialect"}), 40
    





if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)
