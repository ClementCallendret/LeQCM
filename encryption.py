import secrets
import string
import bcrypt
#Alors, oui on est pas en https, oui on est sur python, oui on utilise flask dinc c'est absolument pas sécurisé
#Mais j'aime la cryptographie, donc on aura une BDD bien sécurisée (j'espère)

#On encrypte
def poivre(password):
    #conversion du password en bytes
    password = bytes(password, encoding='utf-8')
    #initialisation poivre avec b devant comme ça c'est en byte
    pepper = b""
    #on prend 2 en longueur car après ça risque d'être long
    nbChiffre = 2
    for i in range(nbChiffre):
        #on prend des string digits comme ça 10 possibilités (a mutliplié par le nb de tour de boucle)
        pepper += ''.join(secrets.choice(string.digits))
    #on concatène le poivre avec notre password en clair
    passwordP = password + pepper
    return passwordP

    

def sel(passwordP):
    passwordP = bytes(passwordP, encoding='utf-8')
    #génération du sel
    salt = bcrypt.gensalt()

    #génération du hash
    passHash = bcrypt.hashpw(passwordP, salt)
    return passHash


def encrypt(password):
    #on poivre
    password = poivre(password)
    #on sel
    password = sel(password)
    return password

#On décrypte
def checkPass(login,password):

    #Idem pour le sel
    #bdd2.get.sel(login)
    listHashPotentiels = []
    hash = b""
    #car 100 possibiltés de poivrage
    for i in range(100):
        #On y passe en bytes avant d'enregistrer 
        hash = bytes(password+i)
        #on sale les 100 potentiels hash
        hash = (sel(hash))
        listHashPotentiels.append(hash, encoding='utf-8')
    
    #on vérifie si le hash de la bdd correpond a un des hash potentiels
    #si oui, c'est le bon mot de passe à l'origine

    #On va dans la base de donnée récupéré le hash du mdp avec son login

    #if (bdd.get.hash(login)) in listHashPotentiels:
    if (True):
        return True
    else:
        return False

    