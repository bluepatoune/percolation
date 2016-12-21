#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Percolation.py: Un module python pour effectuer des percolations matricielles.
"""

from matplotlib           import pyplot
from matplotlib           import colors
from mpl_toolkits.mplot3d import Axes3D
from random               import random

EAU_MOUVANTE = 3
EAU = 2
VIDE = 1
ROCHE = 0
NEANT = -1

clrs = {NEANT:        None  ,
        ROCHE:       'grey' ,
        VIDE:        'white',
        EAU:         'blue' ,
        EAU_MOUVANTE:'cyan' }

def draw(matrix3d, subplot, clrs):
    for x, matrix2d in enumerate(matrix3d):
        for y, line in enumerate(matrix2d):
            for z, coef in enumerate(line):
                if clrs[coef] != None:
                    subplot.scatter(z, y, -x, c=clrs[coef])
                
def modelisation(n, p, q, indice=0.5):
    esp = espace(n, p, q, indice)
    esp = pluie(esp)
    return percolation(esp)

def percolation(espace):  # methode 2
    """ Indique s'il y a percolation ou pas """
    
    fig = pyplot.figure()
    subplot = fig.add_subplot(111, projection='3d')
    subplot.set_xlabel('X')
    subplot.set_ylabel('Y')
    subplot.set_zlabel('Z')
    
    draw([[[-1, 0, 1, 2, 3]]], subplot, clrs)
    pyplot.pause(1)
    print( espace )
    eau_mouvante = initialisation_eau_mouvante(espace)
    
    while eau_mouvante != []:
        draw(espace, subplot, clrs)
        pyplot.pause(.0001)

        eau_mouvante = propagation(espace,eau_mouvante)
    
    return resultat(espace)


def propagation(espace, eau_mouvante):# done 
     pores_vides = []
     pores_vides_locale = []
     for (x, y, z) in eau_mouvante:
        pores_vides_locale = regard(espace, x, y, z)
        matrice = infiltration(espace, pores_vides_locale)
        matrice[x][y][z] = EAU
        pores_vides += pores_vides_locale
     eau_mouvante = pores_vides[:] # à changer 
     return eau_mouvante


def resultat(espace): # done 
    for ligne in espace[len(espace)-2]: # on parcourt l'avant dernière ligne de la matrice
        for coef in ligne:
            if coef == EAU or coef == EAU_MOUVANTE:
                return True
    return False

def pluie(espace): # done 
    """Ajoute de l'eau en surface."""
    for y, ligne in enumerate(espace[0]): # matrice du haut ( axe x en hauteur )
        for z, coef in enumerate(ligne): # enumerate renvoie une liste de tuples (indice, valeur)
            if coef == VIDE:
                espace[0][y][z] = EAU_MOUVANTE
    return espace

def regard(espace, x, y, z):#done
    """Renvoie la liste des coordonnées des pores vides autour d'une case."""
    pores_vides = []
    for vecteur in vecteur_espace(3):
         coords = (x+vecteur[0], y+vecteur[1], z+vecteur[2])
         if espace[coords[0]][coords[1]][coords[2]] == VIDE: 
                pores_vides.append(coords)
    return pores_vides
 

def vecteur_espace(dim):#done
    """Renvoie une liste des vecteurs possibles de déplacement dans l'espace."""
    vecteurs = []
    for direction in range(dim):
        for sens in [-1, 1]:
            vecteur = [0]*dim
            vecteur[direction] = sens
            vecteurs.append(vecteur)
    return vecteurs


def infiltration(espace, pores_vides):# done
    """Ajoute de l'eau dans les pores vides."""
    for (x, y, z) in pores_vides: # On itère sur la liste par tuples
        espace[x][y][z] = EAU_MOUVANTE
    return espace

def initialisation_eau_mouvante(espace):#done 
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

def zero(n, p, q):
    """ crééer une matrice de zéros de taille n,p,q """
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

def bords(espace):
    """On borde la matrice de -1, sur trois côtés."""
    for matrice in espace:
        for ligne in matrice:
            ligne.insert(0, NEANT)
            ligne.append(NEANT)
        ligne_bas = [NEANT] * len(matrice[0])
        matrice.append(ligne_bas)
        matrice.insert(0, ligne_bas)
    matrice_fond=[ligne_bas]*len(espace[0])
    espace.append(matrice_fond)
    return espace

if __name__ == '__main__':
    print(modelisation(3, 3, 3))
