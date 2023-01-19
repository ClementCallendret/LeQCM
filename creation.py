from flask import Blueprint, Flask, request, redirect, url_for,render_template
import fileIO

crea = Blueprint('creation',__name__)

@crea.route('/MesQuestions')
def init():
    return render_template('MesQuestions.html')

@crea.route('/MesQuestions',methods = ['POST'])
def creation():
    listeQ = []
    print("let's gooooo")
    print(request.form)
    if (request.method == 'POST'):
        for key,value in request.form.items():
            listeQ.append(key)
            print("clé",key)
            print(value)
        print(listeQ)
        res = []
        #for idQuestion in listeQ:
        #    result.append(read(idQuestion))
        res = [{'id' : 1, 'title' : 'titre', 'state' : 'Si A = B Samy est bg', 'answers':[{'val' : True, 'text' : 'je pense que A = B'},{'val' : False, 'text' : 'je pense que A != B'}], 'tags' : ['beau', 'moche sa mère']},
            {'id' : 2, 'title' : 'titre2', 'state' : 'Si A = B Samy est moche sa mère', 'answers':[{'val' : False, 'text' : 'je pense que A != B2'},{'val' : True, 'text' : 'je pense que A = B2'}],'tags' : ['moche sa mère', 'moche de fou']}
            ]
        if (listeQ != []):
            return render_template("creation.html",res = res) 
    return render_template('MesQuestions.html') 
