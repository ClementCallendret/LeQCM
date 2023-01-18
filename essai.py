from flask import Flask, render_template, request, redirect, url_for

import markdown
import md_mermaid, pylatex

import base64     
app = Flask(__name__)

def mermaidTranslator(str):
    newstr = str.replace(r"\n", "\n")

    return newstr



@app.route('/', methods=['POST', 'GET'])
def md(): # la variable text correspondra à ce que l'on récupérera de la méthode POST provenant du code html.
                  # OBJECTIF : renvoyer le contenu de cette variable au code html une fois bien traduite avec mermaid en l'occurence. 
  text = r"""

  \n##CLEMENT porte des SALOPETTE C'est du markdownnnn\n

  **The Cauchy-Schwarz Inequality**
  $$\left( \sum_{k=1}^n a_k b_k \\right)^2 leq \\left( sum_{k=1}^n a_k^2 \\right) \left( sum_{k=1}^n b_k^2 \\right)$$

  \n~~~mermaid\ngraph TB\nA --> B\nB --> C\n~~~\n

  \n~~~mermaid\ngraph TB\nD --> E\nE --> F\n~~~\n

  \n~~~mermaid\npie title Camembert qui montre a quel point Clement est bg\n"incroyablement beau" : 85\n"Ignoble" : 15\n~~~\n

  $$V_{sphere} = \frac{4}{3}\pi r^3$$

  $$V_{cube} = l w h $$

  """
  text = mermaidTranslator(text)
  print(text)

  html = markdown.markdown(text, extensions=['md_mermaid'])

  return render_template('blabla.html', mark = html)






app.run(host='0.0.0.0', port=5555, debug=True)
