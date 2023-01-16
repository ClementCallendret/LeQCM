from flask import Flask, redirect, url_for, request

@app.route('register',methods = ['POST','GET'])
def register():
    if (methods.request == 'POST'):
        login = request.form['name']
        password = request.form['password']
        #entrer name + password dans fichier txt
        fileIO.login.add([login,password])
