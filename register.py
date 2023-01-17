from flask import Flask, redirect, url_for, request, Blueprint,render_template, flash
import fileIO

regist = Blueprint('register',__name__)

@regist.route('/register')
def init():
    return render_template('register.html')

@regist.route('/register',methods = ['POST','GET'])
def register():
    if (request.method == 'POST'):
        login = request.form['name']
        password = request.form['password']
        if (not (fileIO.login.check(login,register))):
            fileIO.login.create(login,password)
            return redirect(url_for('login'))
        else :
            flash('Utilisateur inconnu')
        return render_template('register.html')
