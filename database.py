import sqlalchemy as sa
from extension import db
import models

def dbCommit():
    try:
        db.session.commit()
        return True
    except sa.exc.SQLAlchemyError:
        db.session.rollback()
        return False

############### PROFESSORS LOGIN #######################

def matchProfessorPassword(username, password) :
    prof = models.Professor.query.filter_by(username=username).first()
    if not prof or not (password == prof.password) :
        return False
    else:
        return True

def professorExist(username) :
    prof = models.Professor.query.filter_by(username=username).first()
    if prof:
        return True
    else :
        return False

def addProfessor(username, password) :
    prof = models.Professor(username=username, password=password)
    db.session.add(prof)
    dbCommit()
    return prof.username

####################### TAG ######################

def tagExist(name):
    tag = models.Tag.query.filter_by(name=name).first()
    if tag:
        return True
    else:
        return False

def addTag(name):
    tag = models.Tag(name=name)
    db.session.add(tag)
    dbCommit()
    return tag.name

def deleteTag(name):
    tag = models.Tag.query.filter_by(id = name)
    db.session.delete(tag)
    db.commit()

def allTags():
    tags = []
    for tag in models.Tag.query.all():
        tags.append(tag.name)
    return tags

####################### HAS TAG ######################
  
def addHasTag(idQ, idT):
    if not tagExist(idT):
        addTag(idT)
    relation = models.HasTag(idQ=idQ, idT=idT)
    db.session.add(relation)
    return dbCommit()

def deleteHasTag(idQ, idT):
    relation = models.HasTag.query.filter_by(idQ=idQ, idT=idT).first()
    db.session.delete(relation)
    if not models.HasTag.query.filter_by(idT=idT).first():
        deleteTag(idT)

####################### ANSWERS ######################

def addAnswer(answer, idQuestion):
    rep = models.Answer(solution=answer["val"], text=answer["text"], idQ=idQuestion)
    db.session.add(rep)
    dbCommit()
    return rep.id

###################### MODIFICATIONS QUESTIONS ####################

def saveQuestion(idProf, title, state, answers, tags):
    question = models.Question(title=title, state=state, idP=idProf)
    db.session.add(question)
    if not dbCommit():
        return "Could not add question " + title + " to database\n"

    questionId = question.id

    returnMessage = ""
    for t in tags:
        addHasTag(questionId, t)
    
    for rep in answers:
        if not addAnswer(rep, questionId):
            returnMessage += "Could not add answer " + rep + " to database\n"

    if returnMessage == "":
        return questionId
    else:
        return returnMessage

def updateQuestion(idQuestion, idProf, title, state, answers, tags):
    dataAnswers = models.Answer.query.filter_by(idQ=idQuestion)
    dataTags = models.HasTag.query.filter_by(idQ=idQuestion)

    #Suppression des réponses qui ne sont plus présentes
    for row in dataAnswers:
        if {"val": row.solution, "text" : row.text} not in answers:
            db.session.delete(row)
            db.session.commit()
    
    #Ajout des nouvelles réponses
    for ans in answers:
        if not models.Answer.query.filter_by(idQ=idQuestion, text=ans["text"], solution=ans["val"]).first() :
            addAnswer(ans, idQuestion)

    #suppression des tags qui ne sont plus présents
    for row in dataTags:
        if row.idT not in tags:
            deleteHasTag(idQuestion, row.idT)
    
    #Ajout des nouveaux tags
    for t in tags:
        if not models.HasTag.query.filter_by(idQ=idQuestion, idT=t).first() :
            addHasTag(idQuestion, t)

    db.session.query(models.Question).filter(models.Question.id == idQuestion).update({"title" : title, "state" : state})
    db.session.commit()

###################### REQUETES QUESTIONS ############################

def parseQuestionData(dataQuestion, dataAnswers, dataTags):
    question = {"id":None, "owner" : "", "title" : "", "state":"", "answers" : [], "tags":[]}
    
    if not question:
        return None

    question["id"] = dataQuestion.id
    question["title"] = dataQuestion.title
    question["state"] = dataQuestion.state
    question["owner"] = dataQuestion.idP

    for row in dataAnswers:
        question["answers"].append({"val": row.solution, "text" : row.text})
    
    for row in dataTags:
        question["tags"].append(row.idT)

    return question

def loadQuestionById(idQ):
    dataQuestion = models.Question.query.filter_by(id=idQ).first()
    dataAnswers = models.Answer.query.filter_by(idQ=idQ)
    dataTags = models.HasTag.query.filter_by(idQ=idQ)
    return parseQuestionData(dataQuestion, dataAnswers, dataTags)

def loadQuestionsByProf(idProf):
    result = []
    dataQuestion = models.Question.query.filter_by(idP=idProf)

    for row in dataQuestion:
        dataAnswers = models.Answer.query.filter_by(idQ=row.id)
        dataTags = models.HasTag.query.filter_by(idQ=row.id)
        result.append(parseQuestionData(row, dataAnswers, dataTags))
    
    return result

def possedeQuestion(idQ, idProf):
    question = models.Question.query.filter_by(id=idQ).first()
    if question.idP == idProf:
        return True
    else :
        return False