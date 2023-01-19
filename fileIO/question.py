import fileIO
import os
from pathlib import Path

"""
fonctions de chargements / sauvegardes de données
"""



# on charge le sommaire (qui contient des triplets de la forme(createur, idDeQuestion, [tag])), pour pas avoir a charger en ram tout les énoncés(+10000 ça plante)

def loadTable():
    # on ouvre le fichier sommaire
    with open('./static/question.txt', 'r') as file:
        # on fait un premier split pour séparer les lignes(et on vire le \n de fin que python met toujours)
        file = file.read()[:-1].split("\n\n\n")
        # si le fichier est pas vide
        if file != ['']:
            # on parcourt chaque lignes
            for i in range(len(file)):
                # on coupe la ou ya le séparateur pour avoir au final une liste de lignes(et chaque lignes et une liste de cases(qui sont des strings))
                file[i] = file[i].split("\n\n")
                # ici on va mettre tout les tag dans une liste(plus propre pour d'autres implémentations)
                proccessed = []
                # on parcourt toute les cases de chaques lignes(sauf les deux premieres(createur et id))
                for j in range(len(file[i])-2):
                    # on met toutes ces cases dans une liste
                    proccessed.append(file[i][j+2])
                # on réécrit la ligne avec [createur, id , [nouvelle liste de tags]]
                file[i] = [file[i][0], file[i][1], proccessed]
            # on vire le \n a la fin (encore?)
            file[-1][1] = file[-1][1].replace("\n", '')
        # si la liste était vide
        else:
            # on veut une liste vide pas une liste d'une string vide
            file = []
        # on retourne les données
        return file

# sauvegarde le sommaire dans un fichier en l'encodant

def saveTable(data):
    # on ouvre le fichier sommaire
    with open('./static/question.txt', 'w') as file:
        # on initialise notre future sortie
        out = ""
        # on parcourt les triplets itérativement
        for triplet in data:
            # la on prepare au décompactage de nos tags, il faut que notre ligne sois une liste de strings, pas une liste [string, string, [string, ...]]
            proccessed = [triplet[0],triplet[1]]
            # on prend les listes de tags
            for item in triplet[2]:
                # qu'on ajoute a notre première liste, qui ne contient plus de tag
                proccessed.append(item)
            # on encode cette ligne en séparant chaque éléments par \n\n
            for item in proccessed:
                out+= item + "\n\n"
            # les deux derniers retours sont en trop
            out=out[:-2]
            # on sépare les lignes entre elles par \n\n\n
            out+="\n\n\n"
        # dernière séparation en trop
        out = out[:-3]
        # on écrit le résultat encodé
        print(out, file=file)

# on sauvegarde une question

def saveQuestion(questionID, title, question, answer, correctAnswer):
    # on crée un dossier avec l'identifiant fournit en nom
    os.mkdir('./static/questions/'+str(questionID))
    # on crée un fichier dans ce dossier qui contiendra l'énoncé
    with open('./static/questions/'+str(questionID)+'/question.txt', 'w') as out:
        out.write(question)
    # pour chaques réponses, on crée un fichier avec un numéro, qui contiendront chaques réponses séparément
    for i in range(len(answer)):
        with open('./static/questions/'+str(questionID)+'/'+str(i)+'.txt', 'w') as out:
            out.write(answer[i])
    # on crée un fichier contenant le titre et les réponses possibles
    with open('./static/questions/'+str(questionID)+'/tittle+answer.txt', 'w') as out:
        # faut décompacter les reponses correctes
        formated = correctAnswer
        strOut = ""
        for item in formated:
            strOut+=str(item)+"\n\n"
        strOut=strOut[:-2]
        # ensuite on assemble le tout en une string qu'on ecrit
        out.write(title+"\n\n"+strOut)

"""

manipulations :

"""


# pour charger une question

def read(questionID):
    # on crée une liste qui contient les tout de la question
    out = []
    # si elle existe
    if (Path('./static/questions/'+str(questionID)).is_dir()):
        # on compte le nombre de réponses
        numRep = len(os.listdir('./static/questions/'+str(questionID)+'/'))-2
        ans = []
        # on les stocke dans une liste
        for i in range(numRep):
            with open('./static/questions/'+str(questionID)+'/'+str(i)+'.txt', 'r') as file:
                ans.append(file.read())
        # on recupère ses tags et le créateur:
        tableID = fileIO.question.loadTable()
        tags = []
        owner = ""
        for item in tableID:
            if item[1] == questionID:
                tags = item[2]
                owner = item[0]
        # on charge l'énoncé, le titre, et les réponses possibles
        with open('./static/questions/'+str(questionID)+'/question.txt', 'r') as file:
            with open('./static/questions/'+str(questionID)+'/tittle+answer.txt', 'r') as tA:    
                # si on split notre fichier titre + réponses, on sais que le premiers élément et le titre, le reste, une liste de réponses corrèctes
                tittleAnswer = tA.read().split('\n\n')
                # on assemble tout ce qu'on a récupéré
                out = [questionID, owner, file.read(), tittleAnswer[0], tags, ans, tittleAnswer[1:]]
    # on retourne le résultat
    return out

# pour créer une question

