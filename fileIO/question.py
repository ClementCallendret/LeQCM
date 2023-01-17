import fileIO
import os
from pathlib import Path

### edit both to manage tags
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


def saveQuestion(questionID, question, answer):
    os.mkdir('./static/questions/'+str(questionID))
    with open('./static/questions/'+str(questionID)+'/question.txt', 'w') as out:
        out.write(question)
    for i in range(len(answer)):
        with open('./static/questions/'+str(questionID)+'/'+str(i)+'.txt', 'w') as out:
            out.write(answer[i])



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





def newQuestion(account, question, answer, tag):
    listOfId = os.listdir("./static/questions")
    tableId = fileIO.question.loadTable()
    if listOfId == ['']:
        tableId.append([account, str(len(listOfId)), tag])
        fileIO.question.saveQuestion(len(listOfId), question, answer)
    else:
        written = False
        for i in range(1, len(listOfId)):
            if listOfId[i] != int(listOfId[i-1])-1:
                tableId.append([account, str(i-1), tag])
                fileIO.question.saveQuestion(i-1, question, answer)
                written = True
        if not(written):
            tableId.append([account, str(len(listOfId)), tag])
            fileIO.question.saveQuestion(len(listOfId), question, answer)
            written = True
    fileIO.question.saveTable(tableId)