from flask import Blueprint, Flask, request, redirect, url_for,render_template

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
        #rechercher si password correspond #fileIO.lofin.check([login,password])
        if (True):
                #afficher son compte
                print("login marche")
                return redirect(url_for('connected.connected',login = login))




