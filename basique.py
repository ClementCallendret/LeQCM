def basique(E,nbSuj):
    #E est un tableau, contenant des sous de tableau de la forme [nbQuestionSouhaité,"Tag"]
    #E = [[2,"Java"],[3,"Compilation"],[6,"PHP"]]

    #nbSuj = nombre d esujet voulu
    #GROUPER LES 3 PREMIERS BOUCLES


    #BIENTOT On récupère pour chaque tag leur nombre de question
    #dicoQ = {}
    #for a in range(len(E)):
        #res = requete BDD tag E[a][1]
        #dicoQ[E[a][1]].append(res)

    #On récupère le maximum de question de chaque tag
    tabMax=[]
    #for b in range (len(E)):
    #    tabMax.append(len(dicoQ[E[b]]))
    #INDICE POUR VERIF LE MAX
    tabEnCours = []
    #TAB QU ON VA RETURN AVEC TOUT LES SUJETS
    tabSujet = []
    #TAB POUR LE SUJET EN COURS
    tabSujetEnCours = []
    for c in (len(E)):
        tabEnCours.append(0)

    #Boucle pour chaque sujet
    for i in range (nbSuj):
        #Verif Max pour chaque Tag
        for j in range(len(E),0):
            #Si ça va être = au max
            if tabEnCours[j]+E[j] > tabMax[j] :
                #On incrémente le prochain
                tabEnCours[j+1] += 1 
                for k in range(len(E),j):
                    tabEnCours[i] = 0
        #BOUCLE POUR CHAQUE TAG
        for l in range(len(E)):
            #BOUCLE POUR CHAQUE QUESTION
            for m in range(E[l][0]):
                tabSujetEnCours.append(dicoQ[E[l][1]][m])
        tabSujet.append(tabSujetEnCours)