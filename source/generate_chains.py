#!/usr/bin/env python3
import argparse
import hashlib
import string
import random

chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
chars_len = len(chars)

#Transforme le hash en une chaîne de caractères
def reduce(hashed):
    i = int(hashed,16)
    passwd = ""
    while len(passwd) < 8:
        passwd = passwd + chars[i % chars_len]
        i = i // chars_len
    return passwd

#Créé une ligne en partant d'une string "head" et retourne le dernier élément de la chaine "tail"
def create_line(hashed, nb_boucle):

    for i in range(0,nb_boucle):
        #On hash le mot de passe
        h = hashlib.sha256(hashed.encode('ascii')).hexdigest()
        #On applique la fonction de réduction sur le hash du mot de passe 
        hashed = reduce(h)

    #On retourne le hash du dernier password généré
    return hashlib.sha256(hashed.encode('ascii')).hexdigest()

#Ecrit une chaine avec la tete et la queue générées précédemment
def write_file(head, tail, output_filename):
    with open(output_filename, "a") as output_file:
        prepared_line = head + "-" + tail + "\n"
        output_file.write(prepared_line)

#Génère un mot de passe d'une longueur donnée
def generate_head(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--column", help="Column number", type=int, default=50000)
    parser.add_argument("-l", "--line", help="Line number", type=int, default=500)
    parser.add_argument("-o", "--output", help="Output file", required=True)
    arguments = parser.parse_args()
    
    for i in range(arguments.line):
        head = generate_head(8)
        tail = create_line(head, arguments.column)
        write_file(head, tail, arguments.output)
