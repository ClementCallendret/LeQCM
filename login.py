from flask import Blueprint, request, redirect, url_for,render_template, flash, session
import fileIO

logi = Blueprint('login',__name__)

@logi.route('/login')
def init():
    return render_template('login.html')

@logi.route('/login',methods = ['POST'])
def login():
    if (request.method == 'POST'):
        login = request.form.get('login')
        password = request.form.get('password')
        rememberMe = request.form.get('rememberMe')
        test = request.form.get('test')
        print(test)

        #Pour la checkbox "Se souvenir de moi"
        if (rememberMe == "on"):
            rememberMe = True
        else:
            rememberMe = False
        #Rechercher si login dans base de données
        #rechercher si password correspond 
        if (fileIO.login.check(login, password)):
            session['login']=login
            print(rememberMe)
            session.permanent = rememberMe
            return redirect(url_for('accueil'))
        else :
            flash("Erreur mauvais identifiant ou mot de passe")
            return render_template('login.html') 


