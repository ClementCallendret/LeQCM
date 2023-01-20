from flask import Blueprint, request,session, render_template

connect = Blueprint('connected',__name__)

@connect.route('/connected/<login>')
def connected(login):
    return render_template("connected.html", login=login)

def isConnected():
    if (session['login']==""):
        return False
    else:
        return True