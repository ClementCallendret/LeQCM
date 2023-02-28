from flask import Blueprint, request,session, render_template
import database

profil = Blueprint('profil',__name__)

@profil.route('/profil')
def mainPage():
    if "loginP" in session:
        return render_template("Profil.html", identity=database.getProfIdentity(session['loginP']))
    elif "loginE" in session:
        return render_template("Profil.html", identity=database.getStudentIdentity(session['loginE']))
    return render_template("Profil.html")

