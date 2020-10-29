#!/usr/bin/env python3

import rainbowattack_util as util
import string
import time
import argparse
import multiprocessing

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

def test_attack_process(table):
    #On génère un mot de passe à cracker
    pass_to_crack = util.generate_password(table.password_len, table.chars_set)
    #On hash ce mot de passe
    hash_to_crack = util.do_hash(pass_to_crack)
    print("\nPassword to crack is : sha256(" + pass_to_crack + ")=" + hash_to_crack)

    #On attaque le hash du mot de passe que l'on vient de générer
    pass_cracked = crack_hash(table, hash_to_crack)

    #Si le mot de passe a été retrouvé
    if pass_cracked:
        print("[S] I found the password : " + pass_cracked)
        #Incrémente le compteur de succès
        return 1
    else:
        print("[F] I did not find this password :(")

#Lance un nombre défini de test et affiche le résultat
def test_attack(nb_test, table):
    #Initialisation du compteur de réussite
    cmp_success = 0
    start_time = time.time()

    args = []
    for i in range(nb_test):
        args.append(table)

    #On réalise le nombre de test défini par l'utilisateur
    pool = multiprocessing.Pool()
    result = pool.map(test_attack_process, args)
    pool.close()

    # for i in range(nb_test):
    #     #On génère un mot de passe à cracker
    #     pass_to_crack = util.generate_password(table.password_len, table.chars_set)
    #     #On hash ce mot de passe
    #     hash_to_crack = util.do_hash(pass_to_crack)
    #     print("\nPassword to crack is : sha256(" + pass_to_crack + ")=" + hash_to_crack)
    #
    #     #On attaque le hash du mot de passe que l'on vient de générer
    #     pass_cracked = crack_hash(table, hash_to_crack)
    #
    #     #Si le mot de passe a été retrouvé
    #     if pass_cracked:
    #         print("[S] I found the password : " + pass_cracked)
    #         #Incrémente le compteur de succès
    #         cmp_success += 1
    #     else:
    #         print("[F] I did not find this password :(")

    #On calcule le temps écoulé depuis le début de l'attaque
    duration = time.time() - start_time
    #On affiche le résultat de tous les tests
    print("\nResults : " + str(cmp_success) + "/" + str(nb_test) + " of crack success !")
    print("Cracking test lasted " + str(int(duration/60)) + " minutes and " + str(round(duration%60)) + " seconds")

def test_attack_load_process(args):
    hash_to_crack, table = args

    print("\nHash to crack is : " + hash_to_crack)

    #On attaque le hash
    pass_cracked = crack_hash(table, hash_to_crack)

    #Si le mot de passe a été retrouvé
    if pass_cracked:
        print("[S] I found the password : " + pass_cracked)
        #Incrémente le compteur de succès
        return 1
    else:
        print("[F] I did not find this password :(")

#Teste des hash fournis en entrée et affiche le résultat
def test_attack_load(input_hash_filename, table):
    #Initialisation du compteur de réussite
    cmp_success = 0
    start_time = time.time()

    #On lit le fichier contenant les hash à cracker
    with open(input_hash_filename) as f:
        hash_list = f.read().splitlines()
    f.close()

    args = []
    for hash_to_crack in hash_list:
        args.append((hash_to_crack, table))

    pool = multiprocessing.Pool()
    result = pool.map(test_attack_load_process, args)
    pool.close()

    cmp_success = len(list(filter(None, result)))

    # #Pour chaque hash à cracker dans le fichier
    # for hash_to_crack in hash_list:
    #     print("\nHash to crack is : " + hash_to_crack)
    #
    #     #On attaque le hash
    #     pass_cracked = crack_hash(table, hash_to_crack)
    #
    #     #Si le mot de passe a été retrouvé
    #     if pass_cracked:
    #         print("[S] I found the password : " + pass_cracked)
    #         #Incrémente le compteur de succès
    #         cmp_success += 1
    #     else:
    #         print("[F] I did not find this password :(")

    #On calcule le temps écoulé depuis l'attaque
    duration = time.time() - start_time
    #On affiche le résultat de tous les tests
    print("\nResults : " + str(cmp_success) + "/" + str(len(hash_list)) + " of crack success !")
    print("Cracking test lasted " + str(int(duration/60)) + " minutes and " + str(round(duration%60)) + " seconds")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loadtable", help="Load an external rainbow table", action="store_true")
    parser.add_argument("-lh", "--loadhash", help="Perform tests with hash from a file", action="store_true")
    parser.add_argument("-c", "--column", help="Column number", type=int, default=1000)
    parser.add_argument("-ch", "--chain", help="Chains number", type=int, default=5000)
    parser.add_argument("-min", "--minimum", help="Minimum length of the password to crack", type=int, default=8)
    parser.add_argument("-max", "--maximum", help="Maximum length of the password to crack", type=int, default=12)
    parser.add_argument("-f", "--tablefile", help="Rainbow table pickle file", required=True)
    parser.add_argument("-t", "--test", help="Number of test to perform", type=int, default=100)
    parser.add_argument("-hf", "--hashfile", help="Hash to crack file")
    arguments = parser.parse_args()

    #Set de caractères possible pour le mot de passe à trouver
    chars_set = string.ascii_letters + string.digits

    if arguments.loadtable:
        #Initialisation de la table
        table = util.RainbowTable(arguments.minimum, chars_set, arguments.chain, arguments.column, arguments.tablefile)

        #Chargement de la table
        table.load()

        #Test de l'attaque
        if arguments.loadhash:
            #Lire les hash depuis un fichier
            try:
                if arguments.hashfile is None:
                    raise ValueError
                test_attack_load(arguments.hashfile, table)
            except ValueError:
                print("Please specify argument --hashfile (-h for help)")
        else:
            #Générer les hash aléatoirement
            test_attack(arguments.test, table)

    else:
        for length in range(arguments.minimum, arguments.maximum+1):
            print("\nFor length " + str(length) + " :\n")

            output_filename = arguments.tablefile + '_' + str(length) + '.pickle'
            #Initialisation de la table
            table = util.RainbowTable(length, chars_set, arguments.chain, arguments.column, output_filename)

            #Génération de la table
            table.generate()

            #Test de l'attaque
            if arguments.loadhash:
                #Lire les hash depuis un fichier
                test_attack_load(arguments.hashfile, table)
            else:
                #Générer les hash aléatoirement
                test_attack(arguments.test, table)
