from database import loadQuestionsByProfTag, getProfIdentity, loadQuestionById
from flask import session
from random import random
from math import comb
from math import ceil

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





def getQuestionByTag(E=[[], int]):
    tab = []
    idP = session['loginP']
    for i in range (len(E)):
         tab.append([E[i][1]]) #ajout tag
         tab[i].append(loadQuestionsByProfTag(idP,E[i][1])) #ajout idQ en fonctino des tags
         #requête BDD pour chaque tag E[i][1]
    #trier les tabs de manière croissante en fonction de leur nb de questions
    #tab = [["java",[1,2,3]],["C",[3,4]],["Meynard",[4,5,6,7,8]]]
    #tri bulles

    #Suppression doublon
    #On donne le doublon à la liste qui a le moins de question
    return tab
#print(tagMultiples([[3,"java"],[2,"compilation"]]))

def conversion(E):
    dico = {}
    for i in range (len(E)):
        dico[E[i][0]]=(E[i][1])
    return dico

def conversion2(E):
    dico = {}
    for i in range (len(E)):
        dico[E[i][1]]=(E[i][0])
    return dico


def generateurS(E ,nbSujet, questionsSansDoublons): #E=[[], int] mais ptetre plus mtn
    #E est un tableau, contenant des sous de tableau de la forme [nbQuestionSouhaité,"Tag"]
    #E = [[2,"Java"],[3,"Compilation"],[6,"PHP"]]

    #BIENTOT On récupère pour chaque tag leur nombre de question
    #print("E",E)
        #tab = getQuestionByTag(E)
    #print("tab1",tab)
        #tab = triBulles(tab)
    #print("tab2",tab)

        #tab = doublon(tab)
    #print("tab3",tab)

    dicoQ = conversion(questionsSansDoublons)

    #for a in range(len(E)):
        #res = requete BDD tag E[a][1]
        #dicoQ[E[a][1]].append(res)
    #dicoQ = {
     #   "java" : ["J1","J2","J3","J4"],
      #  "compilation" : ["C1","C2","C3","C4","C5","C6"]
    #}

    print(dicoQ)
    #nbSuj = nombre d esujet voulu
    pas = 1
    tabSujet = []
    for j in range(nbSujet):
            tabSujet.append([])

    #METHODE :
    #Pour chaque tag on regarde combien il faut faire de question
    #Et pour chaque question on fait nbSujet tour de boucle

    #Pour chaque tag
    for j in range(len(E)):
        #Pour chaque question dans 1 tag
        #E[j][0] = nb de Question pour un tag (premier tour de boucle c'est 2 car [2,"Java"] )

        for k in range(E[j][0]):
            #pour chaque sujet
            #On évite que le pas soit un multiple sinon on retourne sur les mêmes valeurs 

            #Si nbQ pair alors pas doit être impair
            #Si nbQ impair alors pas doit être tout sauf multipe de nbQ et inversement

            while (( (len(dicoQ[E[j][1]])%2 == 0 and pas%2 == 0) or ((len(dicoQ[E[j][1]]))%2 != 0 and (pas%len(dicoQ[E[j][1]]) == 0))or (len(dicoQ[E[j][1]])%pas == 0)) and len(dicoQ[E[j][1]]) != 1):
                pas += 1
            l = k
            for compteur in range (nbSujet):             
                tabSujet[compteur].append(dicoQ[E[j][1]][l])
                l = (l+pas)%len(dicoQ[E[j][1]])
        pas += 1
    return tabSujet

#Mixe si mixe == True
def mixage(tabSujet):
    #Mélange les questions de chaque sujet
    for i in range(len(tabSujet)):
        random.shuffle(tabSujet[i])
    return tabSujet

#fonction possInter qui calcule les différents intervalles de questions possibles
def combi(tableaux, sum, combination, target_sum):
    combinations = []
    # Si la somme de la combinaison actuelle est celle qu'on veut et qu'on a utilisé chaque tableau
    if sum == target_sum and len(tableaux) == 0:
        combinations.append(combination)
    # Sinon faut rajouter des questions
    elif sum < target_sum:
        if len(tableaux) == 0:
            return []
        else:
            # Pour chaque élément du premier tableau
            for element in tableaux[0]:
                # on ajoute l'élément actuel à la combinaison
                new_combination = combination + [element]
                # puis on ajoute la valeur de l'élément actuel à la somme
                new_sum = sum + element
                # appel récurisf pour les tableaux restants,
                combinations += combi(tableaux[1:], new_sum, new_combination, target_sum)
    return combinations

def IdToQuestion(tabQ):
    for i in range(len(tabQ)):
        for j in range(len(tabQ[i])):
            tabQ[i][j] = loadQuestionById(tabQ[i][j])
    return tabQ

def getNbSujetsPossibles(tabQuestions, nbQuestionVouluParTag):
    total = 1
    dicoNbQ = conversion2(nbQuestionVouluParTag)
    for tag in tabQuestions:
        total *= comb(len(tag[1]), dicoNbQ[tag[0]])
    return total

def repartirCombi(tabQuestions, tabCombinaisons, nbSujetsVoulu):
    nbSujetParCombi = [] #un tableau de tableaux à deux entré : [une combinaison, le nombre de sujets possibles avec]
    nbSujetTotal = 0
    for combi in tabCombinaisons:
        nbPossible = getNbSujetsPossibles(tabQuestions, combi)
        nbSujetTotal += nbPossible
        if nbPossible > 0:
            nbSujetParCombi.append([combi, nbPossible])

    print("######## nbSujetTotalPossible : ", nbSujetTotal, " / ", nbSujetsVoulu)
    print("######## combis : ", nbSujetParCombi)
    if nbSujetTotal < nbSujetsVoulu :
        return None

    nbSujetParCombi.sort(key=lambda combi: combi[1]) #on tri par nombre de sujets possibles
    print("######## combis triés : ", nbSujetParCombi)

    nbSujetRestants = nbSujetsVoulu
    nbCombiRestantes = len(nbSujetParCombi)
    for combi in nbSujetParCombi:
        print("#####################")
        moy = ceil(nbSujetRestants / nbCombiRestantes)
        print(nbSujetRestants)
        print(moy)
        print(combi[1])
        if combi[1] <= moy :
            nbSujetRestants -= combi[1]
        else:
            nbSujetRestants -= moy
            combi[1] = moy
        nbCombiRestantes -= 1

    return nbSujetParCombi

