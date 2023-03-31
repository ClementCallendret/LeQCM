from flask import Blueprint, request,session, render_template, redirect, url_for, flash
import database
import json
import generateurS

crea_sujets = Blueprint('Création_Sujets',__name__)

@crea_sujets.route('/Création_Sujets/')
def init():
    if "loginP" in session:
        tags = database.allTags()
        #print(generateurS.tagMultiples([[1,"a"],[2,"b"]]))
        return render_template("Création_Sujets.html", title="", tags=json.dumps(tags, indent=4), state="", stateFormated="", idAnswers="[]", answers=[], answersFormated=[], numeralAnswer=0, selectedTag=[], newTags="[]")
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.initRedirect', redirection="Création_Sujets"))
