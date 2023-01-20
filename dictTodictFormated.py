import formatage
def dictTodictFormated(dico):
    for question in dico:
        question['state']=formatage.formatageMD(question['state'])
        for answer in question['answers']:
            answer['text']=formatage.formatageMD(answer['text'])
    return dico