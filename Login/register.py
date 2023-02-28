from flask import Flask, redirect, url_for, request, Blueprint,render_template, flash
import database
import encryption

register = Blueprint('register',__name__)

@register.route('/register')
def init():
    return render_template('register.html')

@register.route('/register',methods = ['POST'])
def registerRoute():
    if (request.method == 'POST'):
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')
        surname = request.form.get('surname')
        cpassword = request.form.get('cpassword')
        if (password == cpassword):
            tab = encryption.encrypt(password)
            password = tab[0]
            sel = tab[1]
            if (database.addProfessor(login, name, surname, password, sel)):
                return redirect(url_for('login.init'))
            else :
                flash('Utilisateur déjà enregistré')
        else:
            flash('Les deux mots de passes sont différent')

    return render_template('register.html')
