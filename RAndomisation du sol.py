import random as rd

def matrice(n,p,i):
    """Création d'une matrice modélisant une roche poreuse aléatoire. 0 indique la roche , 1 indique un pore """
    S=zero(n,p)
    S=pores(S,i)
    S=bords(S)
    matshow(S)
    return S
    
def zero(n,p):
    """ crééer un ematrice de zéros de taille n,p """ 
    S=[0]*n
    for e in range(n):
        S[e]=[0]*p
    return S

def pores(S,i):
    """ introduit des pores au hasard  en fobnction de l'indice de porosité i """
    for x in range(len(S)):
        for y in range(len(S[0])):
            
            S[x][y]=rd.choice([0,0,1,1,1])
    return S
    
def liste (i):
    """ retourne une liste de 0 et de 1'en fonction de l'indice de porosité compris entre """
    

def bords(S):
    """ on borde la matrice de -1 """
    for x in range(len(S)):
        S[x].insert(0,-1)
        S[x].append(-1)
    L=[-1]*len(S[0])
    S.append(L)
    return S