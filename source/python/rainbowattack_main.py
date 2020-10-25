import rainbowattack_util as util
import string
import time

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

#Test l'attaque sur un mot de passe généré aléatoirement
def test(table):

    password = util.generate_head(table.password_len, table.chars_set)
    hash_to_crack = util.do_hash(password)
    print("\nCracking password: {0}\nH(password): {1}".format(password, hash_to_crack))

    cracked = crack_hash(table, hash_to_crack)
    if cracked:
        print("Success! Password: {0}".format(cracked))
        return True
    else:
        print("Unsuccessful :(")
        return False

#Lance un nombre défini de test et affiche le résultat
def bulk_test(table, numTests):
	start = time.time()
	numSuccess = 0

	for i in range(numTests):
		print("\nTest {0} of {1}".format(i + 1, numTests))
		numSuccess += test(table)

	print("""\n{0} out of {1} random hashes were successful!\n
Average time per hash (including failures): {2} secs.""" \
		.format(numSuccess, numTests, (time.time() - start) / numTests))


if __name__ == "__main__":

    #Set de caractères possible pour le mot de passe à trouver
    chars_set = string.ascii_letters + string.digits
    password_len = 4
    chain_number = 5000
    column_number = 1000
    output_filename = 'RainbowTable.pickle'

    #Table initialisation
    table = util.RainbowTable(password_len, chars_set, chain_number, column_number, output_filename)

    #Generate table
    table.generate()

    bulk_test(table, 100)