#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Percolation.py: Un module python pour effecter des percolations matricielles."""

from matplotlib    import pyplot 
from matplotlib    import colors
#from randomisation import matrice

EAU = 2
VIDE = 1
ROCHE = 0
NEANT = -1

couleurs = ['black', 'grey' , 'white', 'blue']
valeurs  = [ NEANT ,  ROCHE ,  VIDE  ,  EAU  ]

def modelisation(n, p, indice=0.5):
    mat = matrice(n, p, indice)
    mat = pluie(mat)
    return percolation(mat)

def percolation(matrice): 
    """ Indique s'il y a percolation ou pas """
    cmap = colors.ListedColormap(couleurs) # TODO: Relève du display, à metttre ailleurs.
    norm = colors.BoundaryNorm(valeurs + [max(valeurs)+1], cmap.N)

    pyplot.matshow([valeurs], 1, cmap=cmap, norm=norm)
    pyplot.pause(1)
    pores_vides2 = [1]
    while pores_vides2 != []:
        pyplot.matshow(matrice, 1, cmap=cmap, norm=norm) # TODO: Séparer la logique de display de la logique de génération (threads ?)
        pyplot.pause(.0001)
        pores_vides2 = []
        for x in range(len(matrice)):             # Lignes
            for y in range(1, len(matrice[0])):   # Colonnes
                if matrice[x][y] == EAU:
                    pores_vides = regard(matrice, x, y)
                    pores_vides2 += regard(matrice, x, y)
                    matrice = infiltration(matrice, pores_vides)
    return resultat(matrice)

def resultat(matrice):
    for coef in matrice[len(matrice)-2]: # on parcourt l'avant dernière ligne de la matrice 
        if coef == EAU:
            return True
    return False

def pluie(matrice): 
    """Ajoute de l'eau en surface."""
    for i, coef in enumerate(matrice[0]): # enumerate renvoie une liste de tuples (indice, valeur) 
        if coef == VIDE:
            matrice[0][i] = EAU
    return matrice

def regard(matrice, x, y): 
    """Renvoie la liste des coordonnées des pores vides autour d'une case.""" 
    pores_vides = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i == 0 or j == 0) and matrice[x+i][y+j] == VIDE: # on ne regarde pas les cases en diagonale 
                pores_vides.append((x+i, y+j)) # Les couples de coordonnées sont enregistrés en tuples ()
    return pores_vides

def infiltration(matrice, pores_vides):
    """Ajoute de l'eau dans les pores vides."""
    for (x, y) in pores_vides: # On Itère sur la liste par tuples
        matrice[x][y] = EAU
    return matrice

#if __name__ == '__main__':
#    data = -1
#    while data != None:
#        data = input("Entrez 4 args ")
#        percolation(data[0], data[1], data[2], data[3])



#  ==[ COMMENTAIRES ]==

#Vous devez définir clairement vos variables par leur nom 

#Ne jamais prendre de lettre majuscule en nom de variable.

#Utilisez xrange() au lieu de range() si la liste est statique. Ça passe un itérateur à la structure for au lieu de passer une liste, c'est bien bien bien plus efficace.

#Ne mélangez pas les fonctions et le display. Tout ce qui doit tourner de manière effective au lancement du script doit être dans "if __name__ == '__main__':", le reste c'est des fonctions. Vous pouvez ainsi concevoir et réutiliser votre code comme un module.
