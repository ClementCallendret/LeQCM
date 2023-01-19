from flask import Flask, render_template, request, redirect, url_for, Blueprint
import pygments
import markdown
import md_mermaid

import base64     




interpreteur = Blueprint('interpreteur',__name__)




@interpreteur.route('/interpreteur', methods=['POST', 'GET'])
def md(): # la variable text correspondra à ce que l'on récupérera de la méthode POST provenant du code html.
                  # OBJECTIF : renvoyer le contenu de cette variable au code html une fois bien traduite avec markdown(+mermaid et codehilite). 
  text = """ 

  \n##CLEMENT LE BEST\n

  \n~~~mermaid\ngraph TB\nA --> B\nB --> C\n~~~\n

  \n~~~mermaid\ngraph TB\nD --> E\nE --> F\n~~~\n
  """

  html = markdown.markdown(text, extensions=['codehilite','fenced_code','md_mermaid'])

  print(html)

  return render_template('blabla.html', mark = html)




