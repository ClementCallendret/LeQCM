from flask import render_template, request, Blueprint
import markdown
import md_mermaid, latex
import base64 

edit = Blueprint('editeur',__name__)

def formatageMD(text): # la variable text correspondra à ce que l'on récupérera de la méthode POST provenant du cod html.
              # OBJECTIF : renvoyer le contenu de cette variable au code html une fois bien traduite avec mermaid en l'occurence. 
    html = markdown.markdown(text, extensions=['md_mermaid'])
    return html


@edit.route('/editeur', methods=['GET','POST'])
def editeurGet():
    if request.method == 'POST' :
        question = {"enonce" : "", "enonceFormate" : "", "reponses" : []}
        question["enonce"] = request.form["enonce"]
        question["enonceFormate"] = formatageMD(str(question["enonce"]))
        #question["enonceFormate"] = formatageMD(" \n~~~mermaid\ngraph TB\nA --> B\nB --> C\n~~~\n")

        
        print(question["enonce"])
        print(question["enonceFormate"])

        numsReponses = request.form["idEachReps"].split(",")
        
        newIdReps = ""     
        for i in range(0, len(numsReponses) - 1) :
            newIdReps += str(i) + ","
            n = numsReponses[i]
            question["reponses"].append({"val" : request.form.get("checkReponse" + n), "text" : request.form["textReponse" + n]})
            
        

        return render_template('EditeurDeQuestion.html', nbReponses= len(question["reponses"]), reponses=question["reponses"], enonce=question["enonce"], enonceFormate=question["enonceFormate"], idReps=newIdReps)
    
    else :
        return render_template('EditeurDeQuestion.html', nbReponses= 0, reponses=[], enonce="", enonceFormate="", idReps="")