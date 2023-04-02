from flask import Blueprint, request,session, render_template, redirect, url_for, flash
import database
import json
import generateurS
#A virer plus tard mais jsp il veut idToquestion en plus
from generateurS import IdToQuestion
crea_sujets = Blueprint('Création_Sujets',__name__)

@crea_sujets.route('/Création_Sujets/')
def init():
    if "loginP" in session:
        tags = database.allTags()
        #print(generateurS.tagMultiples([[1,"a"],[2,"b"]]))
        return render_template("Création_Sujets.html", title="", tags = tags, tagsJSON=json.dumps(tags, indent=4), state="", stateFormated="", idAnswers="[]", answers=[], answersFormated=[], numeralAnswer=0, selectedTag=[], newTags="[]")
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
            titre = request.form.get(titre)
            #Si intervalle 
            tabQ = []
            if intervalle=="on":
                nbr_questions = request.form.get(nbr_questions)
                for i in range(len(allTags)):
                    tabQ.append([request.form.get(allTags[i]+"min"),request.form.get(allTags[i]+"max")])
                    tabQ[allTags[i]] = allTags[i]
                
                #tabQ contient pour tout les tags, leur min et leur max
                # [["java",[2,5]]["C",[5,7]]]
            else :
                for i in range(len(allTags)):
                    tabQ.append(request.form.get(allTags[i]))
                    tabQ[allTags[i]] = allTags[i]
                #tabQ contient pour tout les tags, leur nombre souhaités 
                #exemple tabQ[[5,"java"],[7,"c"]]
                tabQ = generateurS(tabQ,nbr_sujets)
                #tabQ contient tout les sujets avec à la place des questions l'id des questions 
                #Donc va falloir que je fasse une fonction 
                questions = IdToQuestion(tabQ)
            return render_template("PageQcm.html",questions = questions, title=titre, anonyme = button_anonymat)
