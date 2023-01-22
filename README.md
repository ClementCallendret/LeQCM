# LeQCM
Installation  : 
    télécharger :
    - Python 3.8.10
    - Flask 2.2.2
    - pygments 2.10.0
    - markdown 3.2
    - md-mermaid 0.1.1

Lancement :
 - Être dans le répertoire du projet
 - éxecuter dans le terminal : python3 main.py



Format et méthode de sauvegarde:

Les questions sont enregistrées dans le stockage séparement.
Des identifiants leurs sont attribuées ainsi qu'un dossier distinct portant l'identifiant comme nom.

Chaque dossier est composé: 
 - d'un fichier question.txt, contenant l'énoncé.
 - d'un fichier title+answer.txt, contenant le titre et les questions justes.
 - de fichier ayant pour nom un entier, contenant les réponses dans l'ordre, à raison d'une réponse par fichier.

Pour garder une trace des tags, créateurs et identifiants de chaques questions, il y a aussi un fichier question.txt hors du repertoire questions.
ce fichier est une table de ces valeurs. Il s'est avéré plus judicieux de procéder avec ce systeme, en raison de l'objectif même de cette application. En effet, cette application doit être conçue pour pouvoir contenir un très grand nombre de questions, ainsi il est impératif d'épargner la quantitée de mémoire utilisée(l'autre alternative étant de charger les données de chaque questions de la mémoire en tout temps).

les identifiants sont attribuées selon ces règles: 
 - si il n'y a pas de question à l'id 0: on la crée à cet identifiant.
 - si il y a un ecart entre deux valeurs (ex: 1-3): on comble ce trou.
 - sinon, on crée une nouvelle question en suivant l'ordre numérique.

cette méthode permet de minimiser le nombre d'identifiant, tout en évitant de devoir reatribué les identifiants suivant à chaque fois qu'une question est supprimée.

lors de la recherche de questions, on interroge simplement la base (question.txt), lors de la recupération des données complètes d'une question, on les récupère directement dans le fichier portant son identifiant, et après un rapide formatage, elles sont transmises plus haut pour êtres affichées et/ou traitées.
