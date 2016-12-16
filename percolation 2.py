#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Percolation.py: Un module python pour effectuer des percolations matricielles."""

from matplotlib    import pyplot
from matplotlib    import colors

#from randomisation import matrice

EAU_MOUVANTE = 3
EAU = 2
VIDE = 1
ROCHE = 0
NEANT = -1

couleurs = ['black', 'grey' , 'white', 'blue', 'cyan']
valeurs  = [ NEANT ,  ROCHE ,  VIDE  ,  EAU  ,  EAU_MOUVANTE]

def modelisation(n, p, indice=0.5):
    mat = matrice(n, p, indice)
    mat = pluie(mat)
    return percolation(mat)

 # changer nom matrice
def percolation(matrice):  # methode 2
    """ Indique s'il y a percolation ou pas """

    cmap = colors.ListedColormap(couleurs) # TODO: Relève du display, à metttre ailleurs.
    norm = colors.BoundaryNorm(valeurs + [max(valeurs)+1], cmap.N)
    pyplot.matshow([valeurs], 1, cmap=cmap, norm=norm)
    pyplot.pause(1)

    eau_mouvante = initialisation_eau_mouvante(matrice)
    while eau_mouvante != []:

        pyplot.matshow(matrice, 1, cmap=cmap, norm=norm) # TODO: Séparer la logique de display de la logique de génération (threads ?)
        pyplot.pause(.0001)

        eau_mouvante = propagation(matrice,eau_mouvante)
    return resultat(matrice)


def propagation(matrice, eau_mouvante):
     pores_vides = []
     pores_vides_locale = []
     for (x, y) in eau_mouvante:
        pores_vides_locale = regard(matrice, x, y)
        matrice = infiltration(matrice, pores_vides_locale)
        matrice[x][y] = EAU
        pores_vides += pores_vides_locale
     eau_mouvante = pores_vides[:]
     return eau_mouvante

def percolation_critique(n, p, N, P):
    proba = []
    indice = []
    for d in range(N+1):
        indice += [d/N]
    for i in indice:
        S = 0
        for e in range(P):
            if modelisation(n, p, i):
                S += 1
        proba += [S/P]
    pyplot.plot(indice, proba)
    return indice, proba
# EN FONCTION RAPPORT N/P


def resultat(matrice):
    for coef in matrice[len(matrice)-2]: # on parcourt l'avant dernière ligne de la matrice
        if coef == EAU or coef == EAU_MOUVANTE:
            return True
    return False

def pluie(matrice):
    """Ajoute de l'eau en surface."""
    for i, coef in enumerate(matrice[0]): # enumerate renvoie une liste de tuples (indice, valeur)
        if coef == VIDE:
            matrice[0][i] = EAU_MOUVANTE
    return matrice

def regard(matrice, x, y):
    """Renvoie la liste des coordonnées des pores vides autour d'une case."""
    pores_vides_new = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i == 0 or j == 0) and matrice[x+i][y+j] == VIDE: # on ne regarde pas les cases en diagonale
                pores_vides_new.append((x+i, y+j)) # Les couples de coordonnées sont enregistrés en tuples ()
    return pores_vides_new
# liste vecteur en argument

def initialisation_eau_mouvante(matrice):

    eau_mouvante = []
    for i, coef in enumerate(matrice[0]):
        if coef == EAU_MOUVANTE:
            eau_mouvante.append((0,i))
    return eau_mouvante

def infiltration(matrice, pores_vides):
    """Ajoute de l'eau dans les pores vides."""
    for (x, y) in pores_vides: # On itère sur la liste par tuples
        matrice[x][y] = EAU_MOUVANTE
    return matrice

from random import random

def matrice(n, p, indice=.5):
    """Création d'une matrice modélisant une roche poreuse aléatoire."""
    matrice = zero(n, p)
    matrice = pores(matrice, indice)
    matrice = bords(matrice)
    return matrice

def zero(n, p):
    """ crééer une matrice de zéros de taille n,p """
    matrice = [0]*n
    for i in range(n):
        matrice[i] = [0]*p
    return matrice

def pores(matrice, indice=.5):
    """Introduit des pores vides au hasard, en fonction de l'indice de porosité i."""
    for i, ligne in enumerate(matrice):
        for j, coef in enumerate(ligne):
            if random() < indice:
                matrice[i][j] = VIDE
    return matrice

def bords(matrice):
    """On borde la matrice de -1, sur trois côtés."""
    for ligne in matrice:
        ligne.insert(0, NEANT)
        ligne.append(NEANT)
    ligne_bas = [NEANT] * len(matrice[0])
    matrice.append(ligne_bas)
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


