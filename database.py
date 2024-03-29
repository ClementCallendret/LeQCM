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

def addProfessor(username, name, surname, password, sel) :
    prof = models.Professor(username=username, name=name, surname=surname, password=password, sel=sel)
    db.session.add(prof)
    if dbCommit():
        return prof.username
    else:
        return False

def getProfessorSel(username):
    prof = models.Professor.query.filter_by(username=username).first()
    if prof :
        return prof.sel
    else:
        return None

def getProfIdentity(username):
    prof = models.Professor.query.filter_by(username=username).first()
    if prof :
        return [prof.name, prof.surname]
    else:
        return None
    
def updateProfessorPassword(username, newPswd, newSel):
    prof = models.Professor.query.filter_by(username=username).first()
    if prof :
        print("ok")
        prof.password = newPswd
        prof.sel = newSel
        return dbCommit()
    else:
        print("non")
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

def addStudent(idS, name, surname, password, sel) :
    if not studentExist(idS):
        std = models.Student(id=idS, password=password, name=name, surname=surname, sel=sel)
        db.session.add(std)
        if dbCommit():
            return std.id
    return False

def addHasStudent(idP, idS):
    if not studentExist(idS) or not professorExist(idP):
        return False
    relation = models.HasStudent(idP=idP, idS=idS)
    db.session.add(relation)
    return dbCommit()

def getStudentSel(idS):
    std = models.Student.query.filter_by(id=idS).first()
    if std :
        return std.sel
    else:
        return None
    
def getStudentIdentity(idS):
    std = models.Student.query.filter_by(id=idS).first()
    if std :
        return [std.name, std.surname]
    else:
        return None
    
def updateStudentPassword(id, newPswd, newSel):
    std = models.Student.query.filter_by(id=id).first()
    if std :
        std.password = newPswd
        std.sel = newSel
        return dbCommit()
    else:
        return False
    
def getStudentsByProf(idP):
    students = []
    for student in models.HasStudent.query.filter_by(idP=idP):
        id = getStudentIdentity(student.idS)
        students.append([student.idS, id[0], id[1]])
    return students

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

def allTagsByProf(idProf):
    tags = []
    for tag in models.Tag.query.join(models.HasTag, models.HasTag.idT == models.Tag.name).join(models.Question, models.Question.id == models.HasTag.idQ).with_entities(models.Tag.name.distinct()).filter(models.Question.idP == idProf):
        tags.append(tag[0])
    return tags

def nbQuestionsPerTag(idProf):
    result = {}
    for tag in allTagsByProf(idProf):
        result[tag] = models.Question.query.join(models.HasTag, models.HasTag.idQ == models.Question.id).filter(models.Question.idP == idProf, models.HasTag.idT == tag).count()
    return result

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

def saveQuestion(idProf, title, state, tags, mode, answers = None):
    question = models.Question(title=title, state=state, idP=idProf, mode=mode)

    if mode == 1:
        question.numeralAnswer = answers

    db.session.add(question)
    if not dbCommit():
        return False

    questionId = question.id

    for t in tags:
        addHasTag(questionId, t)
    
    if mode == 0:
        for rep in answers:
            if not addAnswer(rep, questionId):
                return False

    return questionId

def updateQuestion(idQuestion, idProf, title, state, tags, mode, answers = None):
    dataAnswers = models.Answer.query.filter_by(idQ=idQuestion)
    dataTags = models.HasTag.query.filter_by(idQ=idQuestion)
    dataQuestion = models.Question.query.filter_by(id=idQuestion).first()

    if mode == 0:
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
        dataQuestion.mode = 0

    else:
        #Suppression des réponse QCM si jamais on a changé de mode
        for row in dataAnswers:
            db.session.delete(row)
            db.session.commit()
        
        #Maj de la réponse numérique
        if mode == 1:
            dataQuestion.mode = 1
            dataQuestion.numeralAnswer = answers
        else :
            dataQuestion.mode = 2
            dataQuestion.numeralAnswer = None

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
    deleteQuestionSessions(idQuestion)

    q = models.Question.query.filter_by(id=idQuestion).first()
    db.session.delete(q)
    return dbCommit()

######################### REQUETES QUESTIONS ############################

