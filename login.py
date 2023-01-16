from flask import Flask, redirect, url_for, request

@app.route('login',methods = ['POST','GET'])
def login():
    if (methods.request == 'POST'):
        login = request.form['name']
        password = request.form['password']
        #Rechercher si login dans base de données
        #rechercher si password correspond
        if (fileIO.lofin.check([login,password])):
                #afficher son compte

                #supprimer le print quand l'affichage est fait
                print("It's workingg")
