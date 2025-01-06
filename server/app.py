from datetime import timedelta
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@127.0.0.1:3306/progettoFinale"
app.config['SECRET_KEY'] = 'O@1lE#x9YZ!Qj&45^t8pVW%Kd7*mN6Rs'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

from routes import routes

# Registra il blueprint
app.register_blueprint(routes)

