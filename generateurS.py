from database import loadQuestionsByProfTag, getProfIdentity
from flask import session
def generateurS(E=[[], int],nbSujet = int):
    #E est un tableau, contenant des sous de tableau de la forme [nbQuestionSouhaité,"Tag"]
    #E = [[2,"Java"],[3,"Compilation"],[6,"PHP"]]

    #BIENTOT On récupère pour chaque tag leur nombre de question
    dicoQ = {}
    #for a in range(len(E)):
        #res = requete BDD tag E[a][1]
        #dicoQ[E[a][1]].append(res)
    dicoQ = {
        "java" : ["J1","J2","J3","J4"],
        "compilation" : ["C1","C2","C3","C4","C5","C6"]
    }


    #nbSuj = nombre d esujet voulu
    pas = 1
    tabSujet = []
    for j in range(nbSujet):
            tabSujet.append([])
    print(tabSujet)

    #METHODE :
    #Pour chaque tag on regarde combien il faut faire de question
    #Et pour chaque question on fait nbSujet tour de boucle

    #Pour chaque tag
    for j in range(len(E)):
        print("J =",j)
        #Pour chaque question dans 1 tag
        #E[j][0] = nb de Question pour un tag (premier tour de boucle c'est 2 car [2,"Java"] )

        for k in range(E[j][0]):
            print("K =",k)
            #pour chaque suejt
            #On évite que le pas soit un multiple sinon on retourne sur les mêmes valeurs 

            #Si nbQ pair alors pas doit être impair
            #Si nbQ impair alors pas doit être tout sauf multipe de nbQ et inversement
            while ((len(dicoQ[E[j][1]]))%2 == 0 and pas%2 == 0) or ((len(dicoQ[E[j][1]]))%2 != 0 and (pas%(len(dicoQ[E[j][1]]) == 0))or (len(dicoQ[E[j][1]])%pas == 0)):
                pas += 1
            l = k
            for compteur in range (nbSujet):             
                tabSujet[compteur].append(dicoQ[E[j][1]][l])
                l = (l+pas)%len(dicoQ[E[j][1]])
        pas += 1

    return tabSujet

def doublon(tab):
    for i in range (len(tab)):
        j = 0
        longueur1 = len(tab[i][1])
        while j < longueur1 :
        #for j in range(len(tab[i][1])): mais soustraction j et longueur1

            for k in range(i+1,len(tab),1):
                l = 0
                longueur2 = len(tab[k][1])
                while l < longueur2:
                #for l in range(len(tab[k][1])): mais soustraction l et longueur2
                    if (tab[i][1][j]) == (tab[k][1][l]):
                        if (len(tab[i][1]) > len(tab[k][1])):
                            tab[i][1].pop(j)
                            j -= 1
                            longueur1 -= 1
                        else :
                            tab[k][1].pop(l)
                            l -= 1
                            longueur2 -= 1
                    l += 1
            j += 1
    return tab
#print(generateurS([[3,"java"],[2,"compilation"]],30))
def triBulles(tab):
    for i in range (len(tab)):
         for j in range (len(tab)-i-1):
              if len(tab[j][1]) > len(tab[j+1][1]):
                   tab[j], tab[j+1] = tab[j+1], tab[i]
    return tab

def tagMultiples(E=[[], int]):
    tab = []
    idP = getProfIdentity(session['loginP'])
    for i in range (len(E)):
         tab.append(loadQuestionsByProfTag(idP,E[i][0]))
         #requête BDD pour chaque tag E[i][1]
    print(tab)
    #trier les tabs de manière croissante en fonction de leur nb de questions
    #tab = [["java",[1,2,3]],["C",[3,4]],["Meynard",[4,5,6,7,8]]]
    #tri bulles
    tab = triBulles(tab)
    print("tri", tab)
    tab = doublon(tab)

    #Suppression doublon
    #On donne le doublon à la liste qui a le moins de question
    return tab

#print(tagMultiples([[3,"java"],[2,"compilation"]]))