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
                
# Génération aléatoire de l'espace de départ représentant la roche poreuse: 
def zero(n, p, q):
    """Crée un espace en 3 dimensions de zéros de taille n, p, q."""
    espace = [ROCHE] * n
    for y in range(n): 
        espace[y] = [ROCHE] * p
        for z in range(p):
            espace[y][z] = [ROCHE] * q
    return espace

def pores(espace, indice=.5):
    """Introduit des pores vides au hasard, en fonction de l'indice de porosité. Plus l'indice de prorosité est élevé plus la probabilité de percolation est grande"""
    for x, matrice in enumerate(espace):
        for y, ligne in enumerate(matrice):
            for z, coeff in enumerate(ligne):
                if random() < indice:
                    espace[x][y][z] = VIDE
    return espace

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
    
def creation_espace(n, p, q, indice=.5):
    """Création d'un espace de façon aléatoire."""
    espace = zero(n, p, q)              # On crée un volume rocheux
    espace = pores(espace, indice)      # On ajoute des pores dans la roche
    espace = bords(espace)              # On ajoute des limites au volume
    return espace

def vecteurs_deplacement(dim):
    """Renvoie une liste des vecteurs de déplacements possibles dans l'espace en n dimensions"""
    vecteurs = []
    for direction in range(dim):
        for sens in [-1, 1]:
            vecteur = [0] * dim
            vecteur[direction] = sens
            vecteurs.append(vecteur)
    return vecteurs

def initialisation(espace):
    """ Retourne l'espace une fois que la pluie est tombée 
    et les premières coordonnées de l'eau mouvante """
    eau_mouvante = []
    for y, ligne in enumerate(espace[0]):
        for z, coef in enumerate(ligne):
            if coef == VIDE:
                espace[0][y][z] = EAU_MOUVANTE
                eau_mouvante.append((0, y, z))
    return espace, eau_mouvante
    
def coordonnees_vide(espace, x, y, z, vecteurs):
    """Renvoie la liste des coordonnées des pores vides autour d'une case de coordonnées données en argument en fonction des vecteurs de déplacement"""
    pores_vides = []
    for vecteur in vecteurs:          
         coords = (x+vecteur[0], y+vecteur[1], z+vecteur[2])
         if espace[coords[0]][coords[1]][coords[2]] == VIDE:
                pores_vides.append(coords)
    return pores_vides

def deplacement_eau(espace, pores_vides):
    """Ajoute de l'eau mouvante dans les pores vides."""
    for (x, y, z) in pores_vides:
        espace[x][y][z] = EAU_MOUVANTE
    return espace
    
def coordonnees_eau(espace, eau_mouvante, vecteurs):
    """Renvoie les coordonnées des nouvelles particules d'eau mouvante après l'infiltration de l'eau. Les pores vides au temps t deviennent l'eau mouvante au temps t+1"""
    nouvelle_eau_mouvante = []
    pores_vides_locaux = [] 
    # Nécessaire pour ne pas enregistrer 2 fois un même pore
    for (x, y, z) in eau_mouvante:
        pores_vides_locaux = coordonnees_vide(espace, x, y, z, vecteurs)
        matrice = deplacement_eau(espace, pores_vides_locaux)
        matrice[x][y][z] = EAU          # L' eau mouvante devient stagnante
        nouvelle_eau_mouvante += pores_vides_locaux  
    return nouvelle_eau_mouvante

def infiltration(espace, vecteurs, eau_mouvante, affichage=True):
    """Renvoie l'espace après infiltration de l'eau.
    affichage: si True, affiche l'infiltration progressive de l'eau  dans l'espace 3D"""
    if affichage:
        fig = pyplot.figure()
        subplot = fig.add_subplot(111, projection='3d')
        subplot.set_xlabel('Z')
        subplot.set_ylabel('Y')
        subplot.set_zlabel('-X')

        draw([[[-1, 0, 1, 2, 3]]], subplot, couleurs)
        pyplot.pause(1)

    while eau_mouvante != []: # Tant qu'il y a de d'eau mouvante dans l'espace
        eau_mouvante = coordonnees_eau(espace, eau_mouvante, vecteurs)
        
        if affichage:
            draw(espace, subplot, couleurs)
            pyplot.pause(.0001)
    return espace
    
