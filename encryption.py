import secrets
import string
import bcrypt
import database
#Alors, oui on est pas en https, oui on est sur python, oui on utilise flask avec le debug donc c'est absolument pas sécurisé
#Mais j'aime la cryptographie, donc on aura une BDD bien sécurisée (j'espère)

#On encrypte
def pepper(password):
    #conversion du password en bytes
    #POUR PLUS TARD pepper = int(secrets.choice(string.digits))

    pepper = (secrets.choice("01"))

    #on prend que 2 possibilité sinon c'est trop long a décoder après
    #on concatène le poivre avec notre password en clair
    passwordP = password + pepper
    return passwordP

    

def salt(passwordP):
    #génération du sel
    salt = bcrypt.gensalt()
    passwordP = (bytes(passwordP, encoding='utf-8'))
    #génération du hash
    passHash = ''
    passHash = bcrypt.hashpw(passwordP, salt)
    tab = [passHash,salt]
    return tab

#PRINCIPE :
#On prend le mdp, on lui ajoute le poivre, donc soit 0 soit 1. LE POIVRE N EST PAS STOCKE
#Puis on génère le sel, ON LE STOCKE PLUS TARD
#On passe le mdp poivré avec le sel
#On récupère le hash de tout ce beau monde
#On stocke le hash dans la BDD
def encrypt(password):
    #on poivre
    password = pepper(password)
    #on sel
    tab = salt(password)
    #on return le password poivré + salé et le sel
    return tab



#on sel avec le sel correspondant
def unsalt(passwordP,salt):
    #génération du hash
    passHash = bcrypt.hashpw(passwordP, salt)
    return passHash



#On poivre avec toutes les possibilités
def unpepper(password, salt):
    listHashPotentiels = []
    passwordP = b""
    #car 2 possibiltés de poivrage (0 et 1)
    for i in range(2):
        #On y passe en bytes avant d'enregistrer 
        passwordP = bytes(password + str(i), encoding='utf-8')

        #on sale les 2 potentiels hash
        passHash = unsalt(passwordP,salt)
        listHashPotentiels.append(passHash)
    return listHashPotentiels




#PRINCIPE:
#On récupère le sel du compte dans le BDD grâce au login
#On envoi le mdp et le sel dans la fonction unpepper
#la fonction unpepper crée tout les peppers possible (ici soit 0 soit 1),
#puis on sale les 2 mdp poivrés et on fait une liste avec les 2 hashs potentiels
#On test si un des 2 hashs potentiels correspond au hash stocké dans la BDD
#Si oui, c'est le bon mot de passe à l'origine, donc on renvoi TRUE
#Sinon, on renvoi FALSE

#On décrypte (STATUT = S SI STUDENT OU P SI PROFESSOR)
def decrypt(login,password,statut):
    #On récupère le sel de l'utilisateur
    salt = b""
    if (statut == 'P'):
        salt = database.getProfessorSel(login)
    elif (statut == 'S'):
        salt = database.getStudentSel(login)
    if (salt == None):
        return False
    #On fait la liste de tout les hashs potentiels
    listHashPotentiels = unpepper(password, salt)

    
    #on vérifie si le hash de la bdd correpond a un des hash potentiels
    #si oui, c'est le bon mot de passe à l'origine

    #On va dans la base de donnée récupéré le hash du mdp avec son login
    if (statut == 'P'):
        for i in range(2):
            if (database.matchProfessorPassword(login, listHashPotentiels[i])):
                return True
    elif (statut == 'S'):
        for i in range(10):
            if (database.matchStudentPassword(login, listHashPotentiels[i])):
                return True
    return False

    
