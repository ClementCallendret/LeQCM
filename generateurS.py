from database import loadQuestionsByProfTag, getProfIdentity, loadQuestionById
from flask import session
from random import random
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
    print("tab", tab)
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
    print("TABLEAU ",tab)
    #trier les tabs de manière croissante en fonction de leur nb de questions
    #tab = [["java",[1,2,3]],["C",[3,4]],["Meynard",[4,5,6,7,8]]]
    #tri bulles
    print("triBulles Res", tab)

    #Suppression doublon
    #On donne le doublon à la liste qui a le moins de question
    return tab
#print(tagMultiples([[3,"java"],[2,"compilation"]]))

def conversion(E):
    dico = {}
    for i in range (len(E)):
        dico[E[i][0]]=(E[i][1])
    return dico


def generateurS(E=[[], int],nbSujet = int):
    #E est un tableau, contenant des sous de tableau de la forme [nbQuestionSouhaité,"Tag"]
    #E = [[2,"Java"],[3,"Compilation"],[6,"PHP"]]

    #BIENTOT On récupère pour chaque tag leur nombre de question
    print("E",E)
    tab = getQuestionByTag(E)
    print("tab1",tab)
    tab = triBulles(tab)
    print("tab2",tab)

    tab = doublon(tab)
    print("tab3",tab)

    dicoQ = conversion(tab)
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
            #pour chaque sujet
            #On évite que le pas soit un multiple sinon on retourne sur les mêmes valeurs 

            #Si nbQ pair alors pas doit être impair
            #Si nbQ impair alors pas doit être tout sauf multipe de nbQ et inversement
            print("dicoQ", dicoQ)
            print("len(dicoQ[E[j][1]",len(dicoQ[E[j][1]]))
            print("pas", pas)

            while ( (len(dicoQ[E[j][1]])%2 == 0 and pas%2 == 0) or ((len(dicoQ[E[j][1]]))%2 != 0 and (pas%len(dicoQ[E[j][1]]) == 0))or (len(dicoQ[E[j][1]])%pas == 0)):
                pas += 1
            l = k
            for compteur in range (nbSujet):             
                tabSujet[compteur].append(dicoQ[E[j][1]][l])
                l = (l+pas)%len(dicoQ[E[j][1]])
        pas += 1
    print("TABSUJET",tabSujet)
    return tabSujet

#Mixe si mixe == True
def mixage(tabSujet):
    #Mélange les questions de chaque sujet
    for i in range(len(tabSujet)):
        random.shuffle(tabSujet[i])
    return tabSujet

#fonction possInter qui calcule les différents intervalles de questions possibles
def possInter(tab, current_sum, current_combination, target_sum):
    # Si la somme de la combinaison actuelle est égale à la somme cible
    if current_sum == target_sum:
        print(current_combination)
    # Si la somme de la combinaison actuelle est inférieure à la somme cible
    elif current_sum < target_sum:
        # Si tous les tableaux ont été explorés
        if len(tab) == 0:
            return
        else:
            # Pour chaque élément du premier tableau
            for element in tab[0]:
                # Ajouter l'élément actuel à la combinaison
                new_combination = current_combination + [element]
                # Ajouter la valeur de l'élément actuel à la somme
                new_sum = current_sum + element
                # Appeler récursivement la fonction en utilisant les tableaux restants,
                # la nouvelle somme et la nouvelle combinaison
                possInter(tab[1:], new_sum, new_combination, target_sum)

def IdToQuestion(tabQ):
    for i in range(len(tabQ)):
        for j in range(len(tabQ[1])):
            tabQ[i][1][j] = loadQuestionById(tabQ[i][1][j])
    return tabQ