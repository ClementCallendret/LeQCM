from flask import Blueprint, request,session, render_template

ajt_Stu = Blueprint('AjoutStudents',__name__)

@ajt_Stu.route('/AjoutStudents/')
def AjoutStudents():
    return render_template("AjoutStudents.html")

