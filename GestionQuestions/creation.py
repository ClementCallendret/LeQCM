from flask import Blueprint, request,render_template, url_for, redirect, session, flash
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

    allQuestions = database.loadQuestionsByProf(session["loginP"])
    for q in allQuestions :
      q["state"] = formatage.formatageMD(q["state"])
    
    return render_template("Sorting.html", questions=jsoned, id="new", title="", button="Creer une Séquence", allQuestions=allQuestions)

@creation.route("/MesQuestions/UpdateSequence/<id>")
def updateSequence(id):
    if "loginP" in session and database.possedeSequence(id,session["loginP"]):
        seq = database.loadSequenceById(id)
        questions = []
        for id in seq["idList"]:
            q = database.loadQuestionById(id)
            q["state"] = formatage.formatageMD(q["state"])
            questions.append(q)
        jsoned = json.dumps(questions, indent=4)

        allQuestions = database.loadQuestionsByProf(session["loginP"])
        for q in allQuestions :
            q["state"] = formatage.formatageMD(q["state"])

        return render_template("Sorting.html", questions=jsoned, id=id, title=seq["title"], button="Sauvegarder les modifications", allQuestions=allQuestions)
    else:
        return redirect(url_for('mesQuestions.mainPage'))

        
@creation.route('/MesQuestions/PageQCM',methods = ['POST'])
def creationPageQCM():
    idList = json.loads(request.form["orderedId"])
    questions = []
    for id in idList:
        questions.append(database.loadQuestionById(id))
    questions = formatage.dictTodictFormated(questions)
    title = request.form.get("title")
    if title == "":
        title = "Sans Titre"
    return render_template("PageQcm.html",questions = questions, title=title)

@creation.route('/MesQuestions/CreerSequence',methods = ['POST'])
def creationSequence():
    idList = json.loads(request.form["orderedId"])
    if len(idList) == 0:
        flash("Vous n'avez pas sélectionné de questions")
    else:
        title = request.form.get("title")
        if title == "":
            title = "Sans Titre"

        if request.form["id"] == "new":
            database.saveSequence(idList, session["loginP"], title)
        else:
            database.updateSequence(request.form["id"], idList, title)
    return redirect(url_for('mesQuestions.mainPage'))

def union(list1,list2):
   result = list(set(list1 + list2))
   return result
