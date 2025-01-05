from app import db

class User(db.Model):
    __tablename__ = "utente"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255),  nullable=False)
    cognome = db.Column(db.String(255),  nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
