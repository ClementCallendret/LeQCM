from flask import Blueprint, request,render_template, url_for
import database
import formatage

crea = Blueprint('creation',__name__)

@crea.route('/MesQuestions/creerQCM',methods = ['POST'])
def creation():
    listeQ = []
    if (request.method == 'POST'):
        for key,value in request.form.items():
            listeQ.append(key)
        res = []
        for ID in listeQ:
            res.append(database.loadQuestionById(ID))
        res = formatage.dictTodictFormated(res)
        #Pour numéroter les questions 
        for i in range (len(res)):
            res[i]['state'] = str(i+1)+". "+res[i]['state']
        #Formatage
        if (listeQ != []):
            return render_template("creation.html",res = res) 
    return render_template('MesQuestions.html') 
