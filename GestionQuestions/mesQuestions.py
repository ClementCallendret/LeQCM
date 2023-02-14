from flask import render_template, Blueprint, session, redirect, url_for,flash, request
import database
import formatage
import json

mesQues = Blueprint('mesQuestions',__name__)

@mesQues.route('/MesQuestions')
def mesQuestions():
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
    return redirect(url_for('login.init'))

@mesQues.route('/MesQuestions/Delete', methods=['POST'])
def deleteQuestions():
  idList = []
  for key,value in request.form.items():
    idList.append(key)
  print(idList)
  for id in idList :
    if database.possedeQuestion(id, session["loginP"]):
      database.deleteQuestion(id)
  return redirect(url_for('mesQuestions.mesQuestions'))