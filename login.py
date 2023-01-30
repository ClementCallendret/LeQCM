from flask import Blueprint, Flask, request, redirect, url_for,render_template, flash, session
import fileIO

logi = Blueprint('login',__name__)



@logi.route('/login')
def init():
    return render_template('login.html')

@logi.route('/loginP',methods = ['POST'])
def loginP():
    if (request.method == 'POST'):
        login = request.form.get('loginP')
        password = request.form.get('passwordP')
        rememberMe = request.form.get('rememberMeP')
        #Pour la checkbox "Se souvenir de moi"
        if (rememberMe == "on"):
            rememberMe = True
        else:
            rememberMe = False
        #Rechercher si login dans base de données
        #rechercher si password correspond 
        if (fileIO.login.check(login, password)):
        #if(compteExisteProf(login,password))
            session['loginP']=login
            session.permanent = rememberMe
            return redirect(url_for('accueil'))
        else :
            print("mauvais login ou mdp")
            flash("Erreur mauvais identifiant ou mot de passe")
            return render_template('login.html') 


@logi.route('/loginE',methods = ['POST'])
def loginE():
    if (request.method == 'POST'):
        login = request.form.get('loginE')
        password = request.form.get('passwordE')
        rememberMe = request.form.get('rememberMeE')
        #Pour la checkbox "Se souvenir de moi"
        if (rememberMe == "on"):
            rememberMe = True
        else:
            rememberMe = False
        print("Etu :",login,password,rememberMe)
        #Rechercher si login dans base de données
        #rechercher si password correspond 
        if (fileIO.login.check(login, password)):
        #if(compteExisteEleve(login,password)):
            session['loginE']=login
            session.permanent = rememberMe
            return redirect(url_for('accueil'))
        else :
            print("mauvais login ou mdp")
            flash("Erreur mauvais identifiant ou mot de passe")
            return render_template('login.html') 
