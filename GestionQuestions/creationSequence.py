from flask import Blueprint, request,render_template, url_for, redirect, session
import database
import formatage
import json

creation = Blueprint('creation',__name__)

@creation.route('/MesQuestions/Sorting', methods = ["POST"])
def sorting():
    idList = json.loads(request.form["selectedQ"])
    questions = []
    tags = database.allTagsByProf(session["loginP"])
    for id in idList:
        q = database.loadQuestionById(id)
        q["state"] = formatage.formatageMD(q["state"])
        questions.append(q)
    jsoned = json.dumps(questions, indent=4)

    allQuestions = database.loadQuestionsByProf(session["loginP"])
    for q in allQuestions :
      q["state"] = formatage.formatageMD(q["state"])
    
    return render_template("Sorting.html", questions=jsoned, id="new", title="", button="Creer une Séquence", allQuestions=allQuestions, tags=tags)

@creation.route("/MesQuestions/UpdateSequence/<id>")
def updateSequence(id):
    if "loginP" in session and database.possedeSequence(id,session["loginP"]):
        seq = database.loadSequenceById(id)
        questions = []
        for it in seq["idList"]:
            q = database.loadQuestionById(it)
            q["state"] = formatage.formatageMD(q["state"])
            questions.append(q)
        jsoned = json.dumps(questions, indent=4)

        allQuestions = database.loadQuestionsByProf(session["loginP"])
        for q in allQuestions :
            q["state"] = formatage.formatageMD(q["state"])

        print(id)
        return render_template("Sorting.html", questions=jsoned, id=id, title=seq["title"], button="Sauvegarder les modifications", allQuestions=allQuestions)
    else:
        return redirect(url_for('mesQuestions.mainPage'))

        
@creation.route('/MesQuestions/PageQCM',methods = ['POST'])
def creationPageQCM():
    idList = json.loads(request.form["orderedId"])
    questions = []
    for id in idList:
        questions.append(database.loadQuestionById(id))
    questions = formatage.formatQuestionList(questions)
    title = request.form.get("title")
    if title == "":
        title = "Sans Titre"
    return render_template("PageQcm.html",questions = questions, title=title, anonyme = False)

@creation.route('/MesQuestions/CreerSequence',methods = ['POST'])
def creationSequence():
    idList = json.loads(request.form["orderedId"])
    title = request.form.get("title")
    if title == "":
        title = "Sans Titre"
    
    id = 0
    if request.form["id"] == "new":
        id = database.saveSequence(idList, session["loginP"], title)
    else:
        id = (int)(request.form["id"])
        database.updateSequence(request.form["id"], idList, title)
    return redirect(url_for('creation.updateSequence', id=id))

def union(list1,list2):
   result = list(set(list1 + list2))
   return result
