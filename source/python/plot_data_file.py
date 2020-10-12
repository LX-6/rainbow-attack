#!/usr/bin/env python3

import matplotlib.pyplot as plt
from collections import Counter
import argparse

# Trace le graphe des collisions dans un fichier contenant une liste de mdp
# Les mdp dont écris ligne par ligne
def plotfile(filename):
    with open(filename) as file:
        data = file.readlines()

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
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file")
    arguments = parser.parse_args()
    plotfile(arguments.input)
