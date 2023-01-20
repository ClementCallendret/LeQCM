import markdown
import pygments

# la variable text correspondra à ce que l'on récupérera de la méthode POST provenant du cod html.
# OBJECTIF : renvoyer le contenu de cette variable au code html une fois bien traduite avec mermaid en l'occurence. 
def formatageMD(text):
    text = '\n'+text.replace('\r', '')
    html = markdown.markdown(text, extensions=['codehilite','fenced_code','md_mermaid'])
    return html