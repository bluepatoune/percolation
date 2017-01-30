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
            VIDE:         None,
            EAU:         'blue' ,
            EAU_MOUVANTE:'cyan' }
            
# n = nombre de matrice (profondeur)
# p = nombre de ligne dans chaque matrice 
# q = nombre de coeff dans chaque ligne ( colonne ) 

def draw(espace, subplot, clrs):
    """Dessine chaque coeficient de la matrice comme un point de plot 3D."""
    for x, matrice in enumerate(espace):
        for y, line in enumerate(matrice):
            for z, coef in enumerate(line):
                if couleurs[coef] != None:
                    subplot.scatter(z, y, -x, c=couleurs[coef])

def modelisation(n, p, q, dim, indice = 0.5, affichage = True):
    """réalisation d'une propagation d'eau à travers un sol rocheux, retourne True si il y a percolation """
    etape_1 = initialisation(n, p, q, indice)
    eau_mouvante1 = etape_1[1]
    esp = etape_1[0]
    liste_vecteurs = vecteurs_espace(dim) 
    return percolation(esp, liste_vecteurs, eau_mouvante1, affichage)

def percolation(espace, liste_vecteurs, eau_mouvante1, affichage):
    """Affiche graphiquement la propagation de l'eau, et indique s'il y a percolation."""
    if affichage == True:
        fig = pyplot.figure()
        subplot = fig.add_subplot(111, projection='3d')
        subplot.set_xlabel('Z')
        subplot.set_ylabel('Y')
        subplot.set_zlabel('-X')

        draw([[[-1, 0, 1, 2, 3]]], subplot, couleurs)
        pyplot.pause(1)

    eau_mouvante = eau_mouvante1
    while eau_mouvante != []:
        if affichage == True:
            draw(espace, subplot, couleurs)
            pyplot.pause(.0001)

        eau_mouvante = propagation(espace, eau_mouvante, liste_vecteurs)

    return resultat(espace)


def propagation(espace, eau_mouvante, liste_vecteurs):
    """Propage l'eau mouvante dans les cases vides."""
    pores_vides = []
    pores_vides_locale = []
    for (x, y, z) in eau_mouvante:
        pores_vides_locale = regard(espace, x, y, z, liste_vecteurs)
        matrice = infiltration(espace, pores_vides_locale)
        matrice[x][y][z] = EAU
        pores_vides += pores_vides_locale
    eau_mouvante = list(pores_vides)
    return eau_mouvante

def replace(espace, v, CST):
    for i in range(len(v)):
        espace = espace[v[i]]
    espace = CST

def resultat(espace):
    """Indique s'il y a percolation ou pas."""
    for ligne in espace[len(espace)-2]: # On parcourt l'avant dernière matrice de l'espace
        for coef in ligne:
            if coef == EAU or coef == EAU_MOUVANTE:
                return True
    return False
    
def resultat(espace):
    matrice = espace[len(espace)-2]
    y = 0
    z = 0
    p = len(matrice)-2
    q = len(matrice[0])-2
    while y <= p and (matrice[y][z] != EAU or matrice[y][z] != EAU_MOUVANTE):
        z += 1
        if z == q:
            y += 1
            z = 0
    if y == p+1:
        return False
    else :
        return True
        
def resultat(espace): # rendre ca jolie 
    matrice = espace[len(espace)-2]
    y = 0
    z = 0
    p = len(matrice)-2
    q = len(matrice[0])-2
    while y <= p and matrice[y][z] != EAU and matrice[y][z] != EAU_MOUVANTE:
        if z != q:
            z += 1
        else: 
            y += 1
            z = 0
    if y == p+1:
        return False
    else :
        return True

    
def vecteurs_espace(dim):
    """Renvoie une liste des vecteurs possibles déplacement dans l'espace ."""
    liste_vecteurs = []
    for direction in range(dim):
        for sens in [-1, 1]:
            vecteur = [0]*dim
            vecteur[direction] = sens
            liste_vecteurs.append(vecteur)
    return liste_vecteurs

def regard(espace, x, y, z, liste_vecteurs):
    """Renvoie la liste des coordonnées des pores vides autour d'une case d'eau mouvante."""
    pores_vides = []
    for vecteur in liste_vecteurs:
         coords = (x+vecteur[0], y+vecteur[1], z+vecteur[2])
         if espace[coords[0]][coords[1]][coords[2]] == VIDE:
                pores_vides.append(coords)
    return pores_vides
    
def infiltration(espace, pores_vides):
    """Ajoute de l'eau mouvante dans les pores vides."""
    for (x, y, z) in pores_vides:
        espace[x][y][z] = EAU_MOUVANTE
    return espace

def initialisation(n, p, q, indice):
    esp = espace(n, p, q, indice)
    eau_mouvante = []
    for y, ligne in enumerate(esp[0]):
        for z, coef in enumerate(ligne):
            if coef == VIDE:
                esp[0][y][z] = EAU_MOUVANTE
                eau_mouvante.append((0, y, z))
    return esp, eau_mouvante
    
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
    print(modelisation(8, 8, 8, 3, 0.9, False))
