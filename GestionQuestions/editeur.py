from flask import render_template, request, Blueprint, session, flash, redirect, url_for
import database
import formatage

#import base64 //

edit = Blueprint('editeur',__name__)

# Ouverture sans requête POST
@edit.route('/editeur/<questionId>')
def init(questionId):
  if 'loginP' in session:

    # Cas ou l'on veut créer une nouvelle question
    if questionId == "createNew":

    # Renvoie d'un template vide pour une nouvelle question
      allTag = database.allTags()
      return render_template('EditeurDeQuestion.html', title="", isQcm=True, state="", stateFormated="", idAnswers="", answers=[], answersFormated=[], numeralAnswer=0, tags=allTag, selectedTag=[])

    # Cas ou l'on charge une question
    else:
      allTag = database.allTags()
      # Chargement de la question depuis la BD
      question = database.loadQuestionById(questionId)
      # On accède a la page seulement si la question appartient bien au Professeur
      if question["owner"] == session["loginP"] :

        if question.get("numeralAnswer") :
          print("1")
          return render_template('EditeurDeQuestion.html', title=question["title"], isQcm=False, state=question["state"], stateFormated=formatage.formatageMD(question["state"]), idAnswers="", answers=[], answersFormated=[], numeralAnswer=question["numeralAnswer"], tags=allTag, selectedTag=question["tags"], newTags="")
        else:
          # Calcule des id des réponses pour les conserver dans la page
          idAnswers = ""
          for i in range(0, len(question["answers"])):
            idAnswers += str(i) + ","
          print(idAnswers)
          return render_template('EditeurDeQuestion.html', title=question["title"], isQcm=True, state=question["state"], stateFormated=formatage.formatageMD(question["state"]), idAnswers=idAnswers, answers=question["answers"], answersFormated=formatage.formatAnswers(question["answers"]), numeralAnswer=0, tags=allTag, selectedTag=question["tags"], newTags="")

      # Cas ou l'on veut charger une question déjà créé
      else:
        flash("La question d'id " + questionId + " ne vous appartient pas !\nCréation d'une nouvelle question")
        return render_template('EditeurDeQuestion.html', title="", isQcm=True, state="", stateFormated="", idAnswers="", answers=[], answersFormated=[], numeralAnswer=0, tags=allTag, selectedTag=[], newTags="")
  else:
    flash("Vous devez être connecté pour acceder à cette page")
    return redirect(url_for('login.init'))


# Cas ou l'on veut charger l'apercu ou sauvegarder
@edit.route('/editeur/<questionId>', methods=['POST'])
def editeurPOST(questionId):
  print("pasinit")
  if 'loginP' in session:
    # Récupération de l'énoncé et calcul du rendu
    state = request.form["state"]
    stateFormated = formatage.formatageMD(state) 

    # Recupération des ids des réponses dans un tableau 
    oldIdAnswers = request.form["idAnswers"].split(",")
    answers = []
    newIdAnswers = ""
    answersFormated = []

    # Récupération de chaque réponse si QCM
    if request.form.get("isQcm"):
      for i in range(0, len(oldIdAnswers) - 1) :
        newIdAnswers += str(i) + ","
        n = oldIdAnswers[i]
        answers.append({"val" : request.form.get("checkAnswer" + n)=="on" , "text" : request.form.get("textAnswer" + n)})
      
      # Formatage de chaque réponse
      answersFormated = formatage.formatAnswers(answers)

    else: #Récupération de la réponse numérique si non QCM
      answers = request.form.get("numeralAnswer")

    # Récupération des nouveaux tags ajoutés par l'utilisateurs
    # Récupération de tous les tags
    newTags = request.form.get("newTags").split(',')[0:-1]
    newTagsStr= ""
    allTag = database.allTags() + newTags
    selectedTags=[]

    for t in newTags:
      newTagsStr += t + ","

    # Recherche des tags qui sont cochés
    for t in allTag:
      if request.form.get(t) is not None :
        selectedTags.append(t)

    # Récupération du titre ou ajout du titre par defaut
    title = request.form.get("title")
    if title is not None:
      title.strip()
    if title is None or title=="":
      title = "Sans Titre"

    # Enregistrement si demandé
    if request.form['action'] == "Enregistrer":
      newTagsStr = ""

      if questionId == 'createNew' :
        # sauvegarde de la question et renvoie vers la page avec le bon identifiant pour savoir que la question est déjà dans un fichier
        questionId = database.saveQuestion(session["loginP"], title, state, answers, selectedTags)
        return redirect(url_for('editeur.editeurPOST', questionId=questionId))
      
      else:
        # update de la question déjà existente
        database.updateQuestion(questionId, session["loginP"], title, state, answers, selectedTags)

    # Renvoie de la template avec l'apercu
    if request.form.get("isQcm") :
      return render_template('EditeurDeQuestion.html', title=title, isQcm=True, state=state, stateFormated=stateFormated, idAnswers=newIdAnswers, answers=answers, answersFormated=answersFormated, numeralAnswer="0", tags=allTag, selectedTag=selectedTags, newTags=newTagsStr)
    else:
      return render_template('EditeurDeQuestion.html', title=title, isQcm=False, state=state, stateFormated=stateFormated, idAnswers=newIdAnswers, answers=[], answersFormated=[], numeralAnswer=str(answers), tags=allTag, selectedTag=selectedTags, newTags=newTagsStr)

  else:
    flash("Vous devez être connecté pour acceder à cette page")
    return redirect(url_for('login.init'))
