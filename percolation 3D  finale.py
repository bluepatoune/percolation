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

DIM          = 3 # TODO: Soit le code est pour n dimensions et cette variable peut avoir du sens (encore que...), soit il ne l'est pas et c'est caduque. Vous vous trimballez partout des définitions de fonction avec du n, p, q ; même le nom de fichier dit que c'est de la dimension 3 uniquement... Ça n'a pas de sens de d"finir cela. Vous devriez alors définir une liste ou un tuple (c'est mieux d'ailleurs) dimensions tel que len(dimensions) = DIM (qui peut alors être (x, y), (x, y, z), (x, y, z, t) au choix.) Si une partie seulement du code est généralisée en n dimensions, à ce moment là vous mettez vos fonctions généralisées dans un autre fichier, et vous les importez dans celui ci.

couleurs = {NEANT:        None ,
            ROCHE:       'grey',
            VIDE:         None ,
            EAU:         'blue',
            EAU_MOUVANTE:'cyan'}

def draw(espace, subplot, clrs):
    """Dessine chaque coeficient d'un espace matriciel comme un point de plot 3D."""
    subplot.cla()
    for x, matrice in enumerate(espace):
        for y, line in enumerate(matrice):
            for z, coef in enumerate(line):
                if couleurs[coef] != None:
                    subplot.scatter(z, y, -x, c=couleurs[coef])

# Utilisation statistique de la fonction percolation

# TODO: Pourquoi elle s'appelle maximum_alveoles celle la ?
def maximum_alveoles(n, p, q, indices, echantillons, affichage=True):
    """Renvoie un dictionnaire associant une moyenne du nombre d'alvéoles à un indice de porosité.
    indices: Nombre d'indices à calculer, équirépartis de 0 à 1.
    echantillons: Taille de l'échantillon à calculer pour un indice donné.
    affichage: Si True, affiche en sus un graph du nombre d'alvéoles en fonction de l'indice."""
    vecteurs = vecteurs_espace(3)
    resultat = {}
    for indice in range(indices):
        indice_normalise = indice / indices
        nombre_alveoles = 0
        for echantillon in range(echantillons):
            espace = creation_espace(n, p, q, indice_normalise)
            nombre_alveoles += comptage_des_alveoles(espace, vecteurs)
        resultat[indice_normalise] = nombre_alveoles / echantillons
    if affichage:
        fig = pyplot.figure()
        subplot = fig.add_subplot(111)
        subplot.set_xlabel("Indice")
        subplot.set_ylabel("Moyenne d'alvéoles")
        subplot.plot(tuple(resultat.keys()), tuple(resultat.values()), 'g*')
        pyplot.pause(1)
    return resultat

# TODO: Voici l'ancienne maximum_alveoles. Je l'ai réécrite au final, mais je vous la laisse commentée pour que vous voyiez ce qui n'allait pas.
# def maximum_alveoles(n, p, q, N, P): # TODO: c'est une TRÈS MAUVAISE IDÉE d'avoir des variables n et N, p et P. n, p, q, ça va encore, mais il faut nommer plus clairement N et P.
#     """ renvoie la liste des indices et des moyennes de nombres d'alvéoles associés.
#     N: le nombre d'indices évalués
#     P: taille de l'échantillon statistique pour chaque indice""" # TODO: La premiere phrase est claire. J'ai mis ici vos commentaires qui n'étaient pas du tout judicieusement placés (vous devez QUAND MËME changer vos noms de variables N et P !)
#     moyennes_alveoles = []
#     indices = []
#     vecteurs = vecteurs_espace(DIM)
#     for d in range(N + 1):
#         indices.append(d / N)
#         nombre_alveoles = 0
#         for e in range(P):
#             espace = creation_espace(n, p, q, d/N)
#             nombre_alveoles += comptage_des_alveoles(espace, vecteurs)
#         moyennes_alveoles.append(nombre_alveoles / P) # moyenne empirique
#     pyplot.plot(indices, moyennes_alveoles,'g*',) # TODO: Vous espérez quoi en passant (,) en fin de fonction ?
#     return indices, moyennes_alveoles # TODO: C'est pas une bonne idée de renvoyer ça. Renvoyez un dictionnaire de N éléments type {indice1: moyenne1, indice2: moyenne2, ...}

def comptage_des_alveoles(espace, vecteurs):
    """Renvoie le nombre d'alvéoles dans un espace après percolation."""
    espace = deepcopy(espace) # Crée une copie au lieu d'une référence
    nombre_alveoles = 0
    for x, matrice in enumerate(espace):
        for y, ligne in enumerate(matrice): # reduire les -1 # TODO: Vous pouvez répéter la question ?
            for z, coef in enumerate(ligne):
                if coef == VIDE:
                    espace[x][y][z] = EAU_MOUVANTE
                    eau_mouvante = [(x, y, z)]
                    espace = percolation(espace, vecteurs, eau_mouvante, affichage=False)
                    nombre_alveoles += 1
    return nombre_alveoles

