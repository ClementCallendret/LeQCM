from flask import render_template, request, Blueprint, session
from flask_sqlalchemy import SQLAlchemy
import models

from extension import db, socketio, app # fichier a part pour éviter les circular imports

from Login.login import logi
from Login.logout import logo
from Login.register import regist
from Login.connected import connect
from GestionQuestions.editeur import edit
from GestionQuestions.mesQuestions import mesQues
from GestionQuestions.creation import crea
from questionLive import questionLive
from AjoutStudents import ajt_Stu

#nom de la variable accueillant le BluePrint
app.register_blueprint(logi)
app.register_blueprint(logo)
app.register_blueprint(regist)
app.register_blueprint(connect)
app.register_blueprint(edit)
app.register_blueprint(mesQues)
app.register_blueprint(crea)
app.register_blueprint(questionLive)
app.register_blueprint(ajt_Stu)

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
    return dict(isLogedP = session.get('loginP'))

@app.context_processor
def isLogedE():
    return dict(isLogedE = session.get('loginE'))

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
