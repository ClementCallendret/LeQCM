from flask import render_template, request, Blueprint, session
from flask_sqlalchemy import SQLAlchemy
import models
import database

from extension import db, socketio, app # fichier a part pour éviter les circular imports

from Login.login import login
from Login.logout import logout
from Login.register import register
from Login.profil import profil
from GestionQuestions.editeur import editeur
from GestionQuestions.mesQuestions import mesQuestions
from GestionQuestions.creationSequence import creation
from Sessions.questionLive import questionLive
from AjoutStudents import ajt_Stu
from Sessions.archives import archives
from GestionQuestions.Creation_Sujets import crea_sujets

#nom de la variable accueillant le BluePrint
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(profil)
app.register_blueprint(editeur)
app.register_blueprint(mesQuestions)
app.register_blueprint(creation)
app.register_blueprint(questionLive)
app.register_blueprint(ajt_Stu)
app.register_blueprint(archives)
app.register_blueprint(crea_sujets)

app.config['SECRET_KEY'] = "SamyLePlusBeauuuUwU"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myQCM.db"
app.config["DEBUG"] = True

db.init_app(app)

with app.app_context():
    db.create_all()

#déclarer les sockets
#import le main dans les blueprints qui les utilisent
    
@app.route('/')
def accueil():
    return render_template('Accueil.html')


@app.context_processor
def isLogedP():
    result = ""
    if database.studentExist(session.get('loginE')):
        result = session.get('loginE')
    else:
        result = False
    return dict(isLogedP = session.get('loginP'))

@app.context_processor
def isLogedE():
    result = ""
    if database.studentExist(session.get('loginE')):
        result = session.get('loginE')
    else:
        result = False
    return dict(isLogedE = result)

@app.context_processor
def getLogin():
    login = ""
    if 'loginP' in session:
        login = session['loginP']
    elif 'loginE' in session:
        login = session['loginE']
    return dict(login=login)


# remplacé par les sockets
# app.run(host='0.0.0.0', port=5000, debug=True)
socketio.run(app)
