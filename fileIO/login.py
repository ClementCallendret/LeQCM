import fileIO
def create(account, password):
    exist=False
    data = fileIO.common.load()
    for couple in data:
        if couple[0]==account:
            exist = True
            print('account already exists')
    if not(exist):
        if data=='':
            data = []
        data.append([account, password])
        fileIO.common.save(data)

def check(account, password):
    out=False
    data = fileIO.common.load()
    for couple in data:
        if couple==[account, password]:
            out = True
    return out