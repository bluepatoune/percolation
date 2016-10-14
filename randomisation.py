#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import random

def matrice(n, p, indice=.5):
    """Création d'une matrice modélisant une roche poreuse aléatoire. 0 indique la roche, 1 indique un pore."""
    matrice = zero(n, p)
    matrice = pores(matrice, indice)
    matrice = bords(matrice)
    return matrice

def zero(n, p):
    """ Créer une matrice de zéros de taille (n, p) """
    return [[0]*p for i in xrange(n)]

def pores(matrice, indice=.5):
    """Introduit des pores au hasard, en fonction de l'indice de porosité i."""
    for i, ligne in enumerate(matrice):
        for j, coef in enumerate(ligne):    # NOTE: MAIS PUTAIN C'EST TELLEMENT PLUS BEAU !!!
            if random() < indice:  # NOTE: """en fonction de l'indice de porosité i"""... Ben voyons... Bon, je l'ai fait du coup.
                matrice[i][j] = 1
    return matrice

def liste(k, indice=.5): # NOTE: Je l'ai fait aussi dans la foulée (mais à quoi ça sert mystère)
    """Retourne une liste de 0 et de 1, de k éléments, en fonction de l'indice de porosité."""
    liste = [0]*k
    for i, element in enumerate(liste):
        if random() < indice:
            liste[i] = 1
    return liste

def bords(matrice):
    """On borde la matrice de -1, sur trois côtés."""
    for ligne in matrice:
        ligne.insert(0, -1)
        ligne.append(-1)
    ligne_bas = [-1] * len(matrice[0]) # TODO: Ce serait tellement plus beau avec une propriété de classe
    matrice.append(ligne_bas)
    return matrice

# NOTE: Je vous en supplie, regardez comment marche la fonction for de python et ARRÊTEZ D'ITÉRER SUR DES INDEX PAR PITIÉÉÉÉÉÉÉ JE SOUUUFFRE AAAARGKUFDH
