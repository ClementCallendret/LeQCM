from flask import Blueprint, request,session, render_template, redirect, url_for, flash
import database
import json

crea_sujets = Blueprint('Création_Sujets',__name__)

@crea_sujets.route('/Création_Sujets/')
def init():
    if "loginP" in session:
        return render_template("Création_Sujets.html", title="", tags=tags, state="", stateFormated="", idAnswers="[]", answers=[], answersFormated=[], numeralAnswer=0, selectedTag=[], newTags="[]"))
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.initRedirect', redirection="Création_Sujets"))
