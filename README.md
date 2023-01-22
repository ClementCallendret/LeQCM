# LeQCM
Installation  :
-télécharger Python 3.8.10,Flask 2.2.2, pygments 2.10.0, markdown 3.2, md-mermaid 0.1.1

Lancement :
-Être dans le répertoire du projet
-executer dans le terminal : python3 main.py

Un QCM



Format et méthode de sauvegarde:

les questions sont enregistrées dans le stockage séparement.
Des identifiants leurs sont attribuées ainsi qu'un dossier d'istinct portant l'identifiant comme nom.

Chaque dossier est composé: 
 - d'un fichier question.txt, contenant l'énoncé.
 - d'un fichier title+answer.txt, contenant le titre est les questions justes.
 - de fichier ayant pour nom un entier, contenant les réponses dans l'odre, à raison d'une réponse par fichier.

Pour garder une trace des tags, créateurs et identifiants de chaques questions, il y a aussi un fichier question.txt hors du repertoire questions.
ce fichier est une table de ces valeurs. Il s'est avéré plus judicieux de procédé avec ce systeme, en raison de l'objectif même de cette application. En effet, cette application doit être conçue pour pouvoir contenir un très grand nombre de questions, ainsi il est impératif d'épargner la quantitée de mémoire utilisée(l'autre alternative étant de charger les données de chaque questions de la mémoire en tout temps).

les identifiants sont attribuées celon ces règles: 
 - si il n'y a pas de question a l'id 0: on l'a crée a cet identifiant.
 - si il y a un ecart entre deux valeurs (ex: 1-3): on comble ce trou
 - sinon, on créer une nouvelle question en suivant l'ordre numérique.

cette méthode permet de minimiser le nombre d'identifiant, tout en évitant de devoir reatribué les identifiants suivant a chaque fois qu'une question est supprimée.

lors de la recherche de questions, on interroge simplement la base (question.txt), lors de la recupperation des données complete d'une question, on les reccuppèrent directement dans le fichier portant son identifiant, et après un rapide formatage, elles sont transmisent plus haut pour êtres affichées et/ou traitées.

lors de la recherche de questions, on interroge simplement la base (question.txt), lors de la recupperation des données complete d'une question, on les reccuppèrent directement dans le fichier portant son identifiant, et après un rapide formatage, elles sont transmisent plus haut pour êtres affichées et/ou traitées.