from flask import render_template, Flask
import login,register,connected

app = Flask(__name__)
@app.route('/')
def gestion_acc():
  return render_template('Accueil.html')

app.run(host='0.0.0.0', port=5000)
