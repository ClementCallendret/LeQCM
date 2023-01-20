import fileIO

def dicToQuestion(dic):
    reponses = fileIO.format.listOfDicToreponse(dic['answers'])
    return [dic['id'], dic['owner'],dic['title'], dic['state'], dic['tags'], reponses[0], reponses[1]]


def questionToDic(list):
    return {'id' : list[0], 'owner': list[1], 'title': list[3], 'state': list[2], 'tags': list[4], 'answers' : fileIO.format.reponsesTolistOfDic(list[5], list[6])}

def reponsesTolistOfDic(reponses, correctReponse):
    out = []
    for item in reponses:
        if item in correctReponse:
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