# Utilisation de la fonction percolation pour un espace particulier

def main(n, p, q, indice, affichage=True):
    """ Renvoie le resultat de la percolation et le nombre d'alvéole pour un espace """
    espace = creation_espace(n, p, q, indice)        # On crée un espace de départ de façon aléatoire
    vecteurs = vecteurs_espace(DIM)   # Liste des vecteurs possibles déplacement dans l'espace
    return comptage_des_alveoles(espace, vecteurs), modelisation(espace, vecteurs, affichage)

def creation_espace(n, p, q, indice=.5):
    """Création d'un espace une roche poreuse aléatoire."""
    espace = zero(n, p, q)              # On crée un volume rocheux
    espace = pores(espace, indice)      # On ajoute des pores dans la roche
    espace = bords(espace)              # On ajoute des limites au volume
    return espace

def zero(n, p, q):
    """Crée un espace de zéros de taille n, p, q."""
    espace = [ROCHE] * n
    for i in range(n): # TODO: Vous pourriez balancer une list comprehension ici
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
        ligne_bas = [NEANT] * len(matrice[0])
        matrice.append(ligne_bas)
        matrice.insert(0, ligne_bas)
    matrice_fond = [ligne_bas] * len(espace[0]) # TODO: ligne_bas n'a pas le bon nom, elle n'est pas toujours en bas
    espace.append(matrice_fond) # On insert une matrice de controle, en bas de l'espace # TODO: Pardon ?
    return espace

def vecteurs_espace(dim):
    """Renvoie une liste des vecteurs de déplacements possibles dans l'espace."""
    vecteurs = []
    for direction in range(dim):
        for sens in [-1, 1]:
            vecteur = [0] * dim
            vecteur[direction] = sens
            vecteurs.append(vecteur)
    return vecteurs

def modelisation(espace, vecteurs, affichage=True):
    """Réalisation d'une propagation d'eau à travers un sol rocheux, retourne True si il y a percolation.""" # TODO: Nom de fonction trop générique...
    etape_1 = initialisation(espace)        # Modélisation de la pluie
    eau_mouvante1 = etape_1[1]              # Les premières coordonnées d'eau mouvante # TODO: Non mais arrêtez avec vos variables intermédiaires au nom impossible...
    espace = etape_1[0]                     # L'ancien espace est remplacé par le nouveau
    espace = percolation(espace, vecteurs, eau_mouvante1, affichage)
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

def percolation(espace, vecteurs, eau_mouvante1, affichage=True):
    """Renvoie l'espace après propagationde l'eau."""
    if affichage:
        fig = pyplot.figure()
        subplot = fig.add_subplot(111, projection='3d')
        subplot.set_xlabel('Z')
        subplot.set_ylabel('Y')
        subplot.set_zlabel('-X')

        draw([[[-1, 0, 1, 2, 3]]], subplot, couleurs)
        pyplot.pause(1)

    eau_mouvante = eau_mouvante1
    while eau_mouvante != []:          #Tant qu'il n'y a plus de d'eau mouvante dans l'espace
        eau_mouvante = propagation(espace, eau_mouvante, vecteurs)
        if affichage:
            draw(espace, subplot, couleurs)
            pyplot.pause(.0001)

    return espace

def propagation(espace, eau_mouvante, vecteurs):
    """Renvoie les coordonnées des nouvelles particules d'eau mouvante après propagation de l'eau."""
    nouvelle_eau_mouvante = []
    pores_vides_locaux = []          # Nécessaire pour ne pas enregistrer 2 fois un même pore
    for (x, y, z) in eau_mouvante:
        pores_vides_locaux = vide(espace, x, y, z, vecteurs)
        matrice = infiltration(espace, pores_vides_locaux)
        matrice[x][y][z] = EAU              # L' eau devient stagnante
        nouvelle_eau_mouvante += pores_vides_locaux  # les pores vides au temps t devienent l'eau mouvante au temps t+1
    return nouvelle_eau_mouvante

def vide(espace, x, y, z, vecteurs):
    """Renvoie la liste des coordonnées des pores vides autour d'une case d'eau mouvante."""
    pores_vides = []
    for vecteur in vecteurs:          # La liste de possibilités de déplacement de l'eau
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
    matrice = espace[len(espace)-2]
    for ligne in matrice:
        for coef in ligne:
            if coef == EAU:
                return True
    return False

# TODO: Voici votre ancienne fonction pour référence.
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

if __name__ == '__main__': # Tests
    main(3, 4, 5, 0.5)
    print(maximum_alveoles(3, 3, 3, 100, 200))
    pyplot.show()