def resultat(espace):
    """Indique s'il y a percolation ou pas.
    Renvoie True si il y a de l'eau stagnante dans la dernière matrice"""
    matrice = espace[len(espace)-2] # La matrice juste avant la matrice limite    
    majorant_ligne = len(matrice) 
    majorant_coef = len(matrice[0])
    indice_ligne = 0 
    indice_coef =  majorant_coef
    while indice_ligne < majorant_ligne and indice_coef == majorant_coef:
        indice_coef = 0 # debut de ligne 
        while indice_coef < majorant_coef and matrice[indice_ligne][indice_coef] != EAU:
            indice_coef += 1 # balaye la ligne 
        indice_ligne += 1
    return not indice_coef == majorant_coef 
    
def percolation(espace, vecteurs, affichage=True):
    """Après l'infiltration de l'eau à travers un sol rocheux à 3 dimensions,
    renvoie True si il y a percolation.""" 
    etat_initial = initialisation(espace)    # Modélisation de la pluie
    premiere_eau_mouvante = etat_initial[1]           
    espace = etat_initial[0]                 # initialisation de l'espace 
    espace = infiltration(espace, vecteurs, premiere_eau_mouvante, affichage)
    return resultat(espace)

def nombre_composantes_connexes(espace, vecteurs):
    """Renvoie le nombre de composantes connexes dans un espace à 3 dimensions."""
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

# Utilisation des fonctions percolation et nombre_composantes_connexes 
# Pour un espace généré aléatoirement:
def etude_un_espace(n, p, q, indice, affichage=True):
    """ Renvoie le resultat de la percolation et
    le nombre de composantes connexes pour un espace à 3 dimensions"""
    espace = creation_espace(n, p, q, indice)        
    vecteurs = vecteurs_deplacement(3) # Les vecteurs en 3 dimensions
    copie_espace = deepcopy(espace) # On ne modifie pas l'espace d'origine
    return nombre_composantes_connexes(copie_espace, vecteurs), percolation(espace, vecteurs, affichage)
    
# Utilisation statistique:
def indices_moyennes_composantes_connexes(n, p, q, nbindices, nbechantillons, affichage=True): 
    """Renvoie deux listes: les indices de porosité et les moyennes du nombre de composantes connexe associées. 
    nbindices: Nombre d'indices à calculer, équirépartis de 0 à 1.
    nbechantillons: Taille de l'échantillon à calculer, assez grand pour appliquer la loi des grands nombres  
    affichage: Si True, affiche un graph des moyennes de composantes connexes en fonction de l'indice."""
    moyennes = []
    indices = []   
    vecteurs = vecteurs_deplacement(3)
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
        subplot.set_xlabel("Indice de porosité")
        subplot.set_ylabel("Moyenne des composantes connexes")
        subplot.plot(indices, moyennes, 'g*')
    return indices, moyennes

# Recodage des fonctions python utilisées:
def enumerer1(iterable):
    """  un codage de enumerate """
    i= 0
    for item in iterable:
        yield i, item        
        i += 1 
# yield renvoie un i, item puis la fonction est en pause et continue lorsqu'elle est rappellée 

def enumerer2(x):
    """ un codage simplifié de enumerate """
    return [(i, x[i]) for i in range(len(x))]
    
def copie(espace):
    """ réalise une copie proche de deepcopy """ 
    n = len(espace) 
    p = len(espace[0])
    q = len(espace[0][0])
    espace_copie = zero(n, p, q)
    for x in range(n):
        for y in range(p):
            for z in range(q):
                espace_copie[x][y][z] = espace[x][y][z]
    return espace_copie
    
# fonctions de tests:        
if __name__ == '__main__':
    print(etude_un_espace(3, 4, 5, 0.5,False))
    indices_moyennes_composantes_connexes(3, 3, 3, 50, 1000)
    pyplot.show()
