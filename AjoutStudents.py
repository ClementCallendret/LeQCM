from flask import Blueprint, request,session, render_template
import database
import json
import encryption

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
            tab = encryption.encrypt(e[0])
            password = tab[0]
            sel = tab[1]
            database.addStudent(e[0], e[1], e[2], password, sel)

    return render_template("AjoutStudents.html")

