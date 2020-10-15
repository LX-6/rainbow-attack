#!/usr/bin/env python3
import argparse
import hashlib
import string
import random

#Set de caractères possible pour le mot de passe à trouver
chars = string.ascii_letters + string.digits
chars_len = len(chars)

#Retourne le contenu du fichier sous forme de tableau
def read_file(input_filename):
    with open(input_filename, "r") as input_file:
        return input_file.readlines()

#Retourne le tail de la chaine correspondant l'index donné en paramètre
def get_tail(index, table):
    return table[index].split('-')[1].split('\n')[0]

#Retourne le head de la chaine correspondant l'index donné en paramètre
def get_head(index, table):
    return table[index].split('-')[0]

# Hashe un mot de passe en utilisant sha256
def sha256(password):
    return hashlib.sha256(password.encode('ascii')).hexdigest()

# Réduit un Hash en un mot de passe
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

#Compare le hash à cracker à tous les tails de la table, retourne l'indice du tail correspondant si le hash et le tail sont similaires
def compare_hash(h, table):
    for i in range(len(table)):
        tail = get_tail(i, table)
        if tail == h :
            return i
    return -1

# Trouve la chaîne de la table contenant le Hash à cracker
def find_tail(h, table, nb_colonne, min, max):
    # Compare le Hash avec les queues de la table
    indice_chain = compare_hash(h, table)

    # Si le Hash est une des queues, on retourne l'indice de la chaîne correspondante
    if(indice_chain != -1):
        return nb_colonne, indice_chain

    # Pour toutes les longueurs de mot de passe possibles
    for password_length in range(int(min), int(max)+1):
        # Pour chaque colonne de la chaîne en partant de la fin
        for start_col in range(nb_colonne-1, -1, -1):
            temp_h = h
            # Réduit puis hashe successivement le Hash à cracker
            for col in range(start_col, nb_colonne):
                temp_h = sha256(reduce(temp_h, password_length, col))

            # Compare le Hash calculé (après réduction et hachage successifs) avec les queues de la table
            indice_chain = compare_hash(temp_h, table)

            # Si le Hash calculé est une des queues, on retourne l'indice de la chaîne correspondante et le nombre d'opérations effectuées
            if(indice_chain != -1):
                return start_col, indice_chain

    return -1, -1

#Retourne le mot de passe correspondant au hash à cracker
def find_password(indice_colonne, indice_chain, table):
    head = get_head(indice_chain, table)
    head_size = len(head)
    password = head

    for col in range(indice_colonne):
        temp_h = sha256(password)
        password = reduce(temp_h, head_size, col)

    return password


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-hf", "--hash", help="Input file that contains hashes to crack", required=True)
    parser.add_argument("-tf", "--table", help="Input file that contains the rainbow table", required=True)
    parser.add_argument("-min", "--minimum", help="Minimum size of password", required=True)
    parser.add_argument("-max", "--maximum", help="Maximum size of password", required=True)
    arguments = parser.parse_args()

    # Hash à cracker
    hashes_array = read_file(arguments.hash)
    # Rainbow
    table_array = read_file(arguments.table)

    # Récupère le nombre de colonnes de la rainbow table en entête du fichier
    nb_colonne = int(table_array.pop(0).split('\n')[0])

    # Pour tous les Hash à cracker
    for h in hashes_array:
        # Trouver la chaîne correspondante et la colonne correspondante
        indice_colonne, indice_chain = find_tail(h.split('\n')[0], table_array, nb_colonne, arguments.minimum, arguments.maximum)

        # Si on a trouvé le Hash
        if indice_colonne != -1 and indice_chain != -1:
            # Trouver le mot de passe correspondant au Hash
            h_pass = find_password(indice_colonne, indice_chain, table_array)

            # Vérifier que le Hash et le mot de passe trouvés concordent bien
            if sha256(h_pass) == h.split('\n')[0]:
                print("\n[V] Le mot de passe correspondant au hash " + str(h) + " est " + str(h_pass) + "\n")
            else:
                print("\n[X] Les hashes ne sont pas similaires\n")

        else:
            print("\nAttack failed for " + str(h))
