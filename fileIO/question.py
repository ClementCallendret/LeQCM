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
        formated = [correctAnswer]
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
        # on charge l'énoncé, le titre, et les réponses possibles
        with open('./static/questions/'+str(questionID)+'/question.txt', 'r') as file:
            with open('./static/questions/'+str(questionID)+'/tittle+answer.txt', 'r') as tA:    
                # si on split notre fichier titre + réponses, on sais que le premiers élément et le titre, le reste, une liste de réponses corrèctes
                tittleAnswer = tA.read().split('\n\n')
                # on assemble tout ce qu'on a récupéré
                out = [file.read(), tittleAnswer[0], ans, tittleAnswer[1:]]
    # on retourne le résultat
    return out

# pour créer une question

def newQuestion(account, title, question, answer, tag, correctAnswer):
    listOfId = os.listdir("./static/questions")
    listOfId.sort()
    tableId = fileIO.question.loadTable()
    if listOfId == []:
        tableId.append([account, str(len(listOfId)), tag])
        fileIO.question.saveQuestion(len(listOfId), title, question, answer, correctAnswer)
    elif listOfId[0] != '0':
        tableId.append([account, '0', tag])
        fileIO.question.saveQuestion('0', title, question, answer, correctAnswer)
    else:
        written = False
        for i in range(1, len(listOfId)):
            if int(listOfId[i]) != int(listOfId[i-1])+1:
                tableId.append([account, str(i), tag])
                fileIO.question.saveQuestion(i, title, question, answer, correctAnswer)
                written = True
        if not(written):
            tableId.append([account, str(len(listOfId)), tag])
            fileIO.question.saveQuestion(len(listOfId), title, question, answer, correctAnswer)
            written = True
    fileIO.question.saveTable(tableId)
def remove(questionID):
    for file in os.listdir('./static/questions/'+str(questionID)):
        os.remove('./static/questions/'+str(questionID)+'/'+(file))
    os.rmdir('./static/questions/'+str(questionID)+'/')
    tableID = fileIO.question.loadTable()
    newTable = []
    for item in tableID:
        if item[1] != questionID:
            newTable.append(item)
    fileIO.question.saveTable(newTable)
def listByAccount(account):
    table = fileIO.question.loadTable()
    out = []
    for item in table:
        if item[0] == account:
            out.append(item[1])
    return out
def listByTag(tag):
    table = fileIO.question.loadTable()
    out = []
    for item in table:
        if tag in item[2]:
            out.append(item[1])
    return out
def listByTags(tags):
    bundle = []
    for tag in tags:
        bundle.append(fileIO.question.listByTag(tag))
    out = []
    for list in bundle:
        for item in list:
            inAll=True
            for oList in bundle:
                if not(item in oList):
                    inAll=False
            if inAll and not(item in out):
                out.append(item)
    return out
def listByAccountAndTags(account, tags):
    bundle = fileIO.question.listByTag(tags)
    temp = fileIO.question.listByAccount(account)
    for elem in temp:
        bundle.append(elem)
    out=[]
    for list in bundle:
        for item in list:
            inAll=True
            for oList in bundle:
                if not(item in oList):
                    inAll=False
            if inAll and not(item in out):
                out.append(item)
    return out
def update(questionID, title, question, answer, tags, correctAnswer):
    with open('./static/questions/'+str(questionID)+'/question.txt', 'w') as out:
        out.write(question)
    for i in range(len(answer)):
        with open('./static/questions/'+str(questionID)+'/'+str(i)+'.txt', 'w') as out:
            out.write(answer[i])
    with open('./static/questions/'+str(questionID)+'/tittle+answer.txt', 'w') as out:
        formated = [title, correctAnswer]
        strOut = ""
        for item in formated:
            strOut+=str(item)+"\n\n"
        strOut=strOut[:-2]
        out.write(strOut)
    table = fileIO.question.loadTable()
    for line in table:
        if line[1] == questionID:
            line[2] == tags
    fileIO.question.saveTable(table)
def isCorrect(questionID, answersToCheck):
    questionData = fileIO.question.read(questionID)
    return answersToCheck.sort() == questionData[3].sort()
