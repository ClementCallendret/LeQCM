from flask import Flask, render_template
from flask import Blueprint

from login import log
from register import regist
from connected import connect



app = Flask(__name__)
app.register_blueprint(log)
app.register_blueprint(regist)
app.register_blueprint(connect)

@app.route('/')

def init():
  return render_template('Accueil.html')

app.run(host='0.0.0.0', port=5000)
app.run(debug=True)