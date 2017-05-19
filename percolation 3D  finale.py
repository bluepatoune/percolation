#!/usr/bin/env python3

"""Percolation.py: Un module python pour effectuer des percolations matricielles. \n
n = nombre de matrices                        (x)
p = nombre de lignes dans chaque matrice      (y)
q = nombre de coefficients dans chaque ligne  (z)"""

from matplotlib           import pyplot, colors
from mpl_toolkits.mplot3d import Axes3D
from random               import random
from copy                 import deepcopy

NEANT        = -1
ROCHE        = 0
VIDE         = 1
EAU          = 2
EAU_MOUVANTE = 3

couleurs = {NEANT:        None  ,
            ROCHE:       'grey' ,
            VIDE:        'white',
            EAU:         'red' ,
            EAU_MOUVANTE:'cyan' }

def draw(espace, subplot, clrs):
    """Dessine chaque coefficient d'un espace matriciel comme un point de plot 3D."""
    subplot.cla()
    for x, matrice in enumerate(espace):
        for y, ligne in enumerate(matrice):
            for z, coef in enumerate(ligne):
                if couleurs[coef] != None:
                    subplot.scatter(z, y, -x, c=couleurs[coef])



# Utilisation de la fonction percolation pour un espace particulier

def etude_un_espace(n, p, q, indice, affichage=True):
    """ Renvoie le resultat de la percolation et le nombre de composantes connexes pour un espace """
    espace = creation_espace(n, p, q, indice)        # On crée un espace de départ de façon aléatoire
    vecteurs = vecteurs_espace(3)   # Liste des vecteurs possibles déplacement dans l'espace
    return nombre_composantes_connexes(espace, vecteurs), percolation(espace, vecteurs, affichage)

def creation_espace(n, p, q, indice=.5):
    """Création d'un espace une roche poreuse aléatoire."""
    espace = zero(n, p, q)              # On crée un volume rocheux
    espace = pores(espace, indice)      # On ajoute des pores dans la roche
    espace = bords(espace)              # On ajoute des limites au volume
    return espace

def zero(n, p, q):
    """Crée un espace de zéros de taille n, p, q."""
    espace = [ROCHE] * n
    for i in range(n): 
        espace[i] = [ROCHE] * p
        for j in range(p):
            espace[i][j] = [ROCHE] * q
    return espace

def pores(espace, indice=.5):
    """Introduit des pores vides au hasard, en fonction de l'indice de porosité."""
    for x, matrice in enumerate(espace):
        for y, ligne in enumerate(matrice):
            for z, coeff in enumerate(ligne):
                if random() < indice:
                    espace[x][y][z] = VIDE
    return espace
  # Plus l'indice de prorosité est élevé plus la probabilité de percolation est grande

def bords(espace):
    """On borde l'espace de NEANT, sur tous ses côtés, sauf à la surface."""
    for matrice in espace:
        for ligne in matrice:
            ligne.insert(0, NEANT)
            ligne.append(NEANT)
        ligne_limite = [NEANT] * len(matrice[0])
        matrice.append(ligne_limite)
        matrice.insert(0, ligne_limite)
    matrice_fond = [ligne_limite] * len(espace[0]) 
    espace.append(matrice_fond) # cela représente la limite inférieure du sol 
    return espace

def vecteurs_espace(dim):
    """Renvoie une liste des vecteurs de déplacements possibles dans l'espace."""
    vecteurs = []
    for direction in range(3):
        for sens in [-1, 1]:
            vecteur = [0] * 3
            vecteur[direction] = sens
            vecteurs.append(vecteur)
    return vecteurs
    
def nombre_composantes_connexes(espace, vecteurs):
    """Renvoie le nombre d'alvéoles dans un espace après percolation."""
    espace = deepcopy(espace)               # Crée une copie au lieu d'une référence
    nombre_composantes_connexes = 0
    for x, matrice in enumerate(espace):
        for y, ligne in enumerate(matrice):
            for z, coef in enumerate(ligne):
                if coef == VIDE:
                    espace[x][y][z] = EAU_MOUVANTE
                    eau_mouvante = [(x, y, z)]
                    espace = infiltration(espace, vecteurs, eau_mouvante, affichage=False)
                    nombre_composantes_connexes += 1
    return nombre_composantes_connexes

