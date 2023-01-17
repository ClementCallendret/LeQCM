from flask import render_template, Flask, request,Blueprint, session
from flask_login import LoginManager

from login import logi
from logout import logo
from register import regist
from connected import connect
from interpreteur import interpreteur


app = Flask(__name__)
app.register_blueprint(logi)
app.register_blueprint(logo)
app.register_blueprint(regist)
app.register_blueprint(connect)
app.register_blueprint(interpreteur)
app.config['SECRET_KEY'] = "SamyLePlusBeauuuUwU"
#initialisation du login a vide

@app.route('/')
def gestion_acc():
    login=False
    if 'username' in session:
        login=True
    return render_template('Accueil.html',login=login)

@app.route('/editeur', methods=['GET', 'POST'])
def editeurGet():
    if request.args.get('nbRep') is not None :
        question = {"enonce" : "", "enonceFormate" : "", "reponses" : []}
        question["enonce"] = request.args.get("enonce")
        #question["enonceFormate"] = fonctionDeSamy() !

        numsReponses = []
        for clef, val in request.args.items() :
            if(clef[0:-1] == "textReponse") :
                numsReponses.append(clef[-1])

        for n in numsReponses :
            question["reponses"].append({"val" : request.args.get("checkReponse" + n), "text" : request.args.get("textReponse" + n)})

        return render_template('EditeurDeQuestion.html', nbReponses= len(question["reponses"]), reponses=question["reponses"], enonce=question["enonce"])
    
    else :
        return render_template('EditeurDeQuestion.html', nbReponses= 0, reponses=[], enonce="")

app.run(host='0.0.0.0', port=5000)
app.run(debug=True)