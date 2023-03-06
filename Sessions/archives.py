from flask import Blueprint, Flask, request, redirect, url_for,render_template, flash, session
import database
import encryption
import json

archives = Blueprint('archives',__name__)

@archives.route('/archives')
def init():
    if "loginP" in session:
        idProf = session['loginP']
        sessions = database.loadSessionDataByProf(idProf)
        print(sessions)
        return render_template("archives.html", sessions=sessions)
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.initRedirect', redirection="archives"))
    
@archives.route('/archives/historique')
def historique():
    if "loginP" in session:
        idProf = session['loginP']
        mySessions = database.loadSessionDataByProf(session["loginP"])
        print(mySessions)
        return render_template("StatsOverTime.html", mySessions=json.dumps(mySessions, indent=4))
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.initRedirect', redirection="archives-historique"))

@archives.route('/archives/stats/<idSession>')
def stats(idSession):
    if "loginP" in session:
        idSession = request.args.get('idSession')
        result = database.loadSessionResults(idSession)
        return render_template("stats.html",result)
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.initRedirect', redirection="stats-"+idSession))