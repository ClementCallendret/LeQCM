from flask import render_template, Blueprint, session, redirect, url_for,flash, request
import database
import formatage
import json

mesQuestions = Blueprint('mesQuestions',__name__)

@mesQuestions.route('/MesQuestions')
def mainPage():
  if "loginP" in session:
    #on charge les question de l'utilisateur et tous les tags pour le filtrage 
    tags = database.allTags()
    questions = database.loadQuestionsByProf(session["loginP"])
    for q in questions :
      q["state"] = formatage.formatageMD(q["state"])

    sequences = database.loadSequencesByProf(session["loginP"])

    return render_template("MesQuestions.html", questions=questions, tags=tags, sequences=sequences)
  else:
    flash("Vous devez être connecté pour acceder à cette page")
    return redirect(url_for('login.initRedirect', redirection="MesQuestions"))

@mesQuestions.route('/MesQuestions/Delete', methods=['POST'])
def deleteQuestions():
  if "loginP" in session:
    questionIdList = json.loads(request.form["selectedQ"])
    for id in questionIdList :
      if database.possedeQuestion(id, session["loginP"]):
        database.deleteQuestion(id)

    sequenceIdList = json.loads(request.form["selectedS"])
    for id in sequenceIdList :
      if database.possedeSequence(id, session["loginP"]):
        database.deleteSequence(id)
    return redirect(url_for('mesQuestions.mainPage'))
  else:
    flash("Vous devez être connecté pour acceder à cette page")
    return redirect(url_for('login.initRedirect', redirection="MesQuestions"))