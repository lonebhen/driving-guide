from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class NLPAPICache(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    api_key = db.Column(db.String(255), unique=True, nullable = False)
    value = db.Column(db.String(255), nullable = False)