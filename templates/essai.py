from flask import Flask, render_template, request, redirect, url_for

import markdown

import base64     










app = Flask(__name__)

@app.route('/')
def md(): # la variable text correspondra à ce que l'on récupérera de la méthode POST provenant du code html.
                  # OBJECTIF : la renvoyer au code html une fois bien traduite avec mermaid en l'occurence. 
  text = """ 
  # AAAAAAAAAA

  Bruh

  ~~~mermaid
  pie title Camembert qui montre a quel point Clément est bg
            "incroyablement beau" : 88
            "Ignoble" : 12
  ~~~

  ~~~mermaid
  graph TB
  A --> B
  B --> C
  ~~~

  Some other text.

  ~~~mermaid
  graph TB
  D --> E
  E --> F
  ~~~
  """

  html = text.markdown(extensions=['md_mermaid'])

  

  return render_template('blabla.html', mark = html)




app.run(host='0.0.0.0', port=5555)
