from dbConnection import db
from app import app
class User(db.Model):
    __tablename__ = "utente"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255),  nullable=False)
    cognome = db.Column(db.String(255),  nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)


# Creazione delle tabelle con il contesto dell'applicazione
with app.app_context():
    db.create_all()  # Crea le tabelle nel database