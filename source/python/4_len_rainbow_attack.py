#!/usr/bin/env python3
import argparse
import hashlib
import string
import random

#Set de caractères possible pour le mot de passe à trouver
chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
chars_len = len(chars)

#Retourne le contenu du fichier sous forme de tableau
def read_file(input_filename):
    with open(input_filename, "r") as input_file:
        return input_file.readlines()

def crack_hash(h, table):
    origin_hash = h
    len_table = len(table)
    is_cracked = False
    i = 0

    #On parcourt toutes les chaines de la table
    while i < len_table and not is_cracked:
        tail = get_tail(i, table)
        c = 0
        while c < 50000 and not is_cracked:
            #Si les hash sont similaires
            if h == tail:
                is_cracked = True
                print(str(h) + " et " + str(tail) + " sont similaires!")

            else:
                #print(str(h) + " et " + str(tail) + " ne sont pas similaires!")
                taille = get_head_size(i, table)
                h = reduce_and_hash(h, taille)
            c += 1

        i += 1
    if is_cracked:
        print("Le tail correspondant au hash " + str(origin_hash) + " est " + str(tail))
    else:
        print("Le hash n'a pas été cracké")
    

#Retourne le hash du mot de passe issu de la réduction du hash précédent
def reduce_and_hash(hashed, length):
    password = reduce(hashed, length)
    return hashlib.sha256(password.encode('ascii')).hexdigest()
    
    #return hashlib.sha256(reduce(hashed, length).encode('ascii')).hexdigest()

#Retourne le tail de la chaine correspondant l'index donné en paramètre
def get_tail(index, table):
    return table[index].split('-')[1].split('\n')[0]

#Retourne le head de la chaine correspondant l'index donné en paramètre
def get_head(index, table):
    return table[index].split('-')[0]

#Retourne la taille du head de la chaine
def get_head_size(index, table):
    return len(get_head(index, table))

#Transforme le hash en une chaîne de caractères
def reduce(hashed, length):
    i = int(hashed,16)
    passwd = ""
    while len(passwd) < length:
        passwd += chars[i % chars_len]
        i = i // chars_len
    return passwd
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-hf", "--hash", help="Input file that contains hashes to crack", required=True)
    parser.add_argument("-tf", "--table", help="Input file that contains the rainbow table", required=True)
    arguments = parser.parse_args()

    hashes_array = read_file(arguments.hash)
    table_array = read_file(arguments.table)
    
    for h in hashes_array:
        crack_hash(h.split('\n')[0], table_array)

