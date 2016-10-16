import random as rd

EAU = 2
VIDE = 1
PIERRE = 0

def matrice(n, p, i):
    """Création d'une matrice modélisant une roche poreuse aléatoire. 0 indique la roche , 1 indique un pore """
    S = zero(n,p)
    S = pores(S,i)
    S = bords(S)
    matshow(S)
    return S
    
def zero(n, p):
    """ crééer un ematrice de zéros de taille n,p """ 
    S = [0]*n
    for i in range(n):
        S[i] = [0]*p
    return S

def pores(S, i):
    """ introduit des pores au hasard  en fonction de l'indice de porosité i """
    for x in range(len(S)):
        for y in range(len(S[0])):
            S[x][y] = bernoulli(i)
    return S
    
def bernoulli (i):
    """ retourne un 1 ou 0 en fonction de la propabilité p."""
    x = rd.random()
    if x < i:
        return 1
    else:
        return 0

def bords(S):
    """ on borde la matrice de -1 """
    for x in range(len(S)):
        S[x].insert(0,-1)
        S[x].append(-1)
    L = [-1]*len(S[0])
    S.append(L)
    return S
