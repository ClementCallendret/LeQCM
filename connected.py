from flask import Flask, Blueprint, request

connect = Blueprint('connected',__name__)

@connect.route('/connected/<login>')
def connected(login):
    return 'Bienvenue ' + login
