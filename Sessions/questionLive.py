from flask import render_template, request, Blueprint, session, redirect, url_for, flash
from flask_socketio import join_room, leave_room, emit
from extension import socketio
import database
from random import choice
from random import randint
import string
import formatage
import json

allStd = ["15369745", "26589647", "25478965", "86297563", "49786521", "89855122", "79935465", "79552368", "79852655", "98253381", "22568745", "12456882", "15975325", "78945612", "46853238"]
nbStd = len(allStd)

# a installer : 
# flask-socketio
# eventlet

questionLive = Blueprint('questionLive',__name__)
rooms = {}

@questionLive.route('/liveSession/<id>')
def liveSessionRoute(id):
    if "loginP" in session or "loginE" in session:
        if id in rooms:
            room = rooms[id]
            isProf = "loginP" in session
            return render_template("questionDisplay.html", idS=id, question=room["activeQuestion"], nbConnected=room["nbConnected"], nbAns=room["nbAns"], inSequence=room["inSequence"], isProf=isProf)
        else:
            flash("La session "+ id +" est introuvable")
            return redirect(url_for('accueil'))
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.initRedirect', redirection="liveSession-"+id))

########################### GESTION SESSION ########################################

@questionLive.route('/createNewSession/<mode>/<id>')
def createNew(mode, id):
    if "loginP" in session :
        if (mode == "Question" and database.possedeQuestion(id, session["loginP"])) or (mode == "Sequence" and database.possedeSequence(id, session["loginP"])) :
            roomId = generateSessionId()
            newRoom = {}
            newRoom["creator"] = session["loginP"]
            newRoom["creatorSID"] = ""
            newRoom["connected"] = {}
            newRoom["nbConnected"] = 0
            newRoom["nbAns"] = 0
            newRoom["answersOpen"] = True
            newRoom["liveAnswersShown"] = False
            newRoom["corrected"] = False
            question = {}
            if mode == "Sequence":
                newRoom["inSequence"] = True
                newRoom["idSequence"] = id
                newRoom["indexQ"] = 0
                question = database.getQuestionFromSequence(id,0)
            else:
                newRoom["inSequence"] = False
                question = database.loadQuestionById(id)
            
            question["state"] = formatage.formatageMD(question["state"])
            if question["mode"] == 0:
                question["answers"] = formatage.formatAnswers(question["answers"])
                newRoom["totalAnswers"] = [0]*len(question["answers"]) #nb de personne ayant proposé chaque rep
                newRoom["correction"] = []
                for i in range(len(question["answers"])): #correction
                    if question["answers"][i]["val"]:
                        newRoom["correction"].append(i)
            else:
                newRoom["totalAnswers"] = {} #nb de personne ayant proposé chaque rep

            newRoom["activeQuestion"] = question
            archiveId = database.saveSession(session["loginP"], id, mode)
            print(archiveId)
            newRoom["archiveId"] = archiveId
            rooms[roomId] = newRoom

            #simulateAnswers(rooms[roomId]["archiveId"], rooms[roomId]["activeQuestion"])
            return redirect(url_for('questionLive.liveSessionRoute', id=roomId))
        else:
            flash("La question ou séquence demandé est introuvable")
            return redirect(url_for('mesQuestions.mainPage'))
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.initRedirect', redirection="MesQuestions"))
    
@socketio.on("nextQuestion")
def nextQuestion(id):
    if id in rooms:
        room = rooms[id]
        if session.get("loginP") == room["creator"] and room["inSequence"]:
            room["indexQ"] += 1
            question = database.getQuestionFromSequence(room["idSequence"], room["indexQ"])
            if question is not None:
                room["activeQuestion"] = question
                room["answersOpen"] = True
                room["corrected"] = False
                room["liveAnswersShown"] = False
                room["nbAns"] = 0
                question["state"] = formatage.formatageMD(question["state"])

                if question["mode"] == 0:
                    question["answers"] = formatage.formatAnswers(question["answers"])
                    room["totalAnswers"] = [0]*len(question["answers"])
                    room["correction"] = []
                    for i in range(len(question["answers"])): #correction
                        if question["answers"][i]["val"]:
                            room["correction"].append(i)
                else:
                    room["totalAnswers"] = {}

                for s in room["connected"]:
                    room["connected"][s] = None

                #simulateAnswers(room["archiveId"], room["activeQuestion"])
                emit("nextQuestion", question, to=id)
            else:
                emit("stopSession", url_for('accueil'), to=id)

@socketio.on("stopSession")
def stopSession(id):
    if id in rooms:
        room = rooms[id]
        if session.get("loginP") == room["creator"]:
            emit("stopSession", url_for('accueil'), to=id)

def generateSessionId():
    id= ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(8))
    if not rooms.get(id):
        return id
    else :
        return generateSessionId()

