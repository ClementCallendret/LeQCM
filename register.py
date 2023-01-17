from flask import Flask, redirect, url_for, request, Blueprint,render_template

regist = Blueprint('register',__name__)

@regist.route('/register')
def init():
    return render_template('register.html')

@regist.route('/register',methods = ['POST','GET'])
def register():
    if (request.method == 'POST'):
        login = request.form['name']
        password = request.form['password']
        #entrer name + password dans fichier txt
        #fileIO.login.add([login,password])
        print("register marche")
        return redirect(url_for('login',login = login))
