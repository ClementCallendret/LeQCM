import fileIO

def dicToQuestion(dic):
    reponses = fileIO.format.listOfDicToreponse(dic['reponses'])
    return [dic['id'], dic['owner'],dic['title'], dic['enonce'], dic['tag'], reponses[0], reponses[1]]


def questionToDic(list):
    return {'id' : list[0], 'title': list[1], 'enonce': list[2], 'tag': list[3], 'reponses' : fileIO.format.reponsesTolistOfDic(list[4], list[5])}

def reponsesTolistOfDic(reponses, correctReponse):
    out = []
    for item in reponses:
        if reponses in correctReponse:
            out.append({'val': True, 'text' : item})
        else :
            out.append({'val': False, 'text' : item})
    return out

def listOfDicToreponse(list):
    out = [[],[]]
    for item in list:
        if item['val'] :
            out[1].append(item['text'])
        out[0].append(item['text'])
    return out