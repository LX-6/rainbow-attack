#!/usr/bin/env python3
import argparse
import hashlib
import string
import random

#Set de caractères possible pour le mot de passe à trouver
chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
chars_len = len(chars)

#Transforme le hash en une chaîne de caractères
def reduce(hashed, length, indice):
    i = int(hashed,16)+indice
    passwd = ""
    while len(passwd) < length:
        passwd += chars[i % chars_len]
        i = i // chars_len
    return passwd

#Créé une chaine en partant d'une string "head" et retourne le dernier élément de la chaine "tail"
def create_chain(password, nb_boucle, longueur):
    #nb_boucle == nombre de colonne de la chaine
    for i in range(nb_boucle):
        #On hash le mot de passe
        hashed = hashlib.sha256(password.encode('ascii')).hexdigest()
        #write_chain_to_file(password, hashed, output_filename)
        #print(hashed)
        #On applique la fonction de réduction sur le hash du mot de passe
        password = reduce(hashed, longueur, int(i))

    #On retourne le hash du dernier password généré
    #print("Password pour la ligne " + str(i) + " : " + password)
    #write_chain_to_file(password, hashlib.sha256(password.encode('ascii')).hexdigest(), output_filename)
    return hashlib.sha256(password.encode('ascii')).hexdigest()

#Ecrit une chaine avec la tete et la queue générées précédemment dans le fichier de sortie
def write_chain_to_file(head, tail, output_filename):
    with open(output_filename, "a") as output_file:
        prepared_line = head + "-" + tail + "\n"
        #prepared_line = head + "-" + tail + "|"
        output_file.write(prepared_line)

#Génère un mot de passe d'une longueur donnée
def generate_head(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--column", help="Column number", type=int, default=50000)
    parser.add_argument("-ch", "--chain", help="Chains number", type=int, default=500)
    parser.add_argument("-o", "--output", help="Output file", required=True)
    arguments = parser.parse_args()

    #On écrit le nombre de colonne dans la première ligne du fichier pour le réutiliser pour l'attaque

    with open(arguments.output, "a") as output_file:
        prepared_line = str(arguments.column) + "\n"
        #prepared_line = head + "-" + tail + "|"
        output_file.write(prepared_line)

    #On génère les chaines pour chaque longueur de mot de passe possible, ici minimum 8 et max 12 caractères
    length = 4
    for i in range(arguments.chain):
        #Obtient la tete de notre chaine
        head = generate_head(length)
        #Obtient la queue de notre chaine
        tail = create_chain(head, arguments.column, length)
        #Ecrit la chaine dans le fichier de sortie
        write_chain_to_file(head, tail, arguments.output)
