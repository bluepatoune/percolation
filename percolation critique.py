def percolation_critique(n, p, N, P):
    proba = []
    indice = []
    for d in range(N+1):
        indice += [d/N]
    for i in indice:
        S = 0
        for e in range(P):
            if modelisation(n, p, i):
                S += 1
        proba += [S/P]
    pyplot.plot(indice, proba)
    return indice, proba
# EN FONCTION RAPPORT N/P