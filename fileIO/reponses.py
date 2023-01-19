import fileIO

def dicToList(dic):
    reponsesASave = []
    reponsesCorrectes = []
    for item in dic:
        reponsesASave.append(item['text'])
        if item['val'] == True:
            reponsesCorrectes.append(dic['text'])
    return [reponsesASave, reponsesCorrectes]


def listToDic(reponses, correctReponses):
    out = {}
    for item in reponses:
        if item in reponses:
            out.append({'val':True,  'text':item})
        else:
            out.append({'val':False, 'text':item})
    return out

