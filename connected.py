from flask import Flask, Blueprint, request,session

connect = Blueprint('connected',__name__)

@connect.route('/connected/<login>')
def connected(login):
    return 'Bienvenue ' + login

def isConnected():
    if (session['login']==""):
        return False
    else:
        return True