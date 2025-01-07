from flask import Blueprint,Response,jsonify,request,session,url_for,redirect,render_template
from flask_cors import CORS,cross_origin
from models import User
from validateRules import user_schema,ValidationError
from userController import UserController
import hashlib
from spootifyUtil import makeCallToSpotify,getPlaylists


routes = Blueprint('routes', __name__)

#frontend routes

#home page
@routes.get("/")
def index():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    else:
        userData = User.query.filter_by(id=session['user_id']).first()
        playlistsData = getPlaylists()
        return render_template('home.html', nome=userData.nome, cognome=userData.cognome, email=userData.email, playlists = playlistsData['items'], next = playlistsData['next'], previous = playlistsData['previous'])

#login page
@routes.get("/login")
def renderLogin():
    if 'user_id' not in session:
        return render_template('login.html')
    else:
        return redirect(url_for('routes.index'))
        
#register page
@routes.get("/register")
def renderRegister():
    if 'user_id' not in session:
        return render_template('register.html')
    else:
         return redirect(url_for('routes.index'))

#autentication routes
@routes.post("/login")
@cross_origin(origin='*')
def login():
    data = request.get_json()
    #print(data)

    try:
        user = User.query.filter_by(email=data['email']).first()
        
        #controlliamo anche la password
        hashedPassword = hashlib.sha256(data['password'].encode()).hexdigest()
        if(hashedPassword == user.password):
            session['user_id'] = user.id
            return redirect('/')
        else:
            raise Exception
        
    except Exception:
        return "Errore: login", 500

@routes.post("/register")
@cross_origin(origin='*')
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

#logout route
@routes.get("/logout")
def logout():
    if 'user_id' not in session:
        return redirect(url_for('routes.renderLogin'))
    else:
        session.clear()
        response = Response()
        response.status = 200
        return redirect(url_for('routes.renderLogin'))
        
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