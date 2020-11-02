import time
import random
import hashlib
import pickle
import multiprocessing
import os

class RainbowTable:
    def __init__(self, password_len, chars_set, chain_number, column_number, output_filename):

        self.table = {} #Dictionnaire qui associe le mot de passe et le hash
        self.password_len = password_len #Taille des mots de passe à cracker
        self.chars_set = chars_set #Echantillon de caractères possibles pour les mots de passe à cracker
        self.chain_number = chain_number #Nombre de chaines dans la table
        self.column_number = column_number #Nombre de colonnes dans la table
        self.output_filename = output_filename #Nom du fichier pickle de sortie

    def generate_chain(self, i):
        table = {}

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
        table[hashed] = head

        #On affiche à l'utilisateur le nombre de chaines créées jusque là
        if i % 1000 == 0:
            print("Number of chains already created : " + str(i))

        return table

    #Génère la rainbow table et la stocke dans un fichier pickle
    def generate(self):
        #Initialisation du chrono
        start_time = time.time()

        pool = multiprocessing.Pool(len(os.sched_getaffinity(0)))
        result = pool.map(self.generate_chain, range(self.chain_number))
        pool.close()

        for chain in result:
            self.table.update(chain)

        #On écrit la représentation pickle de l'objet "table" dans le fichier de sortie
        pickle.dump(self.table, open(self.output_filename, "wb"))

        #On calcule le temps écoulé depuis le début de la génération
        duration = time.time() - start_time

        #On affiche à l'utilisateur la durée de la génération de la table
        print("\nTable generation lasted " + str(int(duration/60)) + " minutes and " + str(round(duration%60)) + " seconds")

    #Lit la rainbow table depuis un fichier pickle
    def load(self):
        #Initialisation du chrono
        start_time = time.time()
        self.table = {}

        print("Loading rainbow table")
        self.table = pickle.load(open(self.output_filename, "rb"))
        #On récupère la longueur du mot de passe head de la première chaine
        self.password_len = len(list(self.table.values())[0])

        #On calcule le temps écoulé depuis le début de la lecture
        duration = time.time() - start_time

		#On affiche à l'utilisateur la durée de la lecture de la table
        print("\nTable loading lasted " + str(round(duration)) + " seconds")

class Args:
    def __init__(self, table, hash_list=None, nb_test=None):

        self.rainbow_table = table #Objet RainbowTable
        self.hash_list = hash_list #Liste des hashes à cracker
        self.nb_test = nb_test #Nombre de tests à effectuer

    #Dunder method qui itère l'objet Args
    def __iter__(self):
        return ArgsIterator(self)

class ArgsIterator:
    def __init__(self, args):

        self.current = 0 #Index courant
        self.args = args #Objet Args

        #Si l'objet Args ne contient pas une liste de hashes
        if args.hash_list is None:
            #Si l'objet Args ne contient pas un nombre de tests à effectuer
            if args.nb_test is None:
                #Erreur dans le paramétrage de la classe Args
                raise ValueError
            #Sinon le maximum d'itérations correspond au nombre de tests à effectuer
            else:
                self.max = args.nb_test
                self.return_tuple = False
        #Sinon le maximum d'itération correspond à la taille de la liste de hashes
        else:
            self.max = len(args.hash_list)
            self.return_tuple = True

    #Dunder method qui itère l'objet ArgsIterator
    def __iter__(self):
        return self

    #Dunder method qui retourne l'élément à l'index courant
    def __next__(self):
        #Si on est arrivé au bout de l'itération
        if self.current >= self.max:
            raise StopIteration

        #S'il faut retourner un tuple d'éléments
        if self.return_tuple:
            #Stocker l'index courant
            tmp_current = self.current
            #Avancer l'index
            self.current += 1
            #Retourner un tuple contenant le hash courant et l'objet RainbowTable
            return (self.args.hash_list[tmp_current], self.args.rainbow_table)
        #Sinon avancer l'index et retourner l'objet RainbowTable
        else:
            self.current += 1
            return self.args.rainbow_table

#Génère un mot de passe d'une longueur donnée
def generate_password(length, chars):
    return ''.join(random.choice(chars) for i in range(length))

#Transforme le hash en une chaîne de caractères
def reduction(hashed, length, i_col, chars):
    chars_number = len(chars)
    #On génère une clé à partir du hash et de l'indice de la colonne
    key = (int(hashed[:9], 16) ^ i_col) % (chars_number ** length)
    password = ""
    #On itère pour la taille du mot de passe souhaité
    for i in range(length):
        #On ajoute le caractère qui correspond à l'indice dans notre set de caractères
        password += chars[key % chars_number]
        key //= chars_number
    return password

#Retourne le hash sha256 de la chaine de caractères passées en paramètre
def do_hash(password):
	return hashlib.sha256(password.encode('ascii')).hexdigest()
