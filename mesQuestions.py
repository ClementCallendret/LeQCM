from flask import render_template, request, Blueprint
import markdown
import md_mermaid, latex
import base64 

mesQues = Blueprint('mesQuestions',__name__)

@mesQues.route('/MesQuestions')
def mesQuestions():
  return render_template("MesQuestions.html")