def newQuestion(account, title, question, answer, tag, correctAnswer):
    # on liste les questions existantes
    listOfId = os.listdir("./static/questions")
    # on trie cettee liste par ordre croissant
    listOfId.sort()
    # on charge le sommaire
    tableId = fileIO.question.loadTable()
    # si il n'y a aucunes questions deja enregistrée
    if listOfId == []:
        # on crée la question '0'(màj du sommaire puis sauvegarde)
        tableId.append([account, str(len(listOfId)), tag])
        fileIO.question.saveQuestion(len(listOfId), title, question, answer, correctAnswer)
    # si il n'y a pas de question '0' (si elle a été supprimée mais qu'il y en a d'autres)
    elif listOfId[0] != '0':
        # on crée la question '0'(màj du sommaire puis sauvegarde)
        tableId.append([account, '0', tag])
        fileIO.question.saveQuestion('0', title, question, answer, correctAnswer)
    else:
        # dans tout les autres cas:
        # on initialise un bool
        written = False
        # on parcourt la liste des questions existantes(fichier)
        for i in range(1, len(listOfId)):
            # si lid de deux question succéssive a un écart de plus de 1 (un trou):
            if int(listOfId[i]) != int(listOfId[i-1])+1:
                # on crée la question dans le trou et on dit qu'on la écrit (le bool)
                tableId.append([account, str(i), tag])
                fileIO.question.saveQuestion(i, title, question, answer, correctAnswer)
                written = True
        # si on a pas écrit la question(pas de trou)
        if not(written):
            # on crée la question avec pour id celui du plus grand+1
            tableId.append([account, str(len(listOfId)), tag])
            fileIO.question.saveQuestion(len(listOfId), title, question, answer, correctAnswer)
    # on sauvergarde le sommaire mis a jour
    fileIO.question.saveTable(tableId)

# pour supprimer une question

def remove(questionID):
    # on parcourt tout les fichiers dans le dossier pourtant l'id de ce qu'on supprime
    for file in os.listdir('./static/questions/'+str(questionID)):
        # on supprime ce qu'on trouve
        os.remove('./static/questions/'+str(questionID)+'/'+(file))
    # on supprime le dossier avec l'id de la question(vide maintenant)
    os.rmdir('./static/questions/'+str(questionID)+'/')
    # on charge le sommaire
    tableID = fileIO.question.loadTable()
    # on le met a jour en gardant toute les lignes qui n'ont pas l'id de la question a supprimer
    newTable = []
    for item in tableID:
        if item[1] != questionID:
            newTable.append(item)
    # on ecrit le sommaire màj dans son fichier
    fileIO.question.saveTable(newTable)

# recherche de l'ensemble des ID de questions avec comme créateur un compte

def listByAccount(account):
    # on charge le sommaire
    table = fileIO.question.loadTable()
    out = []
    # on ecrit dans out tout les id dans les lignes avec le login qu'on veut
    for item in table:
        if item[0] == account:
            out.append(item[1])
    # on retourne la liste
    return out

# pour chercher l'ensemble des ID de questions avec comme tag celui qu'on a

def listByTag(tag):
    # on charge le sommaire
    table = fileIO.question.loadTable()
    # on note dans une liste l'id de question de chaque ligne contenant le tag
    out = []
    for item in table:
        if tag in item[2]:
            out.append(item[1])
    # on retourne cette liste
    return out

# pour rechercher avec plusieurs tags 

def listByTags(tags):
    # on fait une liste avec les listes de resultats de recherche pour chaque tag
    bundle = []
    for tag in tags:
        bundle.append(fileIO.question.listByTag(tag))
    # on fait l'intersection de chaque listes( en gardant que les id qui sont dans chaques listes)
    out = []
    for list in bundle:
        for item in list:
            inAll=True
            for oList in bundle:
                if not(item in oList):
                    inAll=False
            if inAll and not(item in out):
                out.append(item)
    # on retourne le resultat
    return out

# pour chercher avec plusieurs tags et un compte

def listByAccountAndTags(account, tags):
    # on fait pareil que pour plusieurs tags, mais on ajoute dans notre liste de listes de resultat le resultat d'une recherche par compte
    bundle = fileIO.question.listByTag(tags)
    temp = fileIO.question.listByAccount(account)
    for elem in temp:
        bundle.append(elem)
    # on fait l'intersections
    out=[]
    for list in bundle:
        for item in list:
            inAll=True
            for oList in bundle:
                if not(item in oList):
                    inAll=False
            if inAll and not(item in out):
                out.append(item)
    # on retourne le resultat
    return out

# pour mettre a jour une question

def update(questionID, title, question, answer, tags, correctAnswer):
    # on met a jour l'enoncé
    with open('./static/questions/'+str(questionID)+'/question.txt', 'w') as out:
        out.write(question)
    # on met a jour les réponses 
    for i in range(len(answer)):
        with open('./static/questions/'+str(questionID)+'/'+str(i)+'.txt', 'w') as out:
            out.write(answer[i])
    # on met a jour le titre et les reponses posibles
    with open('./static/questions/'+str(questionID)+'/tittle+answer.txt', 'w') as out:
        formated = [title, correctAnswer]
        strOut = ""
        for item in formated:
            strOut+=str(item)+"\n\n"
        strOut=strOut[:-2]
        out.write(strOut)
    # on met a jour le sommaire(le créateur ne peut pas etre changé !)
    table = fileIO.question.loadTable()
    for line in table:
        if line[1] == questionID:
            line[2] == tags
    # on sauvegarde la table màj
    fileIO.question.saveTable(table)

# pour regarder si les réponses correspondent a ce qui est attendu

def isCorrect(questionID, answersToCheck):
    # on charge les données d'une question
    questionData = fileIO.question.read(questionID)
    # si les reponses fournies sont les mêmes que celles sauvergardées alors True sinon False
    return answersToCheck.sort() == questionData[6].sort()

def getAllTags():
    table = fileIO.question.loadTable()
    out = []
    for item in table:
        for tag in item[2]:
            if not(tag in out):
                out.append(tag)
    return out