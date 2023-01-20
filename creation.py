from flask import Blueprint, request,render_template
import fileIO
import dictTodictFormated

crea = Blueprint('creation',__name__)

@crea.route('/MesQuestions/creerQCM',methods = ['POST'])
def creation():
    listeQ = []
    print("let's gooooo")
    print(request.form)
    if (request.method == 'POST'):
        for key,value in request.form.items():
            listeQ.append(key)
        res = []
        #for ID in listeQ:
         #   res.append(fileIO.format.questionToDic(fileIO.question.read(ID)))
        print(res)
        res = [{'id' : 1, 'title' : 'titre', 'state' : 'Si A = B Samy est bg', 'answers':[{'val' : True, 'text' : 'je pense que A = B'},{'val' : False, 'text' : 'je pense que A != B'}], 'tags' : ['beau', 'moche sa mère']},
            {'id' : 2, 'title' : 'titre2', 'state' : '\n~~~mermaid\n graph LR\nA-->B\nB-->C\n~~~', 'answers':[{'val' : False, 'text' : 'je pense que A != B2'},{'val' : True, 'text' : 'je pense que A = B2'}],'tags' : ['moche sa mère', 'moche de fou']}
            ]
        res = dictTodictFormated.dictTodictFormated(res)
        print(res)
        if (listeQ != []):
            return render_template("creation.html",res = res) 
    return render_template('MesQuestions.html') 
