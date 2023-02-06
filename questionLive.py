from flask import render_template, request, Blueprint
from extension import socketio

# a installer : 
# flask-socketio
# eventlet

questionLive = Blueprint('questionLive',__name__)

@questionLive.route('/liveQ')
def liveQ():
    return render_template('AffichageQuestion.html')

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data["m"])
    socketio.emit('messageToClient', {"m" : "message bien recu"})