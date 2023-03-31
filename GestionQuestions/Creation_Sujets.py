from flask import Blueprint, request,session, render_template, redirect, url_for, flash
import database
import json
import generateurS

crea_sujets = Blueprint('Création_Sujets',__name__)

@crea_sujets.route('/Création_Sujets/')
def init():
    if "loginP" in session:
        return render_template("Création_Sujets.html", title="", tags=tags, state="", stateFormated="", idAnswers="[]", answers=[], answersFormated=[], numeralAnswer=0, selectedTag=[], newTags="[]")
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.initRedirect', redirection="Création_Sujets"))

@crea_sujets.route('/CreaS',methods = ['POST'])
def CreaS():
    if "loginP" in session:
        if (request.method == 'POST'):
            #On récupère des données 
            idP = session["loginP"]
            allTags = database.allTagsByProf(idP)

            nbr_sujets = request.form.get(nbr_sujets)
            button_anonymat = request.form.get(button_anonymat)
            button_ordre = request.form.get(button_ordre)
            intervalle = request.form.get(intervalle)
            #Si intervalle 
            if intervalle=="on":
                pass
            else :
                pass
            tabData = []
            for tag in allTags:
                print(request.form.get(tag))

            return render_template("PageQcm.html",questions = questions, title=title, anonyme = anonyme)
