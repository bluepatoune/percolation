#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Percolation.py: Un module python pour effecter des percolations matricielles."""

from matplotlib import pyplot # NOTE: Le 'as' est inutile, pyplot n'est utilisé qu'une fois...
from matplotlib import colors

EAU = 2
VIDE = 1
PIERRE = 0
NEANT = -1

couleurs = ['black', 'grey' , 'white', 'blue']
valeurs  = [ NEANT ,  PIERRE,  VIDE  ,  EAU  ]

def modelisation(n, p, i):
    E = matrice(n, p, i)
    E = pluie(E)
    return percolation(E)

def percolation(matrice): # TODO: On devrait passer à percolation() uniquement un objet matrice à la place de n, p... qui devraient être des propriétés de l'objet matrice
    """ Indique s'il y a percolation ou pas """
    cmap = colors.ListedColormap(couleurs) # TODO: Relève du display, à metttre ailleurs.
    norm = colors.BoundaryNorm(valeurs + [max(valeurs)+1], cmap.N)

    pyplot.matshow([valeurs], 1, cmap=cmap, norm=norm)
    pyplot.pause(1)

   
    for t in range(T):
        pyplot.matshow(matrice, 1, cmap=cmap, norm=norm) # TODO: Séparer la logique de display de la logique de génération (threads ?)
        pyplot.pause(.0001)
        pores_vides2 = []
        for x in range(len(matrice)):             # Lignes
            for y in range(1, len(matrice[0])):   # Colonnes
                if matrice[x][y] == EAU:
                    pores_vides = regard(matrice, x, y)
                    pores_vides2 += regard(matrice, x, y)
                    matrice = infiltration(matrice, pores_vides)
        if pores_vides2 == []: # Si aucune case n'a de voisines vides
            return resultat(matrice)

def resultat(matrice):
    for coef in matrice[len(matrice)-2]: # on parcoure l'avant dernière ligne de la matrice 
        if coef == EAU:
            return True
    return False

def pluie(matrice): # J'ai recodé la fonction, du coup il faut adapter le code qui l'utilise (un seul arg)
    """Ajoute de l'eau en surface."""
    for i, coef in enumerate(matrice[0]): # NOTE: On itère pas sur les index sans raison
        if coef == VIDE:
            matrice[0][i] = EAU
    return matrice

def regard(matrice, x, y): # NOTE: Idem. Noveau code, donc à utiliser différement.
    """Renvoie la liste des coordonnées des pores vides autour d'une case d'eau.""" # TODO: Et si c'est pas une case d'eau ?
    pores_vides = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i == 0 or j == 0) and matrice[x+i][y+j] == VIDE:
                pores_vides.append((x+i, y+j)) # NOTE: Les couples de coords en tuples () c'est mieux qu'en listes [].
    return pores_vides

def infiltration(matrice, pores_vides):
    """Ajoute de l'eau dans les pores vides."""
    for (x, y) in pores_vides: # NOTE: Itérez sur la liste par tuples
        matrice[x][y] = EAU
    return matrice

if __name__ == '__main__':
    data = -1
    while data != None:
        data = input("Entrez 4 args ")
        percolation(data[0], data[1], data[2], data[3])



#  ==[ COMMENTAIRES ]==

#Vous devez définir clairement vos variables par leur nom ou dans le docstr des fonctions. En l'état, on comprend rien sans la structure de l'algo.

#Ne jamais prendre de lettre majuscule en nom de variable.

#Utilisez xrange() au lieu de range() si la liste est statique. Ça passe un itérateur à la structure for au lieu de passer une liste, c'est bien bien bien plus efficace.

#Ne mélangez pas les fonctions et le display. Tout ce qui doit tourner de manière effective au lancement du script doit être dans "if __name__ == '__main__':", le reste c'est des fonctions. Vous pouvez ainsi concevoir et réutiliser votre code comme un module.
