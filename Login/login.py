from flask import Blueprint, Flask, request, redirect, url_for,render_template, flash, session
import database
import encryption
login = Blueprint('login',__name__)



@login.route('/login')
def init():
    return render_template('login.html')

@login.route('/loginP',methods = ['POST'])
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
        if (encryption.decrypt(login, password, 'P')):
        #if(compteExisteProf(login,password))
            session.pop('loginP',None)
            session.pop('loginE',None)
            session['loginP']=login
            session.permanent = rememberMe
            return redirect(url_for('accueil'))
        else :
            print("mauvais login ou mdp")
            flash("Erreur mauvais identifiant ou mot de passe")
            return render_template('login.html') 


@login.route('/loginE',methods = ['POST'])
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
        if (encryption.decrypt(login, password, 'E')):
        #if(compteExisteEleve(login,password)):
            #ON VIDE LA SESSION AU CAS OU Y A UN PTIT MALIN(mais en temps normal ça sert à rien)
            session.pop('loginP',None)
            session.pop('loginE',None)
            session['loginE']=login
            session.permanent = rememberMe
            return redirect(url_for('accueil'))
        else :
            print("mauvais login ou mdp")
            flash("Erreur mauvais identifiant ou mot de passe")
            return render_template('login.html') 
