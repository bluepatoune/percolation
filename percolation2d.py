#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Percolation.py: Un module python pour effectuer des percolations matricielles."""

from matplotlib    import pyplot
from matplotlib    import colors
from random        import random

NEANT        = -1
ROCHE        = 0
VIDE         = 1
EAU          = 2
EAU_MOUVANTE = 3
DIM          = 2

couleurs = ['black', 'grey' , 'white', 'blue', 'cyan']
valeurs  = [ NEANT ,  ROCHE ,  VIDE  ,  EAU  ,  EAU_MOUVANTE]

def modelisation(n, p, indice=0.5):
    mat = matrice(n, p, indice)
    mat = pluie(mat)
    return percolation(mat)

# TODO: Changer nom matrice

def percolation(matrice):  # methode 2
    """Dessine la propagation de l'eau, et indique s'il y a percolation."""
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
    """Propage l'eau mouvante dans les cases d'air."""
    pores_vides = []
    pores_vides_locale = []
    for (x, y) in eau_mouvante:
        pores_vides_locale = regard(matrice, x, y)
        matrice = infiltration(matrice, pores_vides_locale)
        matrice[x][y] = EAU
        pores_vides += pores_vides_locale
    eau_mouvante = list(pores_vides)
    return eau_mouvante

def resultat(matrice):
    """Indique s'il y a percolation ou pas."""
    for coef in matrice[len(matrice)-2]: # On parcourt l'avant dernière ligne de la matrice
        if coef == EAU or coef == EAU_MOUVANTE:
            return True
    return False

def pluie(matrice):
    """Ajoute de l'eau en surface."""
    for i, coef in enumerate(matrice[0]):
        if coef == VIDE:
            matrice[0][i] = EAU_MOUVANTE
    return matrice

"""def regard(matrice, x, y):
    #Renvoie la liste des coordonnées des pores vides autour d'une case.
    pores_vides_new = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i == 0 or j == 0) and matrice[x+i][y+j] == VIDE: # On ne regarde pas les cases en diagonale
                pores_vides_new.append((x+i, y+j)) # Les couples de coordonnées sont enregistrés en tuples (x, y)
    return pores_vides_new"""


def regard(espace, x, y):
    """Renvoie la liste des coordonnées des pores vides autour d'une case."""
    pores_vides = []
    for vecteur in vecteur_espace(DIM):
         coords = (x+vecteur[0], y+vecteur[1])
         if espace[coords[0]][coords[1]] == VIDE:
                pores_vides.append(coords)
    return pores_vides


def vecteur_espace(dim):
    """Renvoie une liste des vecteurs de déplacement dans l'espace possibles."""
    vecteurs = []
    for direction in range(dim):
        for sens in [-1, 1]:
            vecteur = [0]*dim
            vecteur[direction] = sens
            vecteurs.append(vecteur)
    return vecteurs

def initialisation_eau_mouvante(matrice):
    eau_mouvante = []
    for i, coef in enumerate(matrice[0]):
        if coef == EAU_MOUVANTE:
            eau_mouvante.append((0, i))
    return eau_mouvante

def infiltration(matrice, pores_vides):
    """Ajoute de l'eau dans les pores vides."""
    for (x, y) in pores_vides: # On itère sur la liste par tuples
        matrice[x][y] = EAU_MOUVANTE
    return matrice

def matrice(n, p, indice=.5):
    """Création d'une matrice modélisant une roche poreuse aléatoire."""
    matrice = zero(n, p)
    matrice = pores(matrice, indice)
    matrice = bords(matrice)
    return matrice

def zero(n, p):
    """Crée une matrice de zéros de taille (n, p)."""
    matrice = [0]*n
    for i in range(n):
        matrice[i] = [0]*p
    return matrice

def pores(matrice, indice=.5):
    """Introduit des pores vides au hasard, en fonction de l'indice de porosité."""
    for i, ligne in enumerate(matrice):
        for j, coef in enumerate(ligne):
            if random() < indice:
                matrice[i][j] = VIDE
    return matrice

def bords(matrice):
    """On borde la matrice de NEANT, sur trois côtés."""
    for ligne in matrice:
        ligne.insert(0, NEANT) # HACK: ligne = [NEANT] + ligne + [NEANT] ?
        ligne.append(NEANT)
    ligne_bas = [NEANT]*len(matrice[0])
    matrice.append(ligne_bas)
    return matrice

if __name__ == '__main__': # Fonction de test
    print(modelisation(100, 100, 0.6))
