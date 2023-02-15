from flask import Blueprint, request,render_template, url_for, redirect, session
import database
import formatage
import json

creation = Blueprint('creation',__name__)

@creation.route('/MesQuestions/Sorting', methods = ["POST"])
def sorting():
    idList = json.loads(request.form["selectedQ"])
    questions = []
    for id in idList:
        q = database.loadQuestionById(id)
        q["state"] = formatage.formatageMD(q["state"])
        questions.append(q)
    jsoned = json.dumps(questions, indent=4)
    return render_template("Sorting.html", questions=jsoned)

@creation.route('/MesQuestions/PageQCM',methods = ['POST'])
def creationPageQCM():
    idList = json.loads(request.form["orderedId"])
    questions = []
    for id in idList:
        questions.append(database.loadQuestionById(id))
    questions = formatage.dictTodictFormated(questions)
    #Pour numéroter les questions 
    for i in range (len(questions)):
        questions[i]['state'] = str(i+1)+". "+questions[i]['state']
    #Formatage
    if (idList != []):
        return render_template("PageQcm.html",res = questions)

@creation.route('/MesQuestions/CreerSequence',methods = ['POST'])
def creationSequence():
    idList = json.loads(request.form["orderedId"])
    title = request.form.get("title")
    if title == "":
        title = "Sans Titre"

    database.saveSequence(idList, session["loginP"], title)
    return redirect(url_for('mesQuestions.mainPage'))
