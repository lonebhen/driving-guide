from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db = SQLAlchemy()


class NLPAPICache(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    api_key = db.Column(db.String(255), unique=True, nullable = False)
    value = db.Column(db.String(255), nullable = False)
    
class DialectEnum(Enum):
    TWI = "tw"
    FANTE ="fat"
    DAGBANI="dag"
    GURENE="gur"
    YORUBA="yo"
    GA = "gaa"
    HAUSA = "hausa"
    EWE = "ee"
    
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    msisdn = db.Column(db.String(255), unique = True, nullable = False)
    local_dialect = db.Column(db.Enum(DialectEnum), nullable=False)