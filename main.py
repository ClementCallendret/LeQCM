from flask import render_template, Flask, request,Blueprint, session

from login import logi
from logout import logo
from register import regist
from connected import connect
from editeur import edit

app = Flask(__name__)
app.register_blueprint(logi)
app.register_blueprint(logo)
app.register_blueprint(regist)
app.register_blueprint(connect)
app.register_blueprint(edit)

app.config['SECRET_KEY'] = "SamyLePlusBeauuuUwU"
#initialisation du login a vide

@app.route('/')
def gestion_acc():
    login=False
    if 'username' in session:
        login=True
    return render_template('Accueil.html',login=login)

app.run(host='0.0.0.0', port=5000, debug=True)