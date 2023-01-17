from flask import render_template, Flask, redirect, url_for, request, Blueprint

from login import log
from register import regist
from connected import connect
from editeur import edit

app = Flask(__name__)

app.register_blueprint(log)
app.register_blueprint(regist)
app.register_blueprint(connect)
app.register_blueprint(edit)

@app.route('/')
def gestion_acc():
    return render_template('Accueil.html')

app.run(host='0.0.0.0', port=5000, debug=True)