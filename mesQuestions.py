from flask import render_template, Blueprint

mesQues = Blueprint('mesQuestions',__name__)

@mesQues.route('/MesQuestionsEHOOOOH')
def mesQuestions():
  return render_template("MesQuestions.html")
