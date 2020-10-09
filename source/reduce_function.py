# Caractères utlisables dans le mdp
# A MODIFIER POUR CORRESPONDRE A LA POLITIQUE DE MDP
chars="abcdefghijklmnopqrstuvwxyz"
chars_len = len(chars)

# Fonction de réduction
# A OPTIMISER
def reduce(input_filename, output_filename):
    with open(input_filename) as input_file:
        with open(output_filename, "w") as output_file:
            for hash in input_file:
                i = int(hash,16)

                passwd = ""
                # Transforme le hash en une chaîne de caractères
                # A MODIFIER POUR CORRESPONDRE A LA POLITIQUE DE MDP
                while len(passwd) < 8:
                    passwd = passwd + chars[i % chars_len]
                    i = i // chars_len

                output_file.write(passwd)
                output_file.write("\n")
        output_file.close()
    input_file.close()


if __name__ == "__main__":
    print("Input Filename :")
    input_filename = input()
    print("Output Filename :")
    output_filename = input()
    reduce(input_filename, output_filename)
