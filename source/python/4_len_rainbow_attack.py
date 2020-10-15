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

#Compare le hash à cracker à tous les tails de la table, retourne l'indice du tail correspondant si le hash et le tail sont similaires
def compare_hash(h, table):
    for i in range(len(table)):
        tail = get_tail(i, table)
        if tail == h :
            #print("\nTail : " + str(tail))
            #print("Hash : " + str(h))
            #print(i)
            return i
    return -1

def find_tail(h, table, nb_colonne):
    origin_hash = h
    len_table = len(table)
    is_cracked = False
    #i = 0
    
    for taille in range(4, 5):
        c = 0
        while c <= nb_colonne and not is_cracked:
            search = compare_hash(h, table)

            #Si les hash sont similaires
            if search != -1:
                #print("H precedent : " + str(h_old))
                #print("Pass precedent : " + str(pass_old))
                is_cracked = True
                tail = get_tail(search, table)
                return c, search
                # print(str(h) + " et " + str(tail) + " sont similaires!")
            else:
                #print(str(h) + " et " + str(tail) + " ne sont pas similaires!")
                h_old = h
                h, pass_old = reduce_and_hash(h, taille, c)
            c += 1
    '''
    origin_hash = h
    len_table = len(table)
    is_cracked = False
    i = 0

    #On parcourt toutes les chaines de la table
    while i < len_table and not is_cracked:
        tail = get_tail(i, table)
        c = 0
        while c < nb_colonne and not is_cracked:
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
        print("Le head correspondant au hash " + str(origin_hash) + " est " + str(get_head(search, table)))
    else:
        print("Le hash n'a pas été cracké")*
    '''
    return -1, -1

#Retourne le mot de passe correspondant au hash à cracker
def find_password(i_col, i_ch, table, nb_colonne):

    #On récupère la tete de notre chaine
    head = get_head(i_ch, table)

    nb_boucle = nb_colonne - i_col
    longueur = len(head)
    password = head

    for i in range(nb_boucle):
        #On hash le mot de passe
        hashed = hashlib.sha256(password.encode('ascii')).hexdigest()
        #On applique la fonction de réduction sur le hash du mot de passe 
        password = reduce(hashed, longueur, int(i))

    return password

#Transforme le hash en une chaîne de caractères
def reduce(hashed, length, indice):
    i = int(hashed,16)
    passwd = ""
    while len(passwd) < length:
        passwd += chars[i % chars_len]
        i = i // chars_len
    return passwd
    
#Retourne le hash du mot de passe issu de la réduction du hash précédent
def reduce_and_hash(hashed, length, indice):
    
    password = reduce(hashed, length, indice)
    return hashlib.sha256(password.encode('ascii')).hexdigest(), password
    
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



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-hf", "--hash", help="Input file that contains hashes to crack", required=True)
    parser.add_argument("-tf", "--table", help="Input file that contains the rainbow table", required=True)
    arguments = parser.parse_args()

    hashes_array = read_file(arguments.hash)
    table_array = read_file(arguments.table)

    nb_colonne = int(table_array.pop(0).split('\n')[0])

    #Pour tous les hash présents dans le fichier de hash à cracker
    for h in hashes_array:
        indice_colonne, indice_chain = find_tail(h.split('\n')[0], table_array, nb_colonne)
        if indice_colonne != -1 and indice_chain != -1:
            h_pass = find_password(indice_colonne, indice_chain, table_array, nb_colonne)
            
            #Verification
            if hashlib.sha256(h_pass.encode('ascii')).hexdigest() == h.split('\n')[0]:
                print("\n[V] Le mot de passe correspondant au hash " + str(h) + " est " + str(h_pass) + "\n")
            else:
                print("\n[X] Les hashes ne sont pas similaires\n")
            
            #print("\nLe mot de passe correspondant au hash " + str(h) + " est " + str(h_pass) + "\n")
        
        else:
            print("\nAttack failed for " + str(h))
