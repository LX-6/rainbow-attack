TODO

# Tâches
## Générer la rainbow table
1. Générer la liste des mots de passe correspondant à la politique
	- Générer les mots de passe
	- Stocker les mots de passe
2. Ecrire une fonction de réduction R
	- Trouver la fonction R (tests statistiques, etc...)
	- Coder et optimiser la fonction R
3. Générer la rainbow table
	- Générer la chaîne de hash de taille k
	- Stocker les head et les tails

## Utiliser la rainbow table
1. Trouver la bonne chaîne de hash
	- Pour i dans k : vérifier si [R(h)]<sub>i</sub> est une tail d'une chaine
		- Algo de recherche de tail dans la liste des chaines
2. Trouver le mot de passe
	- Pour i dans k : vérifier si [H(p)]<sub>i</sub> est le hash de notre mot de passe

# TODO
## Travail réel
[] | Fourni par le professeur | A faire 
- | - | -
Gen mdp | [x]
Store mdp | [x] 
Find R | | [x]
Code and Optimise R | | [x]
Gen chains | | [x]
Store head and tail | | [x]
Find h in chains | [x] | [x]
Find mdp in chain | [x] | [x]

## A optimiser
Tache | Complexité
- | -
R | ?
Gen chains | `O = n * (k * ( O(R) + O(H) ))`
Find h in chains | `O = n * (k * ( O(R) + O(H) ))`
Find mdp in chain | `O = k * ( O(R) + O(H) )`