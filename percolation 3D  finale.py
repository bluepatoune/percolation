#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Percolation.py: Un module python pour effectuer des percolations matricielles."""

from matplotlib           import pyplot
from matplotlib           import colors
from mpl_toolkits.mplot3d import Axes3D
from random               import random
from copy                 import deepcopy

#Convention de codage:
NEANT        = -1
ROCHE        = 0
VIDE         = 1
EAU          = 2
EAU_MOUVANTE = 3
DIM          = 3

# n = nombre de matrices (profondeur) x est la coordonnée correspaceondante 
# p = nombre de lignes dans chaque matrices y est la coordonnée correspaceondante 
# q = nombre de coefficients dans chaque lignes ( colonne ) z est la coordonnée correspaceondante 

#Convention graphique
couleurs = {NEANT:        None  ,
            ROCHE:       'grey' ,
            VIDE:         None,
            EAU:         'blue' ,
            EAU_MOUVANTE:'cyan' }
            
def draw(espace, subplot, clrs):
    """Dessine chaque coeficient de la matrice comme un point de plot 3D."""
    for x, matrice in enumerate(espace):
        for y, line in enumerate(matrice):
            for z, coef in enumerate(line):
                if couleurs[coef] != None:
                    subplot.scatter(z, y, -x, c=couleurs[coef])
                    
def percolation_critique(n, p, q, N, P):
    proba = []
    indice = []
    liste_vecteurs = vecteurs_espace(DIM) 
    for d in range(N+1): # N le pas 
        indice += [d/N]
    for i in indice:
        S = 0
        for e in range(P): # iterrtion 
            espace = creation_espace(n, p, q, i) 
            percole = modelisation(espace, liste_vecteurs, False)
            if percole == True:
                S += 1
        proba += [S/P]
    pyplot.plot(indice, proba)
    return indice, proba
            
def comptage_des_ilots(espace, liste_vecteurs):
    espace2 = deepcopy(espace)
    compteur = 0
    for x, matrice in enumerate(espace2):
        for y, ligne in enumerate(matrice): # reduire les -1 
            for z, coef in enumerate(ligne):
                if coef == VIDE:
                    compteur += 1
                    espace2[x][y][z] = EAU_MOUVANTE 
                    eau_mouvante1 = [(x,y,z)] 
                    espace2 = percolation(espace2, liste_vecteurs, eau_mouvante1,False)
    return compteur

def modelisation(espace, liste_vecteurs, affichage = True):
    """réalisation d'une propagation d'eau à travers un sol rocheux, retourne True si il y a percolation """
    etape_1 = initialisation(espace) 
    eau_mouvante1 = etape_1[1]              # Les premières coordonnées d'eau mouvante 
    espace = etape_1[0]                        # L'ancien creation_espace est remplacé par le nouveau 
    espace = percolation(espace, liste_vecteurs, eau_mouvante1, affichage)
    return resultat(espace)
    
def percolation_critique(n, p, q, N, P):
    proba = []
    indice = []
    liste_vecteurs = vecteurs_espace(DIM) 
    for d in range(N+1): # N le pas 
        indice += [d/N]
    for i in indice:
        S = 0
        for e in range(P): # iterrtion 
            espace = creation_espace(n, p, q, i) 
            percole = modelisation(espace, liste_vecteurs, False)
            if percole == True:
                S += 1
        proba += [S/P]
    pyplot.plot(indice, proba)
    return indice, proba
    
def initialisation(espace):
    """ Retourne l'creation_espace une fois que la pluie est tombée et les premières coordonnées de l'eau mouvante """
    eau_mouvante = []
    for y, ligne in enumerate(espace[0]):
        for z, coef in enumerate(ligne):
            if coef == VIDE:
                espace[0][y][z] = EAU_MOUVANTE
                eau_mouvante.append((0, y, z))
    return espace, eau_mouvante
    
def vecteurs_espace(dim):
    """Renvoie une liste des vecteurs possibles déplacement dans l'creation_espace."""
    liste_vecteurs = []
    for direction in range(dim):
        for sens in [-1, 1]:
            vecteur = [0]*dim
            vecteur[direction] = sens
            liste_vecteurs.append(vecteur)
    return liste_vecteurs

def percolation(creation_espace, liste_vecteurs, eau_mouvante1, affichage):
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
    while eau_mouvante != []:               # Si il n'y a plus de d'eau mouvante dans l'creation_espace 
        eau_mouvante = propagation(creation_espace, eau_mouvante, liste_vecteurs)
        
        if affichage == True:
            draw(creation_espace, subplot, couleurs)
            pyplot.pause(.0001)
            
    return creation_espace

def propagation(creation_espace, eau_mouvante, liste_vecteurs):
    """Renvoie les coordonnées des nouvelles cases d'eau mouvante après propagation de l'eau."""
    pores_vides = []
    pores_vides_locale = []                 # Nécessaire pour ne pas enregistrer 2 fois un même pore 
    for (x, y, z) in eau_mouvante:
        pores_vides_locale = vide(creation_espace, x, y, z, liste_vecteurs)
        matrice = infiltration(creation_espace, pores_vides_locale)
        matrice[x][y][z] = EAU              # L' eau devient stagnante 
        pores_vides += pores_vides_locale
    eau_mouvante = list(pores_vides)        # les pores vides au temps t devienent l'eau mouvante au temps t+1
    return eau_mouvante
    
def vide(creation_espace, x, y, z, liste_vecteurs): 
    """Renvoie la liste des coordonnées des pores vides autour d'une case d'eau mouvante."""
    pores_vides = []
    for vecteur in liste_vecteurs:          # La liste de possibilités de déplacement de l'eau 
         coords = (x+vecteur[0], y+vecteur[1], z+vecteur[2])
         if creation_espace[coords[0]][coords[1]][coords[2]] == VIDE:
                pores_vides.append(coords)
    return pores_vides
    
def infiltration(creation_espace, pores_vides):
    """Ajoute de l'eau mouvante dans les pores vides."""
    for (x, y, z) in pores_vides:
        creation_espace[x][y][z] = EAU_MOUVANTE
    return creation_espace
    
def resultat(creation_espace): 
    """Indique s'il y a percolation ou pas."""
    matrice = creation_espace[len(creation_espace)-2]          # On ne considère que l'avant dernière matrice 
    y = 0
    z = 0
    p = len(matrice)-2                      # nombre de lignes dans chaque matrices 
    q = len(matrice[0])-2                   # nombre de coefficients dans chaque lignes
    while y <= p and matrice[y][z] != EAU: # TODO remarquez que ce n'est ps possible d'avoir de l'eau mouvante , tel que propagation est fait 
        if z != q:  # Si on est pas arrivé au bout de la ligne 
            z += 1  # On considère le coefficient suivant 
        else: 
            y += 1  # On considère la ligne suivante 
            z = 0
    if y == p+1:    # Si on a parcouru toute la matrice sans trouver d'eau 
        return False
    else :
        return True
    
def creation_espace(n, p, q, indice=.5):
    """Création d'une matrice modélisant une roche poreuse aléatoire."""
    espace = zero(n, p, q)              # On crée la un volume rocheux 
    espace = pores(espace, indice)      # On ajoute des pores dans la roche 
    espace = bords(espace)              # On ajoute des limite au volume 
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
                if random() < indice:           # l' ajout de vide est aléatoire et dépend de l'indice de porosité
                    espace[x][y][z] = VIDE
    return espace

def bords(espace):
    """On borde l'espace de NEANT, sur tous ses côtés, sauf à la surface."""
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
    espace = creation_espace(3, 3, 3, 0.9)        # On crée un espace de départ de façon aléatoire
    liste_vecteurs = vecteurs_espace(DIM)   # Liste des vecteurs possibles déplacement dans l'espace
    print(comptage_des_ilots(espace, liste_vecteurs))
    print(modelisation(espace, liste_vecteurs))
    
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
