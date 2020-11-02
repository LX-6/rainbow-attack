#!/usr/bin/env python3
#title          :rainbowattack_main.py
#description    :Rainbow attack script for sha256 hash function
#author         :Jonathan Chabaud & Alexis Chemin
#date           :October 2020
#version        :1.0
#usage          :python3 rainbowattack_main.py -h
#python version :3.8.1

import rainbowattack_util as util
import string
import time
import argparse
import multiprocessing

# ====================
#       ARGUMENTS
# ====================

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--range", help="Length range of the password to crack. -r {minimum length} {maximum length}", nargs=2, type=int, default=[8,8])
parser.add_argument("-s", "--size", help="Size of the table. -s {column number} {chain number}", nargs=2, type=int, default=[1000,5000])
parser.add_argument("-l", "--load", help="Load an external rainbow table. -l {rainbow table}")

#Seul l'un de ses arguments peut être passé
group = parser.add_mutually_exclusive_group()
group.add_argument("-i", "--importhash", help="Import hashes to crack file. -i {hashes file}")
group.add_argument("-g", "--generate", help="Generate a number of hash to crack. -g {number of hash to crack}", type=int, default=100)


# ====================
#       FUNCTIONS
# ====================

#Prend un hash à cracker en entrée et retourne le mot de passe du hash s'il est présent dans la table
def crack_hash(r_table, hash_to_crack):
    #On répète l'opération en prenant l'indice du nombre de colonnes dans la chaine moins 1 et on décroissant vers 0
    #Ex : Si r_table.column_number=1000, le premier indice_col sera 999 puis 998, ainsi de suite jusqu'à 0
    for indice_col in range(r_table.column_number-1, -1, -1):
        tmp_hash = hash_to_crack
        #On répète l'opération le nombre de fois nécessaire pour que notre tmp_hash retombe sur le hash de tête
        for indice_reduction in range(indice_col, r_table.column_number):
            #On réduit le hash en un mot de passe puis on le hash
            tmp_hash = util.do_hash(util.reduction(tmp_hash, r_table.password_len, indice_reduction-1, r_table.chars_set))
        #Si le hash est présent dans la table
        if tmp_hash in r_table.table:
            #On remonte la chaine pour trouver le mot de passe du hash à cracker
            password = back_up_chain(r_table, hash_to_crack, r_table.table[tmp_hash])
            #Si on a trouvé un mot de passe
            if password:
                #On retourne le mot de passe
                return password

#Retourne le mot de passe cracké si on a réussi à le retrouver
def back_up_chain(r_table, hash_to_crack, password):
    #On répète l'opération pour le nombre de colonnes présentes
    for indice_col in range(r_table.column_number):
        #On hash le mot de passe
        tmp_hash = util.do_hash(password)
        #On compare si le hash du mot de passe correspondant au hash du mot de passe à cracker
        if tmp_hash == hash_to_crack:
            #Si les deux hash sont identiques on retourne le mot de passe
            return password
        #On réduit le hash pour obtenir le mot de passe suivant
        password = util.reduction(tmp_hash, r_table.password_len, indice_col, r_table.chars_set)

    #On retourne None si on a pas trouvé de correspondance
    return None

#Lance un nombre défini de test et affiche le résultat
def test_attack(nb_test, input_hash_filename, table):
    #Initialisation du compteur de réussite
    cmp_success = 0
    start_time = time.time()

    #Si un fichier de hashes est passé en paramètre
    if input_hash_filename:
        #On lit le fichier contenant les hashes à cracker
        with open(input_hash_filename) as f:
            hash_list = f.read().splitlines()
        f.close()
        # On crée un objet itérable de longueur équivalente au nombre de hashes à cracker
        args = util.Args(table, hash_list=hash_list)
    #Sinon on crée un objet itérable de longueur équivalente au nombre de test à effectuer
    else:
        args = util.Args(table, nb_test=nb_test)

    #On initialise le pool
    pool = multiprocessing.Pool(len(os.sched_getaffinity(0)))
    #On lance l'attaque pour tous les hashes en multiprocessing
    result = pool.map(crack_process, args)
    pool.close()

    #On récupère le nimbre de succès
    cmp_success = len(list(filter(None, result)))

    #On calcule le temps écoulé depuis le début de l'attaque
    duration = time.time() - start_time
    #On affiche le résultat de tous les tests
    print("\nResults : " + str(cmp_success) + "/" + str(nb_test) + " of crack success !")
    print("Cracking test lasted " + str(int(duration/60)) + " minutes and " + str(round(duration%60)) + " seconds")

#Crack le hash passé en paramètre, crée et crack un hash généré si aucun hash n'est passé en paramètre
def crack_process(args):

    #On essaie de récupérer le hash à cracker
    try:
        hash_to_crack, table = args
        pass_to_crack = None
    #S'il n'a pas été passé en argument nous le générons
    except:
        table = args
        #On génère un mot de passe à cracker
        pass_to_crack = util.generate_password(table.password_len, table.chars_set)
        #On hash ce mot de passe
        hash_to_crack = util.do_hash(pass_to_crack)

    #On attaque le hash du mot de passe que l'on vient de générer
    pass_cracked = crack_hash(table, hash_to_crack)

    #Si le mot de passe a été retrouvé
    if pass_cracked:
        #Si le mot de passe a été généré on l'affiche pour vérifier que l'opération a bien fonctionné
        if pass_to_crack:
            print("\nPassword to crack is : sha256(" + pass_to_crack + ")=" + hash_to_crack)
            print("[S] I found the password : " + pass_cracked)
        else:
            print("\nHash to crack is : " + hash_to_crack)
            print("[S] I found the password : " + pass_cracked)
        #Incrémente le compteur de succès
        return 1
    else:
        if pass_to_crack:
            print("\nPassword to crack is : sha256(" + pass_to_crack + ")=" + hash_to_crack)
            print("[F] I did not find this password :(")
        else:
            print("\nHash to crack is : " + hash_to_crack)
            print("[F] I did not find this password :(")

# ====================
#       MAIN
# ====================

if __name__ == "__main__":

    arguments = parser.parse_args()

    #Set de caractères possible pour le mot de passe à trouver
    chars_set = string.ascii_letters + string.digits

    if arguments.load:
        #Initialisation de la table
        table = util.RainbowTable(None, chars_set, arguments.size[1], arguments.size[0], arguments.load)

        #Chargement de la table
        table.load()

        test_attack(arguments.generate, arguments.importhash, table)

    else:
        #On répète l'opération pour toutes les tailles de mot de passe indiqué par l'utilisateur
        for length in range(arguments.range[0], arguments.range[1]+1):

            print("\nFor length " + str(length) + " :\n")

            output_filename = 'RainbowTable_' + str(length) + '.pickle'

            #Initialisation de la table
            table = util.RainbowTable(length, chars_set, arguments.size[1], arguments.size[0], output_filename)

            #Génération de la table
            table.generate()

            #Attaque des hashes
            test_attack(arguments.generate, arguments.importhash, table)
