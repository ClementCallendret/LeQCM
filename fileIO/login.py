import fileIO
def create(account, password):
    exist=False
    data = fileIO.common.load()
    for couple in data[0]:
        if couple[0]==account:
            exist = True
            print('account already exists')
    if not(exist):
        if data[0]=='':
            data[0] = []
        data[0].append([account, password])
        fileIO.common.save(data)
