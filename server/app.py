from flask import Flask
from flask import request,Response
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@127.0.0.1:3306/progettoFinale"

db.init_app(app)

#frontend routes
@app.get("/loggedHome")
def logged_view():
    return 0

@app.get("/")
def home():
    utenti = User.query.all()
    for item in utenti:
        # Stampa le informazioni dell'utente
        print(f"ID: {item.id}, Username: {item.nome},  Cognome: {item.cognome}, Email: {item.email}, Password: {item.password}")
    return '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Document</title> </head> <body> <p>Hello world</p> </body> </html>'

#autentication routes
@app.post("/login")
def login():
    data = request.get_json()
    print(data)
    response = Response()
    response.status = 200
    return response
    

@app.post("/register")
def register():
    data = request.get_json()
    print(data)
    response = Response()
    response.status = 200
    return response

from models import User
'''
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'
'''