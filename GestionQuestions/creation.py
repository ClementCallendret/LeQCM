from flask import Blueprint, request,render_template, url_for, redirect, session
import database
import formatage
import json

crea = Blueprint('creation',__name__)

@crea.route('/MesQuestions/Sorting', methods = ["POST"])
def sorting():
    idList = []
    for key,value in request.form.items():
        idList.append(key)
    questions = []
    for id in idList:
        q = database.loadQuestionById(id)
        q["state"] = formatage.formatageMD(q["state"])
        questions.append(q)
    jsoned = json.dumps(questions, indent=4)
    return render_template("QuestionOrder.html", questions=jsoned)

@crea.route('/MesQuestions/validerSelection',methods = ['POST'])
def validerSelection():
    ids = json.loads(request.form.get("orderedId"))
    if request.form["action"] == "Page":
        return creationPageQCM(ids)
    else:
        title = request.form.get("title")
        if title is None:
            title = "Sans Titre"

        return creationSequence(ids, title)

def creationPageQCM(idList):
    questions = []
    for id in idList:
        questions.append(database.loadQuestionById(id))
    questions = formatage.dictTodictFormated(questions)
    #Pour numéroter les questions 
    for i in range (len(questions)):
        questions[i]['state'] = str(i+1)+". "+questions[i]['state']
    #Formatage
    if (idList != []):
        return render_template("creation.html",res = questions)

def creationSequence(idList, title):
    print(database.saveSequence(idList, session["loginP"], title))
    return redirect(url_for('mesQuestions.mesQuestions'))
