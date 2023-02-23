from flask import render_template, request, Blueprint, session, redirect, url_for, flash
from flask_socketio import join_room, leave_room, emit
from extension import socketio
import database
from random import choice
import string
import formatage
import json

# a installer : 
# flask-socketio
# eventlet

questionLive = Blueprint('questionLive',__name__)
rooms = {}

@questionLive.route('/liveSession/<id>')
def liveSessionRoute(id):
    if "loginP" in session or "loginS" in session:
        if id in rooms:
            room = rooms[id]
            isProf = "loginP" in session
            return render_template("questionDisplay.html", idS=id, question=room["activeQuestion"], nbConnected=room["nbConnected"], nbAns=room["nbAns"], inSequence=room["inSequence"], isProf=isProf)
        else:
            return "La session est introuvable"
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.init'))

########################### GESTION SESSION ########################################

@questionLive.route('/createNewSession/<mode>/<id>')
def createNew(mode, id):
    if "loginP" in session :
        if (mode == "Question" and database.possedeQuestion(id, session["loginP"])) or (mode == "Sequence" and database.possedeSequence(id, session["loginP"])) :
            roomId = generateSessionId()
            newRoom = {}
            newRoom["creator"] = session["loginP"]
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
            if not "numeralAnswer" in question:
                question["answers"] = formatage.formatAnswers(question["answers"])
                newRoom["totalAnswers"] = [0]*len(question["answers"]) #nb de personne ayant proposé chaque rep
                newRoom["correction"] = []
                for i in range(len(question["answers"])): #correction
                    if question["answers"][i]["val"]:
                        newRoom["correction"].append(i)
            else:
                newRoom["totalAnswers"] = {} #nb de personne ayant proposé chaque rep

            newRoom["activeQuestion"] = question
            archiveId = database.saveSession(session["loginP"], id, newRoom["inSequence"])
            newRoom["archiveId"] = archiveId
            rooms[roomId] = newRoom
            return redirect(url_for('questionLive.liveSessionRoute', id=roomId))
        else:
            flash("La question ou séquence demandé est introuvable")
            return redirect(url_for('mesQuestions.mainPage'))
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.init'))
    
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

                if "numeralAnswer" in question:
                    room["totalAnswers"] = {}
                else:
                    question["answers"] = formatage.formatAnswers(question["answers"])
                    room["totalAnswers"] = [0]*len(question["answers"])
                    room["correction"] = []
                    for i in range(len(question["answers"])): #correction
                        if question["answers"][i]["val"]:
                            room["correction"].append(i)

                for s in room["connected"]:
                    room["connected"][s] = None

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
        if "loginP" in session and session["loginP"] == room["creator"]: # pour un prof
            join_room(id)
        elif "loginS" in session: # pour un élève
            join_room(id)
            if session["loginS"] not in room["connected"]:
                room["connected"][session["loginS"]] = None #pour enregistrer ses reponses
                room["nbConnected"] += 1
                emit("addOneConnected", to=id)
        else:
            flash("Vous devez être connecté pour acceder à cette page")
            return redirect(url_for('login.init'))

        if room["liveAnswersShown"]:
            emit("showLiveAnswers", getLiveAnswers(id))
        if room["corrected"]:
            emit("showCorrection", getCorrection(id))

@socketio.on("quitSession")
def quitSession(id):
    if id in rooms:
        room = rooms[id]
        if session.get("loginP") == room["creator"]:
            del room
            emit("stopSession", to=id)
        elif session.get("loginS") in room["connected"]:
            room["nbConnected"] -= 1
            emit("rmOneConnected", to=id)
            del room["connected"][session["loginS"]]

########################### GESTION DES REPONSES ####################################

@socketio.on("sendAnswers")
def saveAnswers(data):
    data = json.loads(data)
    answers = data["answers"]
    id = data["rId"]
    login = ""
    if id in rooms :
        room = rooms[id]
        if session.get("loginS") in room["connected"] :
            login = session["loginS"]
            emit("desactivateAnswers")
        else:
            return
    
        if room["connected"][login] is None:
            room["connected"][login] = answers
            room["nbAns"] += 1
            isCorrect = False
            if isinstance(answers, list):
                for a in answers:
                    room["totalAnswers"][a] += 1
                if set(room["correction"]) == set(answers):
                    isCorrect = True
            else:
                if answers in room["totalAnswers"]:
                    room["totalAnswers"][answers] += 1
                else:
                    room["totalAnswers"][answers] = 1
                if answers == room["activeQuestion"]["numeralAnswer"]:
                    isCorrect = True
            if room["inSequence"]:
                database.saveStudentAnswer(login, room["archiveId"], isCorrect, room["indexQ"])
            else:
                database.saveStudentAnswer(login, room["archiveId"], isCorrect)

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
        return json.dumps(room["activeQuestion"]["numeralAnswer"], indent=4)
    else:
        return json.dumps(room["correction"], indent=4)

########################## REPONSES LIVE ##########################

@socketio.on("showLiveAnswers")
def sendLiveAnswers(id):
    if id in rooms:
        room = rooms[id]
        if session.get("loginP") == room["creator"] and not room["liveAnswersShown"]:
            emit("showLiveAnswers", getLiveAnswers(room), to=id)
            room["liveAnswersShown"] = True

def getLiveAnswers(room):
    nbAns = room["nbAns"]
    if "numeralAnswer" in room["activeQuestion"]:
        fiveMostAnswered = ["None"]*5
        fiveMostAnsweredQuant = [0]*5
        if nbAns == 0 :
            return json.dumps([fiveMostAnswered, fiveMostAnsweredQuant], indent=4)
        for key, value in room["totalAnswers"]:
            for i in range(0, 4):
                if value > fiveMostAnsweredQuant[i]:
                    fiveMostAnsweredQuant.insert(i, value)
                    fiveMostAnswered.insert(i, key)
                    fiveMostAnsweredQuant.pop()
                    fiveMostAnswered.pop()
                    break
        for e in fiveMostAnsweredQuant:
            e = (e/nbAns)*100
        fiveMostAnswered[4] = "Autres"
        fiveMostAnsweredQuant[4] = ((nbAns - sum(fiveMostAnsweredQuant[:-1])) / nbAns)*100
        return json.dumps([fiveMostAnswered, fiveMostAnsweredQuant], indent=4)
    else:
        givenAnswers = room["totalAnswers"]
        percents = []
        if nbAns == 0 :
            return json.dumps([0]*len(givenAnswers), indent=4)
        for a in givenAnswers:
            percents.append((a/nbAns)*100)
        return json.dumps(percents, indent=4)

########################## MESSAGES ##########################

@socketio.on('message')
def handle_message(data):
    print("######################################################################################################")
    print('received message: ' + data["m"] + " from " + session.get("loginP"))
    print("######################################################################################################")



