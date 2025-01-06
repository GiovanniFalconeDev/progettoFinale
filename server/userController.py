import hashlib
from models import User
from dbConnection import db

class UserController():
    def addUser(self, data):
        password = data['password']
        hashedPassword = hashlib.sha256(password.encode()).hexdigest()
        
        new_user = User(nome=data['nome'], cognome=data['cognome'], email=data['email'], password=hashedPassword)
        try:
            db.session.add(new_user)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False
            