def parseQuestionData(dataQuestion, dataAnswers, dataTags): #(fct intermédiaire)
    question = {}
    
    if not dataQuestion:
        return None

    question["id"] = dataQuestion.id
    question["title"] = dataQuestion.title
    question["state"] = dataQuestion.state
    question["owner"] = dataQuestion.idP
    question["mode"] = dataQuestion.mode

    if dataQuestion.mode == 0:
        question["answers"] = []
        for row in dataAnswers:
            question["answers"].append({"val": row.solution, "text" : row.text})
    elif dataQuestion.mode == 1:
        question["numeralAnswer"] = dataQuestion.numeralAnswer
    
    question["tags"] = []
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

def loadQuestionsByProfTag(idProf, tag):
    questions = models.Question.query.join(models.HasTag, models.HasTag.idQ == models.Question.id).with_entities(models.Question.id.distinct()).filter(models.Question.idP == idProf, models.HasTag.idT == tag, models.Question.mode != 2)
    result = []
    for row in questions:
        result.append(row[0])
    return result

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
        idSeq = row.idS
        questionsAfter = models.InSerie.query.filter(models.InSerie.idS == row.idS, models.InSerie.posQ>pos)
        for q in questionsAfter:
            q.posQ -= 1
        db.session.delete(row)
        deleteSequenceQuestionAnswers(idSeq, idQ)
        if not models.InSerie.query.filter_by(idS=idSeq).first():
            deleteSequence(idSeq)
    return dbCommit()

def deleteSequence(idSequence):
    deleteSequenceSessions(idSequence)
    inSeries = models.InSerie.query.filter_by(idS=idSequence)
    for row in inSeries:
        db.session.delete(row)
    serie = models.Serie.query.filter_by(id=idSequence).first()
    db.session.delete(serie)
    return dbCommit()

def updateSequence(id, idList, title):
    seq = models.Serie.query.filter_by(id=id).first()
    if not seq:
        return False
    
    seq.title = title
    for row in models.InSerie.query.filter_by(idS=id):
        if row.idQ not in idList:
            db.session.delete(row)
    for i in range(0, len(idList)):
        q = models.InSerie.query.filter_by(idS=id, idQ=idList[i]).first()
        if q:
            q.posQ = i
        else:
            addQuestionToSerie(id, idList[i], i)

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

def saveSession(idProf, id, mode):
    if mode == "Question":
        newSession = models.Session(idP=idProf, idQuestion=id, date=datetime.now())
    else:
        newSession = models.Session(idP=idProf, idSequence=id, date=datetime.now())
    db.session.add(newSession)
    if dbCommit():
        return newSession.id
    else:
        return None

def saveStudentAnswer(idSession, idStudent, correct, idQuestion, openAnswer=None):
    answer = models.StudentAnswer(idSession=idSession, idStudent=idStudent, idQuestion=idQuestion, correct=correct, openAnswer=openAnswer)
    db.session.add(answer)
    return dbCommit()

def possedeSession(idS, idProf):
    session = models.Session.query.filter_by(id=idS).first()
    if session :
        return session.idP == idProf
    else:
        return False

def loadSessionDataById(idSession):
    mySession = models.Session.query.filter_by(id=idSession).first()
    if mySession:
        sessionData = {}
        sessionData["id"] = mySession.id
        sessionData["date"] = mySession.date.strftime("%d/%m/%Y")
        sessionData["idProf"] = mySession.idP
        if mySession.idSequence != None:
            sessionData["idSequence"] = mySession.idSequence
            sessionData["isSequence"] = True
            sessionData["nbAnswers"] = getSequenceAvgNbAnswers(idSession, sessionData["idSequence"])
            sessionData["title"] = models.Serie.query.filter_by(id=mySession.idSequence).first().title
        else :
            sessionData["idQuestion"] = mySession.idQuestion
            sessionData["isSequence"] = False
            sessionData["nbAnswers"] = getQuestionNbAnswers(idSession, sessionData["idQuestion"])
            sessionData["title"] = models.Question.query.filter_by(id=mySession.idQuestion).first().title
        return sessionData
    else:
        return None
    # pour afficher juste un apercu des sessions passés (un peu comme dans mes questions)
    # retour : {id : int, date : date(jspTrop), idProf : string, isSequence : bool, (idSequence ou idQuestion) : int, nbAnswers : [nbAnswers/nbQuestions, nbGoodAnswers/nbQuestions]}

def loadSessionDataByProf(idProf):
    sessions = []
    for row in models.Session.query.filter_by(idP=idProf).order_by(models.Session.date.desc()):
        sessions.append(loadSessionDataById(row.id))
    return sessions
    #pareil mais par prof

def loadSessionResults(idSession):
    session = models.Session.query.filter_by(id=idSession).first()
    if session:
        sessionData = loadSessionDataById(idSession)
        if sessionData["isSequence"]:
            sessionData["results"] = getAvgSequenceResults(idSession, sessionData["idSequence"])
        else:
            sessionData["results"] = getQuestionsResults(idSession, sessionData["idQuestion"])
        return sessionData
    else:
        return None
    
    # retour : {id : int, date : date(jspTrop), idProf : string, isSequence : bool, (idSequence ou idQuestion) : int, nbAnswers : [nbAnswers/nbQuestions, nbGoodAnswers/nbQuestions], results}
    # results si question unique: {idStudent1 : bool, idStudent2 : bool, ...}
    # results si séquence: {idStudent1 : float(pourcentage), idStudent2 : float, ...}

#calcule le résultat moyen d'une question
def getQuestionNbAnswers(idSession, idQuestion):
    ans = models.StudentAnswer.query.filter_by(idSession=idSession, idQuestion=idQuestion).count()
    if models.Question.query.filter_by(id=idQuestion).first().mode == 2:
        goodAns = ans
    else:
        goodAns = models.StudentAnswer.query.filter_by(idSession=idSession, idQuestion=idQuestion, correct=True).count()
    return [ans, goodAns]

# calcule le résultat moyen d'une séquence
def getSequenceAvgNbAnswers(idSession, idSequence):
    studentAnswers = models.StudentAnswer.query.join(models.Question, models.StudentAnswer.idQuestion == models.Question.id).filter(models.StudentAnswer.idSession == idSession)
    nbAnswers = studentAnswers.count()
    nbGoodAnswers = studentAnswers.filter(models.StudentAnswer.correct == True).count()
    nbQ = models.InSerie.query.filter_by(idS = idSequence).count()
    print(nbAnswers)
    print(nbGoodAnswers)
    print(nbQ)
    print([nbAnswers / nbQ, nbGoodAnswers / nbQ])
    return [nbAnswers / nbQ, nbGoodAnswers / nbQ]

# calcule les résultats d'une question pour chaque élève
def getQuestionsResults(idSession, idQuestion):
    results = {}
    allAnswers = models.StudentAnswer.query.filter_by(idSession=idSession, idQuestion=idQuestion)
    reponsesOuvertes = (models.Question.query.filter_by(id=idQuestion).first().mode == 2)
    for row in allAnswers:
            results[str(row.idStudent)] = (reponsesOuvertes or row.correct)
    return results

# calcule le pourcentage de bonne réponse pour chaque élève lors d'une séquence
def getAvgSequenceResults(idSession, idSequence):
    results = []
    questions = models.InSerie.query.filter_by(idS=idSequence).order_by(models.InSerie.posQ)
    for row in questions:
        results.append(getQuestionsResults(idSession, row.idQ))
    return avgResults(results)

# a partire des réponses a plusieurs questions, calcule le pourcentage de bonne réponse pour chaque élève
def avgResults(results):
    avgResults = {}
    n = len(results)
    for i in range(0, n):
        for student in results[i]:
            if student not in avgResults:
                avgResults[student] = 0.0
            if results[i][student]:
                avgResults[student] += 100.0 / n

    return avgResults

#supprime toute les réponses données à une question (diffusé dans une séquence)
def deleteSequenceQuestionAnswers(idS, idQ):
    for row in models.Session.query.filter_by(idSequence=idS):
        models.StudentAnswer.query.filter_by(idQuestion=idQ, idSession=row.id).delete()
    return dbCommit()

#supprime toute les sessions relative à une question
def deleteQuestionSessions(idQuestion):
    for row in models.Session.query.filter_by(idQuestion=idQuestion):
        models.StudentAnswer.query.filter_by(idSession=row.id).delete()
        db.session.delete(row)
    return dbCommit()

#supprime toute les sessions relative à une séquence
def deleteSequenceSessions(idS):
    for row in models.Session.query.filter_by(idSequence=idS):
        models.StudentAnswer.query.filter_by(idSession=row.id).delete()
        db.session.delete(row)
    return dbCommit()

#supprime une session
def deleteSession(idSession):
    models.StudentAnswer.query.filter_by(idSession=idSession).delete()
    db.session.delete(models.Session.query.filter_by(id=idSession).first())
    return dbCommit()

