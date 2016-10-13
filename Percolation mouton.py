#!/usr/bin/python

from matplotlib import pyplot as plt
from matplotlib.pyplot import matshow

#exemple de matrice 
#RP=[[-1,0,0,0,0,1,-1],[-1,1,1,1,0,1,-1],[-1,1,0,1,1,1,-1],[-1,1,0,0,1,0,-1],[-1,1,0,0,1,0,-1],[-1,-1,-1,-1,-1,-1,-1]]

EAU = 2
VIDE = 1
PIERRE = 0

def percolation(n, p, T, i):
    """ Indique s'il y a percolation ou pas """
    P = matrice(n, p, i)
    E = P.copy()        #On a le droit ?
    E = pluie(P, E)
    for t in range(T):
        pores_vides2 = []
        for x in range(len(P)):           #lignes.
            for y in range(1, len(P[0])):   #colonnes.
                if E[x][y] == EAU:
                    pores_vides = regard(P, E, x, y)
                    pores_vides2 += regard(P, E, x, y)
                    E = infiltration(E, pores_vides)
        matshow(E, 1)
        plt.pause(0.000001)
        if pores_vides2 == []:                         #Si aucunes cases n'a de voisines vides.
            return resultat(pores_vides2, E, n, p)
    
def resultat(pores_vides2, E, n, p):
    c = False
    for e in range(p+1):
        if E[n-1][e] == EAU:
            c = True
    return c

def pluie(P, E):
    """ Ajoute de l'eau en surface """
    for i in range(len(P[0])):
        if P[0][i] == VIDE:
            E[0][i] = EAU 
    return E



def regard (P, E, x, y):
    """Renvoie la liste des coodonnées des pores vides autour d'une case d'eau """
    pores_vides=[]
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 or j == 0:
                if P[x+i][y+j] == VIDE and  E[x+i][y+j] == VIDE:        #Un if  ou deux ?
                    pores_vides += [[x+i, y+j]]
    return pores_vides

def infiltration(E,pores_vides):
    """ Ajoute de l'eau dans les pores vides """
    for i in pores_vides:
        E[i[0]][i[1]] = EAU
    return E

#if __name__ == '__main__':
    #if percolation(10, 10, 10) == True:
     #   print ("super ça percole")
    #else:
      #  print ("Try again !")
        
        

#  ==[ COMMENTAIRES ]==

#Vous devez définir clairement vos variables par leur nom ou dans le docstr des fonctions. En l'état, on comprend rien sans la structure de l'algo.

#Ne jamais prendre de lettre majuscule en nom de variable.

#Idem pour les noms de variable en majuscule ou commencant par une majuscule : à bannir, les majuscules sont réservées au CONSTANTES ou aux Classes.

#L'histoire de correspondance 0 1 2 avec VIDE EAU machin truc est à expliciter (un EAU = 2, VIDE = 0 en début de code est une piste envisageable)

#Aérez le code : espaces entres les assignements (=, +=...), les items (,), et les comparateurs (!=, ==...)

#La dernière fonction : à éviter. Utilisez :
#   new = list(old)     -> rapide
#   new = old.copy()    -> générique
#   new = old.deepcopy()-> fera des copies des items internes au lieu de les linker
#selon ce que vous voulez faire, mais pitié pas de [:] même planqué dans une fonction

#Utilisez xrange() au lieu de range() si la liste est statique. Ça passe un itérateur à la structure for au lieu de passer une liste, c'est bien bien bien plus efficace.

#Pas de variable qui sert à rien ("return resultat(bite)", "pas r = resultat(bite) ; return r")

#Ne mélangez pas les fonctions et le display. Tout ce qui doit tourner de manière effective au lancement du script doit être dans "if __name__ == '__main__':", le reste c'est des fonctions. Vous pouvez ainsi concevoir et réutiliser votre code comme un module.