from flask import Flask, redirect, url_for, request
import main

@app.route('register',methods = ['POST','GET'])
def register():
    if (methods.request == 'POST'):
        login = request.form['name']
        password = request.form['password']
        #entrer name + password dans fichier txt
        fileIO.login.add([login,password])
        return redirect(url_for('connected',login = login))
