from flask import Flask, redirect, url_for, request, Blueprint,render_template, flash
import database

regist = Blueprint('register',__name__)

@regist.route('/register')
def init():
    return render_template('register.html')

@regist.route('/register',methods = ['POST'])
def register():
    if (request.method == 'POST'):
        login = request.form.get('login')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        if (password == cpassword):
            if (database.addProfessor(login,password)):
                return redirect(url_for('login.init'))
            else :
                flash('Utilisateur déjà enregistré')
        else:
            flash('Les deux mots de passes sont différent')

    return render_template('register.html')