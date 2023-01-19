from flask import render_template, request, Blueprint
import markdown
import pygments
import fileIO
#import md_mermaid, latex
#import base64 

edit = Blueprint('editeur',__name__)

# la variable text correspondra à ce que l'on récupérera de la méthode POST provenant du code html.
# OBJECTIF : renvoyer le contenu de cette variable au code html une fois bien traduite (dans la variable html )
def formatageMD(text):
  html = markdown.markdown(text, extensions=['codehilite','fenced_code','md_mermaid']) #toutes les extensions ABSOLUMENTS INDISPENSABLES pour mermaid, le code coloré
  return html
  

@edit.route('/editeur', methods=['GET','POST'])
def editeurGet():
  if request.method == 'POST' :
    enonce = request.form["enonce"]
    enonceToFormate = '\n'+enonce.replace('\r','') #On rajoute un \n au début + on remplace tous les \r générés à chaque retour chariot par "".
    enonceFormate = formatageMD(enonceToFormate) # Calcul du rendu de l'énoncé qui est passé par le formatage

    oldIdReponses = request.form["idReponses"].split(",") # Recupération des ids dans un tableau
    reponses = []
    newIdReponses = ""
    for i in range(0, len(oldIdReponses) - 1) : # Récupération des réponses
      newIdReponses += str(i) + ","
      n = oldIdReponses[i]
      reponses.append({"val" : request.form.get("checkReponse" + n), "text" : request.form["textReponse" + n]})
    # si on l'enregistre, on crée une nouvelle question
    # attention, mettre un bool, si la question a déja été enregistrée, on passe par la metode update!!!!
    if request.form['sendType']=='Enregistrer':
      # on formate les données pour l'enristrement
      reponsesASave = []
      reponsesCorrectes = []
      for item in reponses:
        reponsesASave.append(item['text'])
        if item['val'] == 'On':
          reponsesCorrectes.append(request.form["textReponse" + n])
      # enregistrement sur le stockage
      fileIO.question.newQuestion('login?', 'titre?', enonceFormate, reponsesASave, [], reponsesCorrectes)
    # Renvoie de la template avec l'apercu
    return render_template('EditeurDeQuestion.html', reponses=reponses, enonce=enonce, enonceFormate=enonceFormate, idReponses=newIdReponses)
  
  else :
    # Renvoie d'un template vide pour une nouvelle question
    return render_template('EditeurDeQuestion.html', nbReponses= 0, reponses=[], enonce="", enonceFormate="", idReponses="")
