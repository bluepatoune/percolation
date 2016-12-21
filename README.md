# Percolation.py
Modélise l'écoulement de l'eau dans la roche.

## Format de codage des matrices :
Pour une matrice de dimension 2 :
 ```
 [[-1, 1, 1, 0,  0,  1, 1, -1],
 [-1, 1, 1, 0,  0,  1, 1, -1],
 [-1, 1, 1, 0,  0,  1, 1, -1],
 [-1, -1, -1, -1, -1, -1, -1, -1]]
 ```

## Convention de codage
| Valeur | Signification |
| -------| ------------- |
| -1     | Mur           |
| 0      | Roche         |
| 1      | Air           |
| 2      | Eau           |
| 3      | Eau mouvante  |

## Génération
Le taux de roche est modulé par l'**indice de porosité**.
