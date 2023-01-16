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
            file[-1][1] = file[-1][1].replace("\n", '')
        else:
            file = []
        return file



def save(data):
    with open('./static/question.txt', 'w') as file:
        out = ""
        for couple in data:
            for item in couple:
                out+= item + "\n\n"
            out=out[:-2]
            out+="\n\n\n"
        out = out[:-3]
        print(out, file=file)





def newQuestion(account, question, tag):
    listOfId = os.listdir("./static/questions")
    tableId = fileIO.question.loadTable()
    if listOfId == ['']:
        os.mkdir("./static/questions/1")
    else:
        for i in range(len(listOfId)):
            if listOfId[i] != listOfId[i-1]-1:
                os.mkdir("./static/questions/"+str(i-1))
                tableId.append([account, str(i-1), tag])
        


