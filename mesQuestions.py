from flask import render_template, Blueprint, session

mesQues = Blueprint('mesQuestions',__name__)

@mesQues.route('/MesQuestions')
def mesQuestions():
  return render_template("MesQuestions.html")
