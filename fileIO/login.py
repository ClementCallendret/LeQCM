import fileIO
"""

fonctions de manipulation de données


"""


# crée un compte et l'inscrit dans le stockage

def create(account, password):
    # on initialise un bool(qui indique si le login est déja pris)
    exist=False
    # on charge le stockage (liste de couples login, mot de passe)
    data = fileIO.login.load()
    # on parcourt tout les couples itérativement
    for couple in data:
        # si on trouve un compte qui à le nom désiré
        if couple[0]==account:
            # on le met dans notre bool
            exist = True
            # retour sur console(dans un return pourrait servir)
            print('account already exists')
    # si il a pas été trouvé, sont va l'ajouté:
    if not(exist):
        # si ya personne qui a encore crée de compte
        if data=='':
            # on transforme data en une liste (la sauvegarde mange une liste)
            data = []
        #on ajoute a notre liste le couple identifiant mot de passe du nouvel utilisateur
        data.append([account, password])
        # on enregistre tout ça sur fichier
        fileIO.login.save(data)

# verifie si un mot de passe est le bon

def check(account, password):
    # on crée le bool de sortie
    out=False
    # on charge le stockage (liste de couples login, mot de passe)
    data = fileIO.login.load()
    # on parcourt tout les couples itérativement
    for couple in data:
        # si le couple qu'on observe est le même que celui dans le stockage
        if couple==[account, password]:
            # le mot de passe est le bon
            out = True
    # on retourne notre variable
    return out

# supprime un mot de passe

def remove(account):
    # on charge le stockage (liste de couples login, mot de passe)
    data = fileIO.login.load()
    # on initialise une liste qui contiendra les couples login, mot de passe après suppression
    newData=[]
    # on parcourt tout les couples itérativement
    for couple in data:
        # si le couple qu'on observe à un login différent de celui fournit, on l'inscrit dans la nouvelle liste
        if couple[0]!=account:
            newData.append(couple)
    # on sauvergarde la nouvelle liste
    fileIO.login.save(newData)


# change un mot de passe d'un compte dans le stockage 

def changePassword(account, newPassword):
    # on charge tout les couples login,mot de passe
    data = fileIO.login.load()
    # on parcours la liste itérativement
    for couple in data:
        # si l'identifant est celui a modifier:
        if couple[0]==account:
            # on change son mot de passe associé
            couple[1]=newPassword
    # on sauvegarde la liste de couples mise à jour
    fileIO.login.save(data)

"""

fonctions de chargement en mémoire / ecriture sur fichier


"""


# chargement et décodage d'une string en une liste de couples login, mot de passes
def load():
    #on ouvre le fichier contenenant les identifiants et les mots de passes
    with open('./static/login.txt', 'r') as file:
        # on split la string en  une liste de strings de login et mots de passes
        file = file.read()[:-1].split("\n\n\n")
        # si elle est pas vide:
        if file != ['']:
            # on split en sous listes login, mot de passe
            for i in range(len(file)):
                file[i] = file[i].split("\n\n")
            # on vire le dernier retour a la ligne(pour avoir une liste propre)
            file[-1][1] = file[-1][1].replace("\n", '')
        else:
            # si vide on met une liste vide (pour eviter une liste d'une string vide)
            file = []
        return file


# encodage de la liste de couple longin, mot de passe en une string pour l'inscrire dans un txt


def save(data):
    # on crée/ ouvre le fichier contenant les identifiants et les mots de passes
    with open('./static/login.txt', 'w') as file:
        # on crée la string de sortie
        out = ""
        # en parcourant la liste de couples login, mot de passes
        for couple in data:
            # en parcourant les elements de ces couples
            for item in couple:
                # on transforme chaque couple en une string, ou \n\n est utilisé en temps que séparateur
                out+= item + "\n\n"
            #on vire le dernier séparateur qui est en trop(pas d'éléments après)
            out=out[:-2]
            # on assembles les strings obtenues en une seule string avec \n\n\n comme séparateur
            out+="\n\n\n"
        out = out[:-3]
        print(out, file=file)