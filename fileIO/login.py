import fileIO
def create(account, password):
    exist=False
    data = fileIO.login.load()
    for couple in data:
        if couple[0]==account:
            exist = True
            print('account already exists')
    if not(exist):
        if data=='':
            data = []
        data.append([account, password])
        fileIO.login.save(data)

def check(account, password):
    out=False
    data = fileIO.login.load()
    for couple in data:
        if couple==[account, password]:
            out = True
    return out
def remove(account):
    data = fileIO.login.load()
    newData=[]
    for couple in data:
        if couple[0]!=account:
            newData.append(couple)
    fileIO.login.save(newData)
    for item in fileIO.question.listByAccount("e"):
        fileIO.question.remove(item)
def load():
    with open('./static/login.txt', 'r') as file:
        file = file.read()[:-1].split("\n\n\n")
        if file != ['']:
            for i in range(len(file)):
                file[i] = file[i].split("\n\n")
            file[-1][1] = file[-1][1].replace("\n", '')
        else:
            file = []
        return file

def save(data):
    with open('./static/login.txt', 'w') as file:
        out = ""
        for couple in data:
            for item in couple:
                out+= item + "\n\n"
            out=out[:-2]
            out+="\n\n\n"
        out = out[:-3]
        print(out, file=file)

