from flask import Blueprint,Response,jsonify,request,session,url_for,redirect
from models import User
from validateRules import user_schema,ValidationError
from userController import UserController
import hashlib


routes = Blueprint('routes', __name__)

#frontend routes
@routes.get("/")
def index():
    return '<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Document</title> </head> <body> <p>Hello world</p> </body> </html>'

#autentication routes
@routes.post("/login")
def login():
    data = request.get_json()
    #print(data)

    try:
        user = User.query.filter_by(email=data['email']).first()
        
        #controlliamo anche la password
        hashedPassword = hashlib.sha256(data['password'].encode()).hexdigest()
        if(hashedPassword == user.password):
            session['user_id'] = user.id
            return redirect(url_for('routes.index'))
        else:
            raise Exception
        
    except Exception:
        return "Errore: login", 500

@routes.post("/register")
def register():
    #recupero dati dal body della request
    data = request.get_json()
    
    try:
        #validazione dei dati
        user_schema.load(data)
        #proseguo se la validazione ha successo
        userController = UserController()
        #controllo sull' operazione di aggiunta utente al db
        if(userController.addUser(data) == False):
            raise Exception("Errore interno")
        #response con status 200
        response = Response()
        response.status = 200
        return response
    except ValidationError as err:
        #intercetto errore di validazione
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        #intercetto errore generico
        return f"Errore: {str(e)}", 500

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