from flask import Blueprint, Flask, request, redirect, url_for,render_template, flash, session
import database
import encryption
archive = Blueprint('archive',__name__)


@archive.route('/archives')
def init():
    if "loginP" in session:
        idProf = session['loginP']
        sessions = database.loadSessionByProf(idProf)
        print(session)
        return render_template("archives.html", sessions=sessions)
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.init'))

@archive.route('/stats/<idSession>')
def stats():
    if "loginP" in session:
        idProf = session['loginP']
        idSession = request.args.get('idSession')
        result = database.getSessionResults(idSession)
        return render_template("stats.html",result)
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.init'))