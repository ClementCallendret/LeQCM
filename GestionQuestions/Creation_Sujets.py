from flask import Blueprint, request,session, render_template, redirect, url_for, flash
import database
import json
import generateurS
from math import ceil
#A virer plus tard mais jsp il veut idToquestion en plus
from generateurS import IdToQuestion
crea_sujets = Blueprint('Création_Sujets',__name__)

@crea_sujets.route('/Création_Sujets/')
def init():
    if "loginP" in session:
        tags = database.nbQuestionsPerTag(session["loginP"])
        profStudents = database.getStudentsByProf(session["loginP"])
        #print(generateurS.generateurS([[1,"a"],[1,"b"]],2))
        return render_template("Création_Sujets.html", title="", tags = tags, tagsJSON=json.dumps(tags, indent=4), students=profStudents, tabSujet = [], anonyme = False)
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

            nbr_sujets = int(request.form.get("nbr_sujets"))
            button_anonymat = request.form.get("button_anonymat")
            button_ordre = request.form.get("button_ordre")
            intervalle = request.form.get("intervalle")
            titre = request.form.get("titre")
            print(nbr_sujets,button_anonymat,button_ordre,intervalle,titre)
            #Si intervalle 
            if button_anonymat == None:
                button_anonymat = False
            else:
                button_anonymat = True
            tabQ = []
            if intervalle != None:
                nbr_questions = int(request.form.get("nbr_questions"))
                for i in range(len(allTags)):
                    min = int(request.form.get(allTags[i]+"min"))
                    max =int(request.form.get(allTags[i]+"max"))
                    tabQ.append([[min]])
                    for j in range(min+1, max+1, 1):
                        tabQ[i][0].append(j)
                    tabQ[i].append(allTags[i])
                print("tabQ",tabQ)
                #tabQ contient pour tout les tags, les valeurs de l'intervalle [min,max]
                # [[[2,3,4,5],"java"][[5,,6,7],"C"]]
                tabIntervalle = []
                for i in range(len(tabQ)):
                    tabIntervalle.append(tabQ[i][0])
                print("TabIntervalle", tabIntervalle)


                tabCombi = generateurS.combi(tabIntervalle, 0, [], nbr_questions)
                print("tabCombi",tabCombi)
                #tabcombi = [[1, 2], [1, 2]] 1Q tag A et 2Q tag B puis inversement
                tabQAvecDiffCombi = []
                for i in range(len(tabCombi)):
                    tabQAvecDiffCombi.append([])
                    for j in range (len(tabCombi[i])):
                        tabQAvecDiffCombi[i].append([tabCombi[i][j]])
                        tabQAvecDiffCombi[i][j].append(tabQ[j][1])
                print("tabAvec diff combi", tabQAvecDiffCombi)
                nbCombi = len(tabCombi)
                print("nbCombi", nbCombi)
                tabNbSujet = []
                nbSujet = nbr_sujets
                for i in range(nbCombi):
                    nbSujet = ceil(nbr_sujets/nbCombi)
                    tabNbSujet.append(nbSujet)
                    nbr_sujets = nbr_sujets - nbSujet
                    nbCombi = nbCombi - 1
                print("tabNbSujet", tabNbSujet)
                tabSujetID2 = []
                for i in range(len(tabCombi)):
                    print("tabAvecDIffCombi",tabQAvecDiffCombi[i])
                    print("tabNbSujet",tabNbSujet[i])
                    tabSujetID=(generateurS.generateurS(tabQAvecDiffCombi[i],tabNbSujet[i]))
                    for sujet in tabSujetID:
                        tabSujetID2.append(sujet)
                print("tabSujetFinal",tabSujetID2)
            else :
                for i in range(len(allTags)):
                    #On récupère le nb de questions par Tag pour les tag où y a des questions
                    if request.form.get(allTags[i]) != None:
                        tabQ.append([int(request.form.get(allTags[i]))])
                        tabQ[i].append(allTags[i])
                #tabQ contient pour tout les tags, leur nombre souhaités 
                #exemple tabQ[[5,"java"],[7,"c"]]
                #print("TEST CREAS", generateurS.generateurS([[1,'a'],[1,'b']],2))
                tabSujetID2 = generateurS.generateurS(tabQ,nbr_sujets)
                print("TAB FINALE",tabSujetID2)
                #tabQ contient tout les sujets avec à la place des questions l'id des questions 
                #Donc va falloir que je fasse une fonction 
    
        if button_ordre != None:
            tabSujetFinal = generateurS.mixage(tabSujetID2)
        else:
            tabSujetFinal = tabSujetID2

        tabSujetFinalLeVrai = generateurS.IdToQuestion(tabSujetFinal)
        print(tabSujetFinalLeVrai)
        tags = database.nbQuestionsPerTag(session["loginP"])
        profStudents = database.getStudentsByProf(session["loginP"])
        return render_template("Création_Sujets.html", title=titre, tags = tags, tagsJSON=json.dumps(tags, indent=4), students=profStudents, tabSujet = tabSujetFinalLeVrai, anonyme = button_anonymat)
