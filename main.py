from flask import render_template, Flask, request,Blueprint, session

from login import logi
from logout import logo
from register import regist
from connected import connect
from editeur import edit
from mesQuestions import mesQues

app = Flask(__name__)
app.register_blueprint(logi)
app.register_blueprint(logo)
app.register_blueprint(regist)
app.register_blueprint(connect)
app.register_blueprint(edit)
app.register_blueprint(mesQues)

app.config['SECRET_KEY'] = "SamyLePlusBeauuuUwU"
@app.route('/')
def accueil():
    login = ""
    if 'login' in session:
        connected=True
        login = session['login']
    return render_template('Accueil.html')


@app.context_processor
def isLoged():
    return dict(isLoged=session.get('login'))

@app.context_processor
def getLogin():
    login = ""
    if 'login' in session:
        login = session['login']
    return dict(login=login)
    

    

app.run(host='0.0.0.0', port=5000, debug=True)