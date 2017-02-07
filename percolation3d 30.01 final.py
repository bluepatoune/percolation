#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Percolation.py: Un module python pour effectuer des percolations matricielles."""

from matplotlib           import pyplot
from matplotlib           import colors
from mpl_toolkits.mplot3d import Axes3D
from random               import random

#Convention de codage:
NEANT        = -1
ROCHE        = 0
VIDE         = 1
EAU          = 2
EAU_MOUVANTE = 3
DIM          = 3

# n = nombre de matrices (profondeur) x est la coordonnée correspondante 
# p = nombre de lignes dans chaque matrices y est la coordonnée correspondante 
# q = nombre de coefficients dans chaque lignes ( colonne ) z est la coordonnée correspondante 

#Convention graphique
couleurs = {NEANT:        None  ,
            ROCHE:       'grey' ,
            VIDE:         None,
            EAU:         'blue' ,
            EAU_MOUVANTE:'cyan' }

def draw(espace, subplot, clrs):
    """Dessine chaque coefficient de la matrice comme un point de plot 3D."""
    for x, matrice in enumerate(espace):
        for y, line in enumerate(matrice):
            for z, coef in enumerate(line):
                if couleurs[coef] != None:
                    subplot.scatter(z, y, -x, c=couleurs[coef])

def modelisation(n, p, q, indice = 0.5, affichage = True):
    """Réalisation d'une propagation d'eau à travers un sol rocheux, retourne True si il y a percolation. """
    esp = espace(n, p, q, indice=.5)        # On crée un espace de départ de façon aléatoire
    etape_1 = initialisation(esp, indice) 
    eau_mouvante1 = etape_1[1]              # Les premières coordonnées d'eau mouvante 
    esp = etape_1[0]                        # L'ancien espace est remplacé par le nouveau 
    liste_vecteurs = vecteurs_espace(DIM)   # Liste des vecteurs possibles déplacement dans l'espace
    return percolation(esp, liste_vecteurs, eau_mouvante1, affichage)
    
def initialisation(esp, indice):
    """ Retourne l'espace une fois que la pluie est tombée et les premières coordonnées de l'eau mouvante. """
    eau_mouvante = []
    for y, ligne in enumerate(esp[0]):
        for z, coef in enumerate(ligne):
            if coef == VIDE:
                esp[0][y][z] = EAU_MOUVANTE
                eau_mouvante.append((0, y, z))
    return esp, eau_mouvante
    
def vecteurs_espace(dim):
    """Renvoie une liste des vecteurs possibles déplacement dans l'espace."""
    liste_vecteurs = []
    for direction in range(dim):
        for sens in [-1, 1]:
            vecteur = [0]*dim
            vecteur[direction] = sens
            liste_vecteurs.append(vecteur)
    return liste_vecteurs

def percolation(espace, liste_vecteurs, eau_mouvante1, affichage):
    """Affiche graphiquement la propagation de l'eau, et indique s'il y a percolation."""
    if affichage == True:
        fig = pyplot.figure()
        subplot = fig.add_subplot(111, projection='3d')
        subplot.set_xlabel('Z')
        subplot.set_ylabel('Y')
        subplot.set_zlabel('-X')

        draw([[[-1, 0, 1, 2, 3]]], subplot, couleurs) # TODO : pas necessaire 
        pyplot.pause(1)

    eau_mouvante = eau_mouvante1
    while eau_mouvante != []:               # Si il n'y a plus de d'eau mouvante dans l'espace 
        eau_mouvante = propagation(espace, eau_mouvante, liste_vecteurs)
        
        if affichage == True:
            draw(espace, subplot, couleurs)
            pyplot.pause(.0001)
            
    return resultat(espace)

def propagation(espace, eau_mouvante, liste_vecteurs):
    """Propage l'eau mouvante dans les cases vides."""
    pores_vides = []
    pores_vides_locale = []                 # Nécessaire pour ne pas enregistrer 2 fois un même pore 
    for (x, y, z) in eau_mouvante:
        pores_vides_locale = vide(espace, x, y, z, liste_vecteurs)
        matrice = infiltration(espace, pores_vides_locale)
        matrice[x][y][z] = EAU              # L' eau devient stagnante 
        pores_vides += pores_vides_locale
    eau_mouvante = list(pores_vides)        # les pores vides au temps t devienent l'eau mouvante au temps t+1
    return eau_mouvante
    
def vide(espace, x, y, z, liste_vecteurs): 
    """Renvoie la liste des coordonnées des pores vides autour d'une case d'eau mouvante."""
    pores_vides = []
    for vecteur in liste_vecteurs:          # La liste de possibilités de déplacement de l'eau 
         coords = (x+vecteur[0], y+vecteur[1], z+vecteur[2])
         if espace[coords[0]][coords[1]][coords[2]] == VIDE:
                pores_vides.append(coords)
    return pores_vides
    
def infiltration(espace, pores_vides):
    """Ajoute de l'eau mouvante dans les pores vides."""
    for (x, y, z) in pores_vides:
        espace[x][y][z] = EAU_MOUVANTE
    return espace
    
def resultat(espace): 
    """Indique s'il y a percolation ou pas."""
    matrice = espace[len(espace)-2]          # On ne considère que l'avant dernière matrice 
    ligne = 0
    coef = 0
    p = len(matrice)-2                      # nombre de lignes dans chaque matrices 
    q = len(matrice[0])-2                   # nombre de coefficients dans chaque lignes
    while ligne <= p and matrice[ligne][coef] != EAU: # TODO remarquez que ce n'est ps possible d'avoir de l'eau mouvante , tel que propagation est fait 
        if coef != q:  # Si on est pas arrivé au bout de la ligne 
            coef += 1  # On considère le coefficient suivant 
        else: 
            ligne += 1  # On considère la ligne suivante 
            coef = 0
    if ligne == p+1:    # Si on a parcouru toute la matrice sans trouver d'eau 
        return False
    else :
        return True
    
def espace(n, p, q, indice=.5):
    """Création d'une matrice modélisant une roche poreuse aléatoire."""
    espace = zero(n, p, q)              # On crée un volume rocheux 
    espace = pores(espace, indice)      # On ajoute des pores dans la roche 
    espace = bords(espace)              # On ajoute des limites au volume 
    return espace

def zero(n, p, q): 
    """Crée une matrice de zéros de taille n, p, q."""
    espace = [0]*n
    for i in range(n):
        espace[i] = [0]*p
        for j in range(p):
            espace[i][j]=[0]*q
    return espace

def pores(espace, indice=.5):
    """Introduit des pores vides au hasard, en fonction de l'indice de porosité."""
    for x, matrice in enumerate(espace):
        for y, ligne in enumerate(matrice):
            for z, coeff in enumerate(ligne):
                if random() < indice:           # L' ajout de vide est aléatoire et dépend de l'indice de porosité
                    espace[x][y][z] = VIDE
    return espace

def bords(espace):
    """Borde l'espace de NEANT, sur tous ses côtés, sauf à la surface."""
    for matrice in espace:                      # On borde chaque matrice de néant 
        for ligne in matrice:
            ligne.insert(0, NEANT) 
            ligne.append(NEANT)
        ligne_bas = [NEANT]*len(matrice[0])
        matrice.append(ligne_bas) 
        matrice.insert(0, ligne_bas)
    matrice_fond = [ligne_bas]*len(espace[0])
    espace.append(matrice_fond)                 # On insert une matrice de controle, en bas de l'espace
    return espace

if __name__ == '__main__': # Fonction de test
    print(modelisation(8, 8, 8, 0.9, False))
    
# Plus l'indice de prorosité est élevé plus la probabilité de percolation est grande 

"""Exemple de matrice qui percole:
M = [[[-1, -1, -1, -1, -1],
  [-1, 0, 0, 1, -1],
  [-1, 1, 1, 1, -1],
  [-1, 0, 0, 0, -1],
  [-1, -1, -1, -1, -1]],
 [[-1, -1, -1, -1, -1],
  [-1, 0, 1, 0, -1],
  [-1, 1, 1, 1, -1],
  [-1, 1, 0, 1, -1],
  [-1, -1, -1, -1, -1]],
 [[-1, -1, -1, -1, -1],
  [-1, 1, 0, 1, -1],
  [-1, 1, 0, 0, -1],
  [-1, 1, 1, 0, -1],
  [-1, -1, -1, -1, -1]],
 [[-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1]]]"""
  
"""Exemple de matrice qui ne percole pas:
M = [[[-1, -1, -1, -1, -1],
  [-1, 0, 0, 0, -1],
  [-1, 0, 0, 0, -1],
  [-1, 0, 0, 0, -1],
  [-1, -1, -1, -1, -1]],
 [[-1, -1, -1, -1, -1],
  [-1, 0, 0, 0, -1],
  [-1, 0, 0, 0, -1],
  [-1, 0, 0, 0, -1],
  [-1, -1, -1, -1, -1]],
 [[-1, -1, -1, -1, -1],
  [-1, 0, 0, 0, -1],
  [-1, 0, 0, 0, -1],
  [-1, 0, 0, 0, -1],
  [-1, -1, -1, -1, -1]],
 [[-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1],
  [-1, -1, -1, -1, -1]]]"""
