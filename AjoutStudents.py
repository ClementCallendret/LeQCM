from flask import Blueprint, request,session, render_template, redirect, url_for, flash
import database
import json
import encryption

ajt_Stu = Blueprint('AjoutStudents',__name__)

@ajt_Stu.route('/AjoutStudents/')
def init():
    if "loginP" in session:
        return render_template("AjoutStudents.html")
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.initRedirect', redirection="AjoutStudents"))

    
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

