import time
import random
import hashlib
import pickle
from vm_test_rainbowattack_main import logger

class RainbowTable:
    def __init__(self, password_len, chars_set, chain_number, column_number, output_filename):
        
        self.table = {} #Dictionnaire qui associe le mot de passe et le hash
        self.password_len = password_len #Taille des mots de passe à cracker
        self.chars_set = chars_set #Echantillon de caractères possibles pour les mots de passe à cracker
        self.chain_number = chain_number #Nombre de chaines dans la table
        self.column_number = column_number #Nombre de colonnes dans la table
        self.output_filename = output_filename #Nom du fichier pickle de sortie

    #Génère la rainbow table et la stocke dans un fichier pickle
    def generate(self):
        #Initialisation du chrono
        start_time = time.time()

        #On répète pour le nombre de chaines de notre table
        for i in range(self.chain_number):

            #On génère le mot de passe en tête de chaine
            head = generate_password(self.password_len, self.chars_set)

            password = head

            #On répète pour le nombre de colonnes dans notre chaine
            for j in range(self.column_number):
                #On hash le mot de passe
                hashed = do_hash(password)
                #On applique la fonction de réduction sur le hash du mot de passe
                password = reduction(hashed, self.password_len, int(j), self.chars_set)

            #On stocke le dernier hash "tail" et notre mot de passe de tête dans notre dictionnaire
            self.table[hashed] = head

            #On affiche à l'utilisateur le nombre de chaines créées jusque là
            if i % 1000 == 0:
                logger.info("Number of chains already created : " + str(i))

        #On écrit la représentation pickle de l'objet "table" dans le fichier de sortie
        pickle.dump(self.table, open(self.output_filename, "wb"))

        #On calcule le temps écoulé depuis le début de la génération
        duration = time.time() - start_time

        #On affiche à l'utilisateur la durée de la génération de la table
        logger.info("\nTable generation lasted " + str(int(duration/60)) + " minutes and " + str(round(duration%60)) + " seconds")

#Génère un mot de passe d'une longueur donnée
def generate_password(length, chars):
    return ''.join(random.choice(chars) for i in range(length))

#Transforme le hash en une chaîne de caractères
def reduction(hashed, length, i_col, chars):
    #On génère une clé à partir du hash et de l'indice de la colonne
    key = (int(hashed[:9], 16) ^ i_col) % (len(chars) ** length)
    password = ""
    #On itère pour la taille du mot de passe souhaité
    for i in range(length):
        #On ajoute le caractère qui correspond à l'indice dans notre set de caractères
        password += chars[key % len(chars)]
        key //= len(chars)
    return password

#Retourne le hash sha256 de la chaine de caractères passées en paramètre
def do_hash(password):
	return hashlib.sha256(password.encode('ascii')).hexdigest()