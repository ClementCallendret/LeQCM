from flask import render_template, request, Blueprint, session, flash, redirect, url_for
import fileIO
import formatage

#import base64 //

edit = Blueprint('editeur',__name__)

@edit.route('/editeur/<questionId>')
def init(questionId):
  if 'login' in session:

    # Cas ou l'on veut créer une nouvelle question
    if questionId == "createNew":

    # Renvoie d'un template vide pour une nouvelle question
      allTag = fileIO.question.getAllTags()
      return render_template('EditeurDeQuestion.html', nbanswers= 0, answers=[], state="", stateFormated="", idAnswers="",answersFormated=[],  tags=allTag, selectedTag=[], title="")

    else:
      allTag = fileIO.question.getAllTags()
      # Chargement de la question depuis la BD
      question = fileIO.format.questionToDic(fileIO.question.read(questionId))
      # On accède a la page seulement si la question appartient bien au Professeur
      if question["owner"] == session["login"] :

        # Calcule des id des réponses pour les conserver dans la page
        idAnswers = ""
        for i in range(0, len(question["answers"])):
          idAnswers += str(i) + ","

        return render_template('EditeurDeQuestion.html', nbAnswers= len(question["answers"]), answers=question["answers"], state=question["state"], stateFormated="",answersFormated=[], idAnswers=idAnswers, tags=allTag, selectedTag=question["tags"], title=question["title"])

      # Cas ou l'on veut charger une question déjà créé
      else:
        flash("La question d'id " + questionId + " ne vous appartient pas !\nCréation d'une nouvelle question")
        return render_template('EditeurDeQuestion.html', nbAnswers= 0, answers=[], state="", stateFormated="", idAnswers="",answersFormated=[],  tags=allTag, selectedTag=[], title="")
  else:
    flash("Vous devez être connecté pour acceder à cette page")
    return redirect(url_for('login.init'))


@edit.route('/editeur/<questionId>', methods=['POST'])
def editeurPOST(questionId):
  
  # Cas ou l'on veut charger l'apercu
  if 'login' in session:
    # Récupération de l'énoncé et calcul du rendu
    state = request.form["state"]
    stateFormated = formatage.formatageMD(state) 

    # Recupération des ids dans un tableau 
    oldIdAnswers = request.form["idAnswers"].split(",")
    answers = []
    newIdAnswers = ""

    # Récupération de chaque réponse
    for i in range(0, len(oldIdAnswers) - 1) :
      newIdAnswers += str(i) + ","
      n = oldIdAnswers[i]
      answers.append({"val" : request.form.get("checkAnswer" + n)=="on" , "text" : request.form["textAnswer" + n]})
    
    # Formatage de chaque réponse
    answersFormated = []
    for rep in answers :
      textAnswerFormated = formatage.formatageMD(rep["text"])
      answersFormated.append({"val" : rep["val"], "text" : textAnswerFormated})
    # Récupération des nouveaux tags ajoutés par l'utilisateurs
    # Récupération de tous les tags
    allTag = fileIO.question.getAllTags()
    newTags = request.form.get("newTags").split(',')[0:-1]

    # Recherche des tags qui sont cochés
    tags=[]
    for t in newTags:
      if not (request.form.get(t) == None) :
        tags.append(t)
    for t in allTag:
      if not (request.form.get(t) == None) :
        tags.append(t)
    # Récupération du titre ou ajout du titre par defaut
    title = request.form.get("title")
    if not title == None:
      title.strip()
    if title==None or title=="":
      title = "Sans Titre"

    # Enregistrement si demandé
    if request.form['action'] == "Enregistrer":
      answersSaveFormat = fileIO.format.listOfDicToreponse(answers)

      if questionId == 'createNew' :
        # sauvegarde de la question et renvoie vers la page avec le bon identifiant pour savoir que la question est déjà dans un fichier
        questionId = fileIO.question.newQuestion(session["login"], title, state, tags, answersSaveFormat[0], answersSaveFormat[1])
        return redirect(url_for('editeur.editeurPOST', questionId=questionId))
      
      else:
        # update de la question déjà existente
        fileIO.question.update(questionId, title, state, tags, answersSaveFormat[0], answersSaveFormat[1])

    # Renvoie de la template avec l'apercu
    return render_template('EditeurDeQuestion.html', state=state, stateFormated=stateFormated, answers=answers, answersFormated=answersFormated, idAnswers=newIdAnswers, tags=fileIO.question.getAllTags(), selectedTag=tags, title=title)
  else:
    flash("Vous devez être connecté pour acceder à cette page")
    return redirect(url_for('login.init'))
