from flask import render_template, Blueprint, session, redirect, url_for,flash
import database

mesQues = Blueprint('mesQuestions',__name__)

@mesQues.route('/MesQuestions')
def mesQuestions():
  if "login" in session:
    #on charge les question de l'utilisateur et tous les tags pour le filtrage 
    tags = database.allTags()
    questions = database.loadQuestionsByProf(session["login"])

    return render_template("MesQuestions.html", questions=questions, tags=tags)
  else:
    flash("Vous devez être connecté pour acceder à cette page")
    return redirect(url_for('login.init'))
