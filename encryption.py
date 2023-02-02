import secrets
import string
import bcrypt
import database
#Alors, oui on est pas en https, oui on est sur python, oui on utilise flask dinc c'est absolument pas sécurisé
#Mais j'aime la cryptographie, donc on aura une BDD bien sécurisée (j'espère)

#On encrypte
def pepper(password):
    #conversion du password en bytes
    password = bytes(password, encoding='utf-8')
    #initialisation poivre avec b devant comme ça c'est en byte
    pepper = b""
    #on prend 2 en longueur car après ça risque d'être long
    nbChiffre = 2
    for i in range(nbChiffre):
        #on prend des string digits comme ça 10 possibilités (a mutliplié par le nb de tour de boucle)
        pepper = pepper + (bytes(secrets.choice(string.digits),encoding='utf-8'))
    #on concatène le poivre avec notre password en clair
    passwordP = password + pepper
    return passwordP

    

def salt(passwordP):
    print("PASSWORDP: ", passwordP)
    #génération du sel
    salt = bcrypt.gensalt()

    #génération du hash
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
def unsalt(passwword,salt):
    passwordP = bytes(password, encoding='utf-8')

    #génération du hash
    passHash = bcrypt.hashpw(passwordP, salt)
    return passHash



#On poivre avec toutes les possibilités
def unpepper(password, salt):
    listHashPotentiels = []
    hash = b""
    #car 100 possibiltés de poivrage
    for i in range(100):
        #On y passe en bytes avant d'enregistrer 
        print("PASSWORDP: ", password)

        passwordP = password + bytes(i)

        #on sale les 100 potentiels hash
        passHash = unsalt(passwordP,salt)
        listHashPotentiels.append(passHash, encoding='utf-8')

#On décrypte (STATUT = S SI STUDENT OU P SI PROFESSOR)
def decrypt(login,password,statut):
    #On récupère le sel de l'utilisateur
    salt = b""
    if (statut == 'P'):
        salt = database.getProfessorSel(login)
    elif (statut == 'S'):
        salt = database.getStudentSel(login)

    listHashPotentiels = unpepper(password, salt)
    
    #on vérifie si le hash de la bdd correpond a un des hash potentiels
    #si oui, c'est le bon mot de passe à l'origine

    #On va dans la base de donnée récupéré le hash du mdp avec son login
    if (statut == P):
        for i in range(100):
            if (databse.matchProfessorPassword(login, listHashPotentiels[i])):
                return True
    elif (statut == S):
        for i in range(100):
            if (database.matchStudentPassword(login, listHashPotentiels[i])):
                return True
    return False

    