def percolation(espace, vecteurs, affichage=True):
    """Réalisation d'une coordonnees_eau d'eau à travers un sol rocheux, retourne True si il y a percolation.""" 
    etat_initial = initialisation(espace)        # Modélisation de la pluie
    eau_mouvante1 = etat_initial[1]              # Les premières coordonnées d'eau mouvante 
    espace = etat_initial[0]                     # L'ancien espace est remplacé par le nouveau
    espace = infiltration(espace, vecteurs, eau_mouvante1, affichage)
    return resultat(espace)

def initialisation(espace):
    """ Retourne l'espace une fois que la pluie est tombée et les premières coordonnées de l'eau mouvante """
    eau_mouvante = []
    for y, ligne in enumerate(espace[0]):
        for z, coef in enumerate(ligne):
            if coef == VIDE:
                espace[0][y][z] = EAU_MOUVANTE
                eau_mouvante.append((0, y, z))
    return espace, eau_mouvante

def infiltration(espace, vecteurs, eau_mouvante, affichage=True):
    """Renvoie l'espace après infiltration de l'eau."""
    if affichage:
        fig = pyplot.figure()
        subplot = fig.add_subplot(111, projection='3d')
        subplot.set_xlabel('Z')
        subplot.set_ylabel('Y')
        subplot.set_zlabel('-X')

        draw([[[-1, 0, 1, 2, 3]]], subplot, couleurs)
        pyplot.pause(1)

    eau_mouvante = eau_mouvante
    while eau_mouvante != []:          #Tant qu'il y a de l'eau mouvante dans l'espace
        eau_mouvante = coordonnees_eau(espace, eau_mouvante, vecteurs)
        
        if affichage:
            draw(espace, subplot, couleurs)
            pyplot.pause(.0001)

    return espace

def coordonnees_eau(espace, eau_mouvante, vecteurs):
    """Renvoie les coordonnées des nouvelles particules d'eau mouvante après l'infiltration de l'eau."""
    nouvelle_eau_mouvante = []
    pores_vides_locaux = []          # Nécessaire pour ne pas enregistrer 2 fois un même pore
    for (x, y, z) in eau_mouvante:
        pores_vides_locaux = coordonnees_vide(espace, x, y, z, vecteurs)
        matrice = deplacement_eau(espace, pores_vides_locaux)
        matrice[x][y][z] = EAU              # L' eau devient stagnante
        nouvelle_eau_mouvante += pores_vides_locaux  # les pores vides au temps t deviennent l'eau mouvante au temps t+1
    return nouvelle_eau_mouvante

def coordonnees_vide(espace, x, y, z, vecteurs):
    """Renvoie la liste des coordonnées des pores vides autour d'une case d'eau mouvante."""
    pores_vides = []
    for vecteur in vecteurs:          # La liste de possibilités de déplacement de l'eau
         coords = (x+vecteur[0], y+vecteur[1], z+vecteur[2])
         if espace[coords[0]][coords[1]][coords[2]] == VIDE:
                pores_vides.append(coords)
    return pores_vides

def deplacement_eau(espace, pores_vides):
    """Ajoute de l'eau mouvante dans les pores vides."""
    for (x, y, z) in pores_vides:
        espace[x][y][z] = EAU_MOUVANTE
    return espace

def resultat(espace):
    """Indique s'il y a percolation ou pas."""
    matrice = espace[len(espace)-2]
    for ligne in matrice:
        for coef in ligne:
            if coef == EAU:
                return True
    return False

