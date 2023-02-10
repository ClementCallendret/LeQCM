from flask import render_template, Blueprint, session, redirect, url_for,flash
import database
import formatage

mesQues = Blueprint('mesQuestions',__name__)

@mesQues.route('/MesQuestions')
def mesQuestions():
  if "loginP" in session:
    #on charge les question de l'utilisateur et tous les tags pour le filtrage 
    tags = database.allTags()
    questions = database.loadQuestionsByProf(session["loginP"])
    for q in questions :
      q["state"] = formatage.formatageMD(q["state"])

    return render_template("MesQuestions.html", questions=questions, tags=tags)
  else:
    flash("Vous devez être connecté pour acceder à cette page")
    return redirect(url_for('login.init'))

@mesQues.route('/order')
def order():
  return render_template("QuestionOrder.html")
