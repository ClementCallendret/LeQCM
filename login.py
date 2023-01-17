from flask import Blueprint, Flask, request, redirect, url_for,render_template, flash
import fileIO
log = Blueprint('login',__name__)

@log.route('/login')
def init():
    return render_template('login.html')

@log.route('/login',methods = ['POST'])
def login():
    if (request.method == 'POST'):
        login = request.form.get('login')
        password = request.form.get('password')
        print(login)
        print(password)
        #Rechercher si login dans base de données
        #rechercher si password correspond 
        if (fileIO.login.check(login, password)):
            return redirect(url_for('connected.connected',login = login))
        else :
            print("mauvais login ou mdp")
            flash("Erreur mauvais identifiant ou mot de passe")
            return render_template('login.html') 


@log.route('/log/<login>')
def error(login):
    return 'Bienvenue ' + login

