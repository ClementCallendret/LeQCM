import secrets
import string
import bcrypt
import database
#Alors, oui on est pas en https, oui on est sur python, oui on utilise flask dinc c'est absolument pas sécurisé
#Mais j'aime la cryptographie, donc on aura une BDD bien sécurisée (j'espère)

#On encrypte
def pepper(password):
    #conversion du password en bytes
    pepper = int(secrets.choice(string.digits))
    #SINON CA PREND TROP LONGTEMPS :(
    if (pepper>4):
        pepper = "0"
    else :
        pepper= "1"
    #on prend des string digits comme ça 10 possibilités, mais du coup plus que 2
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


def encrypt(password):
    #on poivre
    password = pepper(password)
    #on sel
    tab = salt(password)
    #on return le password salé + poivré et le sel
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
    #car 10 possibiltés de poivrage
    for i in range(2):
        #On y passe en bytes avant d'enregistrer 
        passwordP = bytes(password + str(i), encoding='utf-8')

        #on sale les 100 potentiels hash
        passHash = unsalt(passwordP,salt)
        listHashPotentiels.append(passHash)
    return listHashPotentiels

#On décrypte (STATUT = S SI STUDENT OU P SI PROFESSOR)
def decrypt(login,password,statut):
    #On récupère le sel de l'utilisateur
    salt = b""
    if (statut == 'P'):
        salt = database.getProfessorSel(login)
    elif (statut == 'S'):
        salt = database.getStudentSel(login)

    if (salt == False):
        return False
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

    
