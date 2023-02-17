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
        if rooms.get(id):
            isProf = "loginP" in session
            return render_template("questionDisplay.html", idS=id, question=rooms[id]["activeQuestion"], nbConnected=rooms[id]["nbConnected"], nbAns=rooms[id]["nbAns"], inSequence=rooms[id]["inSequence"], isProf=isProf)
        else:
            return "La session est introuvable"
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.init'))

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
                question = database.getFirstQuestion(id)
            else:
                newRoom["inSequence"] = False
                question = database.loadQuestionById(id)
            if not "numeralAnswer" in question:
                question["answers"] = formatage.formatAnswers(question["answers"])
            question["state"] = formatage.formatageMD(question["state"])
            if "numeralAnswer" in question:
                newRoom["totalAnswers"] = {} #nb de personne ayant proposé chaque rep
            else:
                newRoom["totalAnswers"] = [0]*len(question["answers"]) #nb de personne ayant proposé chaque rep
            newRoom["activeQuestion"] = question
            rooms[roomId] = newRoom
            return redirect(url_for('questionLive.liveSessionRoute', id=roomId))
        else:
            flash("La question ou séquence demandé est introuvable")
            return redirect(url_for('mesQuestions.mainPage'))
    else:
        flash("Vous devez être connecté pour acceder à cette page")
        return redirect(url_for('login.init'))

def generateSessionId():
    id= ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(6))
    if not rooms.get(id):
        return id
    else :
        return generateSessionId()
    
@socketio.on('joinRoom')
def joinRoom(data):
    id = data["rId"]
    if id in rooms:
        if "loginP" in session: # pour un autre compte prof qui assisterais a la session
            join_room(id)
            if session["loginP"] != rooms[id]["creator"] and session["loginP"] not in rooms[id]["connected"]:
                rooms[id]["connected"][session["loginP"]] = None #pour enregistrer ses réponses
                rooms[id]["nbConnected"] += 1
                emit("addOneConnected", to=id)
        elif "loginS" in session: # pour un élève
            join_room(id)
            if session["loginS"] not in rooms[id]["connected"]:
                rooms[id]["connected"][session["loginS"]] = None #pour enregistrer ses reponses
                rooms[id]["nbConnected"] += 1
                emit("addOneConnected", to=id)
        else:
            flash("Vous devez être connecté pour acceder à cette page")
            return redirect(url_for('login.init'))

        if rooms[id]["liveAnswersShown"]:
            emit("showLiveAnswers", getLiveAnswers(id))
        if rooms[id]["corrected"]:
            emit("showCorrection", getCorrection(id))

    else:
        return "Session Introuvable :("

@socketio.on("sendAnswers")
def saveAnswers(data):
    data = json.loads(data)
    answers = data["answers"]
    id = data["rId"]
    login = ""
    if session.get("loginS") and session["loginS"] in rooms[id]["connected"] :
        login = session["loginS"]
        emit("desactivateAnswers")
    elif session.get("loginP") and session["loginP"] in rooms[id]["connected"]:
        login = session["loginP"]
        emit("desactivateAnswers")
    else:
        return
    
    if rooms[id]["connected"][login] is None:
        rooms[id]["connected"][login] = answers
        if isinstance(answers, list):
            for a in answers:
                rooms[id]["totalAnswers"][a] += 1
        else:
            if answers in rooms[id]["totalAnswers"]:
                rooms[id]["totalAnswers"][answers] += 1
            else:
                rooms[id]["totalAnswers"][answers] = 1


@socketio.on("showCorrection")
def sendCorrection(id):
    if session.get("loginP") == rooms[id]["creator"] and not rooms[id]["corrected"]:
        emit("showCorrection", getCorrection(id), to=id)
        rooms[id]["corrected"] = True

@socketio.on("showLiveAnswers")
def sendLiveAnswers(id):
    if session.get("loginP") == rooms[id]["creator"] and not rooms[id]["liveAnswersShown"]:
        emit("showLiveAnswers", getLiveAnswers(id), to=id)
        rooms[id]["liveAnswersShown"] = True

@socketio.on("stopAnswers")
def stopAnswers(id):
    if session.get("loginP") == rooms[id]["creator"] and rooms[id]["answersOpen"]:
        rooms[id]["answersOpen"] = False
        emit("desactivateAnswers", to=id)

def getCorrection(rId):
    if "numeralAnswer" in rooms[rId]["activeQuestion"]:
        return json.dumps(rooms[rId]["activeQuestion"]["numeralAnswer"], indent=4)
    else:
        corrects = []
        i = 0
        answers = rooms[rId]["activeQuestion"]["answers"]
        for i in range(0, len(answers)):
            if answers[i]["val"]:
                corrects.append(i)
            i += 1
        print(corrects)
        return json.dumps(corrects, indent=4)
    
def getLiveAnswers(rId):
    nbAns = rooms[rId]["nbAns"]
    if "numeralAnswer" in rooms[rId]["activeQuestion"]:
        fiveMostAnswered = ["None"]*5
        fiveMostAnsweredQuant = [0]*5
        if nbAns == 0 :
            return json.dumps([fiveMostAnswered, fiveMostAnsweredQuant], indent=4)
        for key, value in rooms[rId]["totalAnswers"]:
            for i in range(0, 5):
                if value > fiveMostAnsweredQuant[i]:
                    fiveMostAnsweredQuant.insert(i, value)
                    fiveMostAnswered.insert(i, key)
                    fiveMostAnsweredQuant.pop()
                    fiveMostAnswered.pop()
                    break
        for e in fiveMostAnsweredQuant:
            e = (e/nbAns)*100
        return json.dumps([fiveMostAnswered, fiveMostAnsweredQuant], indent=4)
    else:
        givenAnswers = rooms[rId]["totalAnswers"]
        percents = []
        if nbAns == 0 :
            return json.dumps([0]*len(givenAnswers), indent=4)
        for a in givenAnswers:
            percents.append((a/nbAns)*100)
        return json.dumps(percents, indent=4)


@socketio.on('message')
def handle_message(data):
    print("######################################################################################################")
    print('received message: ' + data["m"] + " from " + session.get("loginP"))
    print("######################################################################################################")



