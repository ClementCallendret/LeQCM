from flask import Blueprint, request,session, render_template
import database
import json

ajt_Stu = Blueprint('AjoutStudents',__name__)

@ajt_Stu.route('/AjoutStudents/')
def init():
    return render_template("AjoutStudents.html")

    
@ajt_Stu.route('/AjoutStudents/', methods = ['POST'])
def AjoutStudents():
    if (request.method == 'POST'):
        studentToAdd = json.loads(request.form["StudentTab"])
        print(studentToAdd)
        for e in studentToAdd:
            database.addStudent(e[0], e[1], e[2], 0)

    return render_template("AjoutStudents.html")

