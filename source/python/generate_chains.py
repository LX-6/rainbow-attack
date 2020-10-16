#!/usr/bin/env python3
import argparse
import hashlib
import string
import random

#Set de caractères possible pour le mot de passe à trouver
chars = string.ascii_letters + string.digits
chars_len = len(chars)

#Génère un mot de passe d'une longueur donnée
def generate_head(length):
    return ''.join(random.choice(chars) for i in range(length))

#Créé une chaine en partant d'une string "head" et retourne le dernier élément de la chaine ("tail")
def create_chain(password, nb_boucle, longueur):
    for i in range(nb_boucle):
        #On hash le mot de passe
        hashed = hashlib.sha256(password.encode('ascii')).hexdigest()
        #On applique la fonction de réduction sur le hash du mot de passe
        password = reduce(hashed, longueur, int(i))

    #On retourne le hash du dernier password généré
    return hashlib.sha256(password.encode('ascii')).hexdigest()

#Transforme le hash en une chaîne de caractères
def reduce(hashed, length, i_col):
    #On génère une clé à partir du hash et de l'indice de la colonne
    key = (int(hashed[:9], 16) ^ i_col) % (chars_len ** length)
    passwd = ""
    #On itère pour la taille du mot de passe souhaité
    for i in range(length):
        #On ajoute le caractère qui correspond à l'indice dans notre set de caractères
        passwd += chars[key % chars_len]
        key //= chars_len
    return passwd

#Ecrit la table dans le fichier de sortie
def write_table_to_file(table, output_filename):
    with open(output_filename, "a") as output_file:
        for chain in table:
            prepared_line = chain[0] + "-" + chain[1] + "\n"
            output_file.write(prepared_line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--column", help="Column number", type=int, default=50000)
    parser.add_argument("-ch", "--chain", help="Chains number", type=int, default=500)
    parser.add_argument("-min", "--min", help="Minimum length of the password to crack", type=int, default=8)
    parser.add_argument("-max", "--max", help="Maximum length of the password to crack", type=int, default=12)
    parser.add_argument("-o", "--output", help="Output file", required=True)
    arguments = parser.parse_args()

    #On écrit le nombre de colonne dans la première ligne du fichier pour le réutiliser pour l'attaque
    with open(arguments.output, "a") as output_file:
        prepared_line = str(arguments.column) + "\n"
        output_file.write(prepared_line)

    #Initialisation de la liste permettant de stocker tous les heads et les tails
    table_array = list()

    #On génère les chaines pour chaque longueur de mot de passe possible, ici minimum 8 et max 12 caractères
    for length in range(arguments.min,arguments.max+1):
        for i in range(arguments.chain):
            #Obtient la tete de notre chaine
            head = generate_head(length)
            #Obtient la queue de notre chaine
            tail = create_chain(head, arguments.column, length)
            #Initialisation de la liste permettant de stocker le head et le tail
            chain_array = list()
            chain_array.append(head)
            chain_array.append(tail)
            table_array.append(chain_array)
    #Ecrit la table dans le fichier de sortie
    write_table_to_file(table_array, arguments.output)
