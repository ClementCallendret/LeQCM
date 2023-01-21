from flask import Blueprint, request,render_template, url_for
import fileIO
import formatage

crea = Blueprint('creation',__name__)

@crea.route('/MesQuestions/creerQCM',methods = ['POST'])
def creation():
    listeQ = []
    print("let's gooooo")
    print(request.form)
    if (request.method == 'POST'):
        for key,value in request.form.items():
            listeQ.append(key)
        res = []
        for ID in listeQ:
            res.append(fileIO.format.questionToDic(fileIO.question.read(ID)))
        #Pour numéroter les questions 
        for i in range (len(res)):
            res[i]['state'] = str(i+1)+". "+res[i]['state']
        #Formatage
        res = formatage.dictTodictFormated(res)
        if (listeQ != []):
            return render_template("creation.html",res = res) 
    return render_template('MesQuestions.html') 
