from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()

class DialectEnum(Enum):
    TWI = "tw"
    FANTE ="fat"
    DAGBANI="dag"
    GURENE="gur"
    YORUBA="yo"
    GA = "gaa"
    HAUSA = "hausa"
    EWE = "ee"
    


class NLPAPICache(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    api_key = db.Column(db.String(255), unique=True, nullable = False)
    value = db.Column(db.String(255), nullable = False)
    local_dialect = db.Column(db.Enum(DialectEnum), nullable=False)
    

    
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    msisdn = db.Column(db.String(255), unique = True, nullable = False)
    local_dialect = db.Column(db.Enum(DialectEnum), nullable=False)
    
    
class OTPStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    msisdn = db.Column(db.String(20), unique=True, nullable=False)
    otp = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)