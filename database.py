import sqlalchemy as sa
from extension import db
import models
from datetime import datetime

def dbCommit(): #(fct intermediaire)
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

def addProfessor(username, password, sel) :
    prof = models.Professor(username=username, password=password, sel=sel)
    db.session.add(prof)
    if dbCommit():
        return prof.username
    else:
        return False

def changeProfessorPassword(username, newPswd):
    prof = models.Professor.query.filter_by(username=username).first()
    prof.password = newPswd
    return dbCommit()

def getProfessorSel(username):
    prof = models.Professor.query.filter_by(username=username).first()
    if prof :
        return prof.sel
    else:
        return False

############### STUDENT LOGIN #######################

def matchStudentPassword(idS, password) :
    std = models.Student.query.filter_by(id=idS).first()
    if not std or not (password == std.password) :
        return False
    else:
        return True

def studentExist(idS) :
    std = models.Student.query.filter_by(id=idS).first()
    if std:
        return True
    else :
        return False

def addStudent(idS, name, surname, sel) :
    if not studentExist(idS):
        std = models.Student(id=idS, password=idS, name=name, surname=surname, sel=sel)
        db.session.add(std)
        if dbCommit():
            return std.id
    return False

def changeStudentPassword(idS, newPswd):
    std = models.Student.query.filter_by(id=idS).first()
    stdpassword = newPswd
    return dbCommit()

def getStudentSel(idS):
    std = models.Student.query.filter_by(id=idS).first()
    if std :
        return std.sel
    else:
        return False
    
def getStudentName(idS):
    std = models.Student.query.filter_by(id=idS).first()
    if std :
        return std.name
    else:
        return False
    
def getStudentSurname(idS):
    std = models.Student.query.filter_by(id=idS).first()
    if std :
        return std.surname
    else:
        return False

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
    if dbCommit():
        return tag.name
    else:
        return False

def deleteTag(name):
    tag = models.Tag.query.filter_by(name = name).first()
    db.session.delete(tag)
    return dbCommit()

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
    return dbCommit()

####################### ANSWERS ######################

def addAnswer(answer, idQuestion):
    rep = models.Answer(solution=answer["val"], text=answer["text"], idQ=idQuestion)
    db.session.add(rep)
    dbCommit()
    return rep.id

def deleteAnswer(idA):
    relation = models.Answer.query.filter_by(idQ=idA).first()
    db.session.delete(relation)
    return dbCommit()

###################### MODIFICATIONS QUESTIONS ####################

def saveQuestion(idProf, title, state, answers, tags):
    if isinstance(answers, list):
        question = models.Question(title=title, state=state, idP=idProf)
    else:
        question = models.Question(title=title, state=state, idP=idProf, numeralAnswer=answers)

    db.session.add(question)
    if not dbCommit():
        return False

    questionId = question.id

    for t in tags:
        addHasTag(questionId, t)
    
    if isinstance(answers, list):
        for rep in answers:
            if not addAnswer(rep, questionId):
                return False

    return questionId

def updateQuestion(idQuestion, idProf, title, state, answers, tags):
    dataAnswers = models.Answer.query.filter_by(idQ=idQuestion)
    dataTags = models.HasTag.query.filter_by(idQ=idQuestion)
    dataQuestion = models.Question.query.filter_by(id=idQuestion).first()

    if isinstance(answers, list):
        #Suppression des réponses qui ne sont plus présentes
        for row in dataAnswers:
            if {"val": row.solution, "text" : row.text} not in answers:
                db.session.delete(row)
                db.session.commit()

        #Ajout des nouvelles réponses
        for ans in answers:
            if not models.Answer.query.filter_by(idQ=idQuestion, text=ans["text"], solution=ans["val"]).first() :
                addAnswer(ans, idQuestion)

        #On s'assure que la réponse numérique soit Null
        dataQuestion.numeralAnswer = None

    else:
        #Suppression des réponse QCM si jamais on a changé de mode
        for row in dataAnswers:
            db.session.delete(row)
            db.session.commit()
        
        #Maj de la réponse numérique
        dataQuestion.numeralAnswer = answers


    #suppression des tags qui ne sont plus présents
    for row in dataTags:
        if row.idT not in tags:
            deleteHasTag(idQuestion, row.idT)
    
    #Ajout des nouveaux tags
    for t in tags:
        if not models.HasTag.query.filter_by(idQ=idQuestion, idT=t).first() :
            addHasTag(idQuestion, t)

    dataQuestion.title = title
    dataQuestion.state = state
    db.session.commit()

def deleteQuestion(idQuestion):
    dataAnswers = models.Answer.query.filter_by(idQ=idQuestion)
    dataTags = models.HasTag.query.filter_by(idQ=idQuestion)

    for row in dataAnswers:
        db.session.delete(row)
        db.session.commit()

    for row in dataTags:
        deleteHasTag(idQuestion, row.idT)

    deleteQuestionFromSquences(idQuestion)

    q = models.Question.query.filter_by(id=idQuestion).first()
    db.session.delete(q)
    return dbCommit()

######################### REQUETES QUESTIONS ############################

def parseQuestionData(dataQuestion, dataAnswers, dataTags): #(fct intermédiaire)
    question = {"id":None, "owner" : "", "title" : "", "state":"", "tags":[]}
    
    if not question:
        return None

    question["id"] = dataQuestion.id
    question["title"] = dataQuestion.title
    question["state"] = dataQuestion.state
    question["owner"] = dataQuestion.idP

    if dataQuestion.numeralAnswer is None:
        question["answers"] = []
        for row in dataAnswers:
            question["answers"].append({"val": row.solution, "text" : row.text})
    else:
        question["numeralAnswer"] = dataQuestion.numeralAnswer
    
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
    if question :
        return question.idP == idProf
    else:
        return False

###################### MODIFICATIONS SEQUENCE ############################

def addQuestionToSerie(idSerie, idQuestion, posQ):
    InSerie = models.InSerie(idS = idSerie, idQ=idQuestion, posQ=posQ)
    db.session.add(InSerie)
    return dbCommit()

def saveSequence(idList, idProf, title):
    serie = models.Serie(idP = idProf, title=title)
    db.session.add(serie)
    if not dbCommit():
        return False

    for i in range(0, len(idList)):
        addQuestionToSerie(serie.id, idList[i], i)
    
    return serie.id

def deleteQuestionFromSquences(idQ):
    inSeries = models.InSerie.query.filter_by(idQ=idQ)
    for row in inSeries:
        pos = row.posQ
        questionsAfter = models.InSerie.query.filter(models.InSerie.idS == row.idS, models.InSerie.posQ>pos)
        for q in questionsAfter:
            q.posQ -= 1
        db.session.delete(row)
    return dbCommit()

def deleteSequence(idSequence):
    inSeries = models.InSerie.query.filter_by(idS=idSequence)
    for row in inSeries:
        db.session.delete(row)
    
    serie = models.Serie.query.filter_by(id=idSequence).first()
    db.session.delete(serie)
    return dbCommit()

######################### REQUETES SEQUENCES ############################

def possedeSequence(idS, idProf):
    serie = models.Serie.query.filter_by(id=idS).first()
    if serie:
        return serie.idP == idProf
    else:
        return False
    
def loadSequenceById(idSerie):
    serie = {}
    serieDatas = models.Serie.query.filter_by(id=idSerie).first()   
    serie["title"] = serieDatas.title
    serie["id"] = serieDatas.id
    questionsData = models.InSerie.query.filter_by(idS=idSerie).order_by(models.InSerie.posQ)

    serie["idList"] = []
    serie["questionTitles"] = []
    for row in questionsData:
        serie["idList"].append(row.idQ)
        serie["questionTitles"].append(models.Question.query.filter_by(id=row.idQ).first().title)

    return serie

def loadSequencesByProf(idProf):
    series = []
    for row in models.Serie.query.filter_by(idP=idProf):
        series.append(loadSequenceById(row.id))
    return series

def getQuestionFromSequence(id, index):
    question = models.InSerie.query.filter_by(idS=id, posQ=index).first()
    if question:
        return loadQuestionById(question.idQ)
    else:
        return None
    
####################### ARCHIVAGE SESSIONS ###############################

def saveSession(idProf, idSQ, isSequence):
    session = models.Session(idP=idProf, idSQ=idSQ, date=datetime.now(), isSequence=isSequence)
    db.session.add(session)
    if dbCommit():
        return session.id
    else:
        return None

def saveStudentAnswer(idStudent, idSession, correct, indexInSerie = None):
    answer = models.StudentAnswer(idSession=idSession, idStudent=idStudent, correct=correct, indexInSeries=indexInSerie)
    db.session.add(answer)
    return dbCommit()

def getSessionResults(idSession):
    #retourner les résultats de la session
    #{isSequence : bool, results : [{"idStudent":id, "correct":nbCorrect}, ...]}
    pass