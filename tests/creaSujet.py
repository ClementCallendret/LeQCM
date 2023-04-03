def creaSujet(E,nbSuj):
    #E est un tableau, contenant des sous de tableau de la forme [nbQuestionSouhaité,"Tag"]
    #E = [[2,"Java"],[3,"Compilation"],[6,"PHP"]]

    #nbSuj = nombre d esujet voulu
    #GROUPER LES 3 PREMIERS BOUCLES


    #BIENTOT On récupère pour chaque tag leur nombre de question
    dicoQ = {}
    #for a in range(len(E)):
        #res = requete BDD tag E[a][1]
        #dicoQ[E[a][1]].append(res)
    dicoQ = {
        "java" : [1,2,3,4],
        "compilation" : [5,6,7,8,9,10]
    }

    #On récupère le maximum de question de chaque tag
    tabMax=[]
    for b in range (len(E)):
        tabMax.append(len(dicoQ[E[b][1]]))

    print ("TAB MAX", tabMax)
    #INDICE POUR VERIF LE MAX
    tabEnCours = []
    #TAB QU ON VA RETURN AVEC TOUT LES SUJETS
    tabSujet = []
    #TAB POUR LE SUJET EN COURS
    tabSujetEnCours = []
    for c in range (len(E)):
        tabEnCours.append(0)

    print("TAB EN COURS", tabEnCours)
    #Boucle pour chaque sujet
    for i in range (nbSuj):
        print("NOUVEAU SUJET")
        #Verif Max pour chaque Tag
        for j in range(len(E)-1,-1,-1):
            #Si ça va être = au max
            print("tab en cours",tabEnCours[j]+E[j][0])
            print("tab max",tabMax[j])
            if tabEnCours[j]+E[j][0] > tabMax[j] :
                #On incrémente le prochain
                print("FAIT LE IF", j)

                tabEnCours[j-1] += 1 
                print("TAB EN COURS UPDATE", tabEnCours)
                for k in range(j, len(tabEnCours)):
                    print("k",k)
                    tabEnCours[k] = 0

        print("TAB EN Cours ",tabEnCours)
        #BOUCLE POUR CHAQUE TAG
        for l in range(len(E)):
            #BOUCLE POUR CHAQUE QUESTION
            for m in range(tabEnCours[l],E[l][0]+tabEnCours[l]):

                tabSujetEnCours.append(dicoQ[E[l][1]][m])
        tabSujet.append(tabSujetEnCours)
        print("\n TAB SUJET EN COURS ",tabSujetEnCours)
        tabSujetEnCours = []
        tabEnCours[len(tabEnCours)-1] += 1

    return tabSujet

print(creaSujet([[3,"java"],[2,"compilation"]], 13))