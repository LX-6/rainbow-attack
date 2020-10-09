import matplotlib.pyplot as plt
from collections import Counter

# Trace le graphe des collisions dans un fichier contenant une liste de mdp
# Les mdp dont écris ligne par ligne
def plotfile(filename):
    with open(filename) as file:
        data = file.readlines()
    file.close()

    # Compte le nombre d'occurences d'un mdp dans un fichier
    data_count = Counter(data)

    # Trace le graphe des collisions dans la liste de mdp
    x = range(0, len(data_count.keys()))
    y = data_count.values()

    plt.plot(x, y)

    plt.xlabel("Password")
    plt.ylabel("Occurence number")

    plt.title("Collision graph")

    plt.show()


if __name__ == "__main__":
    print("Filename :")
    filename = input()
    plotfile(filename)
