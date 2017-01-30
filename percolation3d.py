#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Percolation.py: Un module python pour effectuer des percolations matricielles."""

from matplotlib           import pyplot
from matplotlib           import colors
from mpl_toolkits.mplot3d import Axes3D
from random               import random

NEANT        = -1
ROCHE        = 0
VIDE         = 1
EAU          = 2
EAU_MOUVANTE = 3

couleurs = {NEANT:        None  ,
            ROCHE:       'grey' ,
            VIDE:        'white',
            EAU:         'blue' ,
            EAU_MOUVANTE:'cyan' }

def draw(espace, subplot, clrs):
    """Dessine chaque coeficient de la matrice comme un point de plot 3D."""
    for x, matrice in enumerate(espace):
        for y, line in enumerate(matrice):
            for z, coef in enumerate(line):
                if couleurs[coef] != None:
                    subplot.scatter(z, y, -x, c=couleurs[coef])

def modelisation(n, p, q, indice=0.5):
    esp = espace(n, p, q, indice)
    esp = pluie(esp)
    return percolation(esp)

def percolation(espace):
    """Dessine la propagation de l'eau, et indique s'il y a percolation."""
    fig = pyplot.figure()
    subplot = fig.add_subplot(111, projection='3d')
    subplot.set_xlabel('Z')
    subplot.set_ylabel('Y')
    subplot.set_zlabel('-X')

    draw([[[-1, 0, 1, 2, 3]]], subplot, couleurs)
    pyplot.pause(1)

    eau_mouvante = initialisation_eau_mouvante(espace)
    while eau_mouvante != []:
        draw(espace, subplot, couleurs)
        pyplot.pause(.0001)

        eau_mouvante = propagation(espace, eau_mouvante)

    return resultat(espace)


def propagation(espace, eau_mouvante):
    """Propage l'eau mouvante dans les cases d'air."""
    pores_vides = []
    pores_vides_locale = []
    for (x, y, z) in eau_mouvante:
        pores_vides_locale = regard(espace, x, y, z)
        matrice = infiltration(espace, pores_vides_locale)
        matrice[x][y][z] = EAU
        pores_vides += pores_vides_locale
    eau_mouvante = list(pores_vides)
    return eau_mouvante


def resultat(espace):
    """Indique s'il y a percolation ou pas."""
    for ligne in espace[len(espace)-2]: # On parcourt l'avant dernière ligne de la matrice
        for coef in ligne:
            if coef == EAU or coef == EAU_MOUVANTE:
                return True
    return False

def pluie(espace):
    """Ajoute de l'eau en surface."""
    for y, ligne in enumerate(espace[0]):
        for z, coef in enumerate(ligne):
            if coef == VIDE:
                espace[0][y][z] = EAU_MOUVANTE
    return espace

def regard(espace, x, y, z):
    """Renvoie la liste des coordonnées des pores vides autour d'une case."""
    pores_vides = []
    for vecteur in vecteur_espace(3):
         coords = (x+vecteur[0], y+vecteur[1], z+vecteur[2])
         if espace[coords[0]][coords[1]][coords[2]] == VIDE:
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


def infiltration(espace, pores_vides):
    """Ajoute de l'eau dans les pores vides."""
    for (x, y, z) in pores_vides:
        espace[x][y][z] = EAU_MOUVANTE
    return espace

def initialisation_eau_mouvante(espace): # TODO: Redondance avec pluie()
    eau_mouvante = []
    for y, ligne in enumerate(espace[0]):
        for z, coef in enumerate(ligne):
            if coef == EAU_MOUVANTE:
                eau_mouvante.append((0, y, z))
    return eau_mouvante


def espace(n, p, q, indice=.5):
    """Création d'une matrice modélisant une roche poreuse aléatoire."""
    espace = zero(n, p, q)
    espace = pores(espace, indice)
    espace = bords(espace)
    return espace

def zero(n, p, q): # TODO: Facile à généraliser en n dimensions avec une fonction récursive...
    """Crée une matrice de zéros de taille (n, p, q)."""
    espace = [0]*n
    for i in range(n):
        espace[i] = [0]*p
        for j in range(p):
            espace[i][j]=[0]*q
    return espace

def pores(espace, indice=.5):
    """Introduit des pores vides au hasard, en fonction de l'indice de porosité i."""
    for x, matrice in enumerate(espace):
        for y, ligne in enumerate(matrice):
            for z, coeff in enumerate(ligne):
                if random() < indice:
                    espace[x][y][z] = VIDE
    return espace

def bords(espace): # TODO: Facile à généraliser en n dimensions avec une fonction récursive...
    """On borde l'espace de NEANT, sur tous ses côtés, sauf le supérieur."""
    for matrice in espace:
        for ligne in matrice:
            ligne.insert(0, NEANT) # HACK: ligne = [NEANT] + ligne + [NEANT] ?
            ligne.append(NEANT)
        ligne_bas = [NEANT]*len(matrice[0])
        matrice.append(ligne_bas) # HACK: ligne = [NEANT] + ligne + [NEANT] ?
        matrice.insert(0, ligne_bas)
    matrice_fond = [ligne_bas]*len(espace[0])
    espace.append(matrice_fond)
    return espace

if __name__ == '__main__': # Fonction de test
    print(modelisation(8, 8, 8))
