import fileIO
import os
from pathlib import Path

def loadTable():
    with open('./static/question.txt', 'r') as file:
        file = file.read()[:-1].split("\n\n\n")
        if file != ['']:
            for i in range(len(file)):
                file[i] = file[i].split("\n\n")
                proccessed = []
                for j in range(len(file[i])-2):
                    proccessed.append(file[i][j+2])
                file[i] = [file[i][0], file[i][1], proccessed]
            file[-1][1] = file[-1][1].replace("\n", '')
            
        else:
            file = []
        return file
def saveTable(data):
    with open('./static/question.txt', 'w') as file:
        out = ""
        for couple in data:
            proccessed = [couple[0],couple[1]]
            for item in couple[2]:
                proccessed.append(item)
            for item in proccessed:
                out+= item + "\n\n"
            out=out[:-2]
            out+="\n\n\n"
        out = out[:-3]
        print(out, file=file)
def saveQuestion(questionID, title, question, answer, correctAnswer):
    os.mkdir('./static/questions/'+str(questionID))
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
def read(questionID):
    out = []
    if (Path('./static/questions/'+str(questionID)).is_dir()):
        numRep = len(os.listdir('./static/questions/'+str(questionID)+'/'))-2
        ans = []
        for i in range(numRep):
            with open('./static/questions/'+str(questionID)+'/'+str(i)+'.txt', 'r') as file:
                ans.append(file.read())
        with open('./static/questions/'+str(questionID)+'/question.txt', 'r') as file:
            with open('./static/questions/'+str(questionID)+'/tittle+answer.txt', 'r') as tA:    
                tittleAnswer = tA.read().split('\n\n')
                out = [file.read(), tittleAnswer[0], ans, tittleAnswer[1:]]
    return out
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
