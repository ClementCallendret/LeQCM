from flask import render_template, Blueprint, session, redirect, url_for,flash
import fileIO

mesQues = Blueprint('mesQuestions',__name__)

@mesQues.route('/MesQuestions')
def mesQuestions():
  if "loginP" in session:
    #on charge les question de l'utilisateur et tous les tags pour le filtrage 
    tags = fileIO.question.getAllTags()
    questions = fileIO.question.listByAccount(session["loginP"])

    #on met les question dans des dictionnaires pour plus de clareté
    for i in range(len(questions)):
      questions[i] = fileIO.format.questionToDic(fileIO.question.read(questions[i]))

    return render_template("MesQuestions.html", questions=questions, tags=tags)
  else:
    flash("Vous devez être connecté pour acceder à cette page")
    return redirect(url_for('login.init'))
