#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import random

def matrice(n, p, indice=.5):
    """Création d'une matrice modélisant une roche poreuse aléatoire."""
    matrice = zero(n, p)
    matrice = pores(matrice, indice)
    matrice = bords(matrice)
    return matrice

def zero(n, p):
    """ crééer une matrice de zéros de taille n,p """ 
    matrice = [0]*n
    for i in range(n):
        matrice[i] = [0]*p
    return matrice

def pores(matrice, indice=.5):
    """Introduit des pores vides au hasard, en fonction de l'indice de porosité i."""
    for i, ligne in enumerate(matrice):
        for j, coef in enumerate(ligne):
            if random() < indice:  
                matrice[i][j] = VIDE
    return matrice

def bords(matrice):
    """On borde la matrice de -1, sur trois côtés."""
    for ligne in matrice:
        ligne.insert(0, -1)
        ligne.append(-1)
    ligne_bas = [-1] * len(matrice[0]) 
    matrice.append(ligne_bas)
    return matrice


