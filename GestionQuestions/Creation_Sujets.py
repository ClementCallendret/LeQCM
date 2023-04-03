from flask import Blueprint, request,session, render_template, redirect, url_for, flash
import database
import json
import generateurS

crea_sujets = Blueprint('Création_Sujets',__name__)

@crea_sujets.route('/Création_Sujets/')
def init():
    if "loginP" in session:
        tags = database.nbQuestionsPerTag(session["loginP"])
        profStudents = database.getStudentsByProf(session["loginP"])
        return render_template("Création_Sujets.html", title="", tags = tags, tagsJSON=json.dumps(tags, indent=4), students=profStudents)
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.initRedirect', redirection="Création_Sujets"))

@crea_sujets.route('/CreaS',methods = ['POST'])
def CreaS():
    if "loginP" in session:
        #On récupère des données 
        idP = session["loginP"]
        allTags = database.allTagsByProf(idP)

        nbr_sujets = int(request.form.get("nbr_sujets"))
        mixage = (request.form.get("button_ordre") != None)
        intervalle = (request.form.get("intervalle") != None)
        titre = request.form.get("titre")
        anonymat = (request.form.get("button_anonymat") != None)
        selectedTags = (request.form.get("selectedTags"))
        tabQ = []
        tabSujetID = []

        if intervalle:
            # On récupère tous les nombres inclus dans l'intervalle demandé par tag
            nbr_questions = int(request.form.get("nbr_questions"))
            for i in range(len(selectedTags)):
                if request.form.get(selectedTags[i]+"min"):
                    min = int(request.form.get(selectedTags[i]+"min"))
                    max = int(request.form.get(selectedTags[i]+"max"))
                    tagRange = []
                    for j in range(min, max+1, 1):
                        tagRange.append(j)
                    tabQ.append([selectedTags[i], tagRange])
                
            print("tabQ : ",tabQ)
            #tabQ contient pour chaque tag, toutes les valeurs de l'intervalle [min,max] (tabQ = [["java", [2,3,4,5]]["C", [5,6,7]])

            # On calcule toutes les combinaisons possibles respectant le nombre de question demandé
            allCombi = generateurS.combi(tabQ, 0, [], nbr_questions)
            print("allCombi : ",allCombi)
            # allCombi = [[1, 2], [2, 1]] 1 question avec tag A et 2 questions avec tag B puis inversement

            # On rajoute des infos pour savoir à quel tag correspond chaque quantité
            combiIdentifiees = []
            for i in range(len(allCombi)):
                combiCourante = []
                for j in range (len(allCombi[i])):
                    combiCourante.append([tabQ[j][0], allCombi[i][j]])
                combiIdentifiees.append(combiCourante)
            print("combinaisons Identifiées : ", combiIdentifiees)

            # On récupère l'id des questions portant chaque tag en supprimant les doublons (question portant 2 tags)
            questionByTag = generateurS.getQuestionByTag(tabQ)
            print("Question par tags : ", questionByTag)
            #questionByTagTrie = sorted(questionByTag, key=lambda tab : len(tab[1]))
            questionByTagTrie = questionByTag
            print("Question par tags triés : ", questionByTagTrie)
            quesParTagSansDoubl = generateurS.doublon(questionByTagTrie)
            print("Question par tags sans doublons : ", quesParTagSansDoubl)
            
            # On calcule le nombre de sujet que l'on fera avec chaque combinaisons et on voit si c'est possible
            combinaisonsRepartie = generateurS.repartirCombi(quesParTagSansDoubl, combiIdentifiees, nbr_sujets)
            print("Combinaisons Reparties : ", combinaisonsRepartie)
            if combinaisonsRepartie == None :
                flash("Vous ne pouvez pas faire suffisement de combinaisons avec les questions que vous possedez")
                return render_template("SujetsAImprimer.html", tabSujet = [], anonyme = False, title="")

            #on génère le bon nombre de sujet pour chaque combinaison
            for i in range(len(combinaisonsRepartie)):
                tabSujetID += (generateurS.generateurS(combinaisonsRepartie[i][0], combinaisonsRepartie[i][1], quesParTagSansDoubl))
            
            print("Sujet finaux (id) : ", tabSujetID)

        else :
            #On récupère le nb de questions demandé par tag
            #SANS ORDRE
            #for i in range(len(allTags)):
             #   if request.form.get(allTags[i]) != None:
              #      tabQ.append([allTags[i], int(request.form.get(allTags[i])) ])
            for i in range(len(selectedTags)):
                if request.form.get(selectedTags[i]) != None:
                    tabQ.append([selectedTags[i], int(request.form.get(selectedTags[i])) ])
            #REMETTRE DANS L ORDRE ICI
            #tabQ contient pour tout les tags, leur nombre souhaités (tabQ = [["java",5], ["c", 7]])
            print("AAAAAAAAAAAAAAAAAA tabQ", tabQ)
            # On récupère l'id des questions portant chaque tag en supprimant les doublons (question portant 2 tags)
            questionByTag = generateurS.getQuestionByTag(tabQ)
            print("############### QByTag : ", questionByTag)
            #questionByTagTrie = sorted(questionByTag, key=lambda tab : len(tab[1]))
            questionByTagTrie = questionByTag
            print("############### QBulle : ", questionByTagTrie)
            quesParTagSansDoubl = generateurS.doublon(questionByTagTrie)
            print("############### QSansDoub: ", quesParTagSansDoubl)

            #on calcule le nombre de sujets faisables avec nos questions pour voir si c'est possible
            nbSujetPossibles = generateurS.getNbSujetsPossibles(quesParTagSansDoubl, tabQ)
            if(nbSujetPossibles < nbr_sujets):
                flash("vous n'avez pas assez de questions différentes pour autant de sujets")
                return render_template("SujetsAImprimer.html", tabSujet = [], anonyme = False, title="")

            tabSujetID = generateurS.generateurS(tabQ, nbr_sujets, quesParTagSansDoubl)
            print("Sujet finaux (id) : ", tabSujetID)

    # On mélange les questions si demandé
    if mixage:
        tabSujetID = generateurS.mixage(tabSujetID)

    #on remplace les identifiants par leur questions respectives
    tabSujetQuestions = generateurS.IdToQuestion(tabSujetID)
    print("Sujets finaux (avec les questions) : ", tabSujetQuestions)
    return render_template("SujetsAImprimer.html", tabSujet = tabSujetQuestions, anonyme = anonymat, title=titre)