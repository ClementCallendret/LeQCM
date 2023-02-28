from flask import Blueprint, request,session, render_template, redirect, url_for, flash
import database
import encryption

profil = Blueprint('profil',__name__)

@profil.route('/profil')
def mainPage():
    if "loginP" in session:
        return render_template("Profil.html", identity=database.getProfIdentity(session['loginP']))
    elif "loginE" in session:
        return render_template("Profil.html", identity=database.getStudentIdentity(session['loginE']))
    return render_template("Profil.html")

@profil.route('/profil/password', methods=['POST'])
def modifyPassword():
    newPassword = request.form['newPassword']
    login = ""
    statut = ""
    if "loginP" in session:
        statut = "P"
        login = session['loginP']
    elif "loginE" in session:
        statut = "S"
        login = session['loginE']
    else:
        return redirect(url_for('login.initRedirect', redirection="profil"))
    
    if (encryption.decrypt(login, request.form['password'], statut)):
        encrypt = encryption.encrypt(newPassword)
        newPassword = encrypt[0]
        newSel = encrypt[1]
        if statut == "P":
            if database.updateProfessorPassword(login, newPassword, newSel):
                flash("Mot de passe modifié")
            else:
                flash("Erreur lors de la modification du mot de passe")
        else:
            if database.updateStudentPassword(login, newPassword, newSel):
                flash("Mot de passe modifié")
            else:
                flash("Erreur lors de la modification du mot de passe")
        return redirect(url_for('profil.mainPage'))
    else:
        flash('Mot de passe incorrect')
        return redirect(url_for('profil.mainPage'))
