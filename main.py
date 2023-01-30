from flask import render_template, Flask, request,Blueprint, session

from login import logi
from logout import logo
from register import regist
from connected import connect
from editeur import edit
from mesQuestions import mesQues
from creation import crea

app = Flask(__name__)
app.register_blueprint(logi)
app.register_blueprint(logo)
app.register_blueprint(regist)
app.register_blueprint(connect)
app.register_blueprint(edit)
app.register_blueprint(mesQues)
app.register_blueprint(crea)

app.config['SECRET_KEY'] = "SamyLePlusBeauuuUwU"
@app.route('/')
def accueil():
    login = ""
    if 'login' in session:
        connected=True
        login = session['login']
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
    if 'loginE' in session:
        login = session['loginE']
    elif 'loginP' in session:
        login = session['loginP']
    return dict(login=login)
    



app.run(host='0.0.0.0', port=5000, debug=True)