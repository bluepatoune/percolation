# percolation.py

Modélise l'écoulement de l'eau dans la roche.

## Format de codage des matrices :
0 modélise la roche 
1 modélise le vide 
-1 modélise le néant
 ```
 [[-1, 1, 1, 0,  0,  1, 1, -1],
 [-1, 1, 1, 0,  0,  1, 1, -1],
 [-1, 1, 1, 0,  0,  1, 1, -1],
 [-1, -1, -1, -1, -1, -1, -1, -1]]
 ```
Le nombre de 1 est déterminé par un indice en argument 