# TODO: Voici l' ancienne fonction avec un while.
# def resultat(espace):
#     """Indique s'il y a percolation ou pas."""
#     matrice = espace[len(espace)-2]          # On ne considère que l'avant dernière matrice
#     y, z = 0, 0
#     p = len(matrice)-2                      # nombre de lignes dans chaque matrices
#     q = len(matrice[0])-2                   # nombre de coefficients dans chaque lignes
#     while y <= p and matrice[y][z] != EAU:
#         if z != q:  # Si on est pas arrivé au bout de la ligne
#             z += 1  # On considère le coefficient suivant
#         else:
#             y += 1  # On considère la ligne suivante
#             z = 0
#     if y == p + 1:
#         return False
#     return True

# Utilisation statistique de la fonction percolation

def indices_composantes_connexes(n, p, q, indices, echantillons, affichage=True): # avec un dictionnaire 
    """Renvoie un dictionnaire associant une moyenne du nombre de composantes connexes à un indice de porosité.
    indices: Nombre d'indices à calculer, équirépartis de 0 à 1.
    echantillons: Taille de l'échantillon à calculer pour un indice donné.
    affichage: Si True, affiche un graph du nombre de composantes connexes en fonction de l'indice."""
    vecteurs = vecteurs_espace(3)
    resultat = {}
    for indice in range(indices):
        indice_normalise = indice / indices
        somme_composantes_connexes = 0
        for echantillon in range(echantillons):
            espace = creation_espace(n, p, q, indice_normalise)
            somme_composantes_connexes += nombre_composantes_connexes(espace, vecteurs)
        resultat[indice_normalise] = somme_composantes_connexes / echantillons
    
    if affichage:
        fig = pyplot.figure()
        subplot = fig.add_subplot(111)
        subplot.set_xlabel("Indice")
        subplot.set_ylabel("Moyenne de composantes connexes")
        subplot.plot(tuple(resultat.keys()), tuple(resultat.values()), 'g*')
    
    return resultat

def indices_composantes_connexes(n, p, q, nbindices, nbechantillons, affichage=True): # avec des listes 
    """Renvoie deux listes associant une moyenne du nombre de composantes connexes à un indice de porosité.
    nbindices: Nombre d'indices à calculer, équirépartis de 0 à 1.
    nbechantillons: Taille de l'échantillon à calculer pour un indice donné.
    affichage: Si True, affiche un graph du nombre de composantes connexes en fonction de l'indice."""
    moyennes = []
    indices = []   
    vecteurs = vecteurs_espace(3)
    for indice in range(nbindices):
        indice_normalise = indice / nbindices
        indices.append(indice_normalise)
        somme_composantes_connexes = 0
        for echantillon in range(nbechantillons):
            espace = creation_espace(n, p, q, indice_normalise)
            somme_composantes_connexes += nombre_composantes_connexes(espace, vecteurs)
        moyennes.append(somme_composantes_connexes / nbechantillons)
    
    if affichage:
        fig = pyplot.figure()
        subplot = fig.add_subplot(111)
        subplot.set_xlabel("Indice")
        subplot.set_ylabel("Moyenne des composantes connexes")
        subplot.plot(indices, moyennes, 'g*')
    return indices, moyennes

def enumerer(iterable):
    """  un codage de enumerate """
    i= 0
    for item in iterable:
        yield i, item        # renvoie un i, item puis la fonction est en pause et continue lorsqu'elle est rappellé 
        i += 1 

def enum(x):
    """ un codage simplifié de enumerate """
    return [(i, x[i]) for i in range(len(x))]
    
def copie(espace):
    """ réalise une copie proche de deepcopy """ 
    n = len(espace) 
    p = len(espace[0])
    q = len(espace[0][0])
    espace2 = zero(n, p, q)
    for x in range(n):
        for y in range(p):
            for z in range(q):
                espace2[x][y][z] = espace[x][y][z]
    return espace2
        
if __name__ == '__main__': # fonctions de tests
    etude_un_espace(3, 4, 5, 0.5)
    indices_composantes_connexes(3, 3, 3, 100, 200)
