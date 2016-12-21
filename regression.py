#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Regression.py: Permet des conjectures statistiques sur les percolations."""

from matplotlib    import pyplot
from percolation2d import modelisation as model2d
from percolation3d import modelisation as model3d

def ratio(n, p, N, P):
    """Percolation critique."""
    proba  = []
    indice = []
    for d in range(N+1):
        indice += [d/N]
    for i in indice:
        S = 0
        for e in range(P):
            if model2d(n, p, i):
                S += 1
        proba += [S/P]
    pyplot.plot(indice, proba)
    return indice, proba

# EN FONCTION RAPPORT N/P

if __name__ == '__main__': # Fonction test
    print(ratio(10, 10, 10, 10))