########################### CONNEXTION ET DECONNEXION ####################################

@socketio.on('joinRoom')
def joinRoom(data):
    id = data["rId"]
    if id in rooms:
        room = rooms[id]
        if "loginP" in session and session["loginP"] == room["creator"]: # pour le prof
            join_room(id)
            room["creatorSID"] = request.sid
            if(room["liveAnswersShown"]):
                emit("showLiveAnswers", {"nbAnswers" : room["nbAns"], "typeAnswer" : (0 if not "numeralAnswer" in room["activeQuestion"] else 1), "answers" : room["totalAnswers"]}, to=room["creatorSID"])
        elif "loginE" in session: # pour un élève
            join_room(id)
            print(session["loginE"] + " A REJOINS LA SESSION")
            if session["loginE"] not in room["connected"]:
                room["connected"][session["loginE"]] = None #pour enregistrer ses reponses
                room["nbConnected"] += 1
                emit("addOneConnected", to=room["creatorSID"])
            elif room["connected"][session["loginE"]] != None:
                emit("desactivateAnswers")
        else:
            flash("Vous devez être connecté pour acceder à cette page")
            return redirect(url_for('login.init'))

        if room["corrected"]:
            emit("showCorrection", getCorrection(room))

@socketio.on("quitSession")
def quitSession(id):
    if id in rooms:
        room = rooms[id]
        if session.get("loginP") == room["creator"]:
            del room
            emit("stopSession", to=id)

########################### GESTION DES REPONSES ####################################

@socketio.on("sendAnswers")
def saveAnswers(data):
    answers = data["answers"]
    id = data["rId"]
    login = ""
    if id in rooms :
        room = rooms[id]
        if session.get("loginE") in room["connected"] :
            login = session["loginE"]
            print(session.get("loginE") + " A REPONDU")
            emit("desactivateAnswers")
        else:
            return
    
        if room["connected"][login] is None:
            room["connected"][login] = answers
            room["nbAns"] += 1
            isCorrect = False
            if room["activeQuestion"]["mode"] == 0:
                for a in answers:
                    room["totalAnswers"][a] += 1
                if set(room["correction"]) == set(answers):
                    isCorrect = True
            else:
                if answers in room["totalAnswers"]:
                    room["totalAnswers"][answers] += 1
                else:
                    room["totalAnswers"][answers] = 1

                if room["activeQuestion"]["mode"] == 1 and answers == room["activeQuestion"]["numeralAnswer"]:
                    isCorrect = True
                elif room["activeQuestion"]["mode"] == 2 :
                    isCorrect = True
            if room["liveAnswersShown"]:
                emit("newAnswer", answers, to=room["creatorSID"])
            emit("addOneAnswer", to=room["creatorSID"])

            database.saveStudentAnswer(room["archiveId"], login, isCorrect, room["activeQuestion"]["id"], answers if room["activeQuestion"]["mode"] == 2 else None)

def simulateAnswers(id, question):
    pourcentageCorrect = randint(50, 100)
    for i in range(0, randint(8, nbStd)):
        if question["mode"] == 2:
            database.saveStudentAnswer(id, allStd[i], True, question["id"], "réponse Test")
        else:
            correct = False
            if randint(0, 100) > pourcentageCorrect:
                correct = True
            database.saveStudentAnswer(id, allStd[i], correct, question["id"], None)

@socketio.on("stopAnswers")
def stopAnswers(id):
    if id in rooms:
        room = rooms[id]
        if session.get("loginP") == room["creator"] and room["answersOpen"]:
            room["answersOpen"] = False
            emit("desactivateAnswers", to=id)

########################## CORRECTION ##########################

@socketio.on("showCorrection")
def sendCorrection(id):
    if id in rooms:
        room = rooms[id]
        if session.get("loginP") == room["creator"] and not room["corrected"]:
            emit("showCorrection", getCorrection(room), to=id)
            room["corrected"] = True

def getCorrection(room):
    if "numeralAnswer" in room["activeQuestion"]:
        return room["activeQuestion"]["numeralAnswer"]
    else:
        return room["correction"]

########################## REPONSES LIVE ##########################

@socketio.on("showLiveAnswers")
def sendLiveAnswers(id):
    if id in rooms:
        room = rooms[id]
        if session.get("loginP") == room["creator"] and not room["liveAnswersShown"] :
            emit("showLiveAnswers", {"nbAnswers" : room["nbAns"], "answers" : room["totalAnswers"]}, to=room["creatorSID"])
            room["liveAnswersShown"] = True

########################## MESSAGES ##########################

@socketio.on('message')
def handle_message(data):
    print("#####################################################################")
    print('received message: ' + data["m"] + " from " + session.get("loginP"))
    print("#####################################################################")



