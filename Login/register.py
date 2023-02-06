from flask import Flask, redirect, url_for, request, Blueprint,render_template, flash
import database
import encryption

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
            tab = encryption.encrypt(password)
            password = tab[0]
            sel = tab[1]
            print(login, password,sel)
            print(database.addProfessor(login,password,sel))
            print(database.addProfessor(login,password,sel))
            if (database.addProfessor(login,password,sel) == False):
                return redirect(url_for('login.init'))
            else :
                flash('Utilisateur déjà enregistré')
        else:
            flash('Les deux mots de passes sont différent')

    return render_template('register.html')
