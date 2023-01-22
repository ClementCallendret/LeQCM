import markdown
import pygments # NE PAS ENLEVER (même si marqué inutilisé)

# la variable text correspondra à ce que l'on récupérera de la méthode POST provenant du code html (la on le prof a tapé le code)
# OBJECTIF : renvoyer le contenu de cette variable au code html une fois bien traduite peu importe si le prof a tapé du mermaid, du code, du LaTeX, etc...
def formatageMD(text):
    text2 = text.copy()
    text2 = '\n'+text2.replace('\r', '')
    html = markdown.markdown(text2, extensions=['codehilite','fenced_code','md_mermaid'])
    return html

def dictTodictFormated(dico):
    for question in dico:
        question['state']=formatageMD(question['state'])
        for answer in question['answers']:
            answer['text']=formatageMD(answer['text'])
    return dico

def formatAnswers(answers):
    formatedAns = []
    for a in answers:
        formatedAns.append({"val" : a["val"], "text" :formatageMD(a["text"])})
    return formatedAns