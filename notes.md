## La fonction enumerate()
Elle permet de récupérer une liste de tuples (indice, valeur) en itérant sur l'objet qu'on lui passe.

```python
>>> print(enumerate('Bonsoir', 'Bonjour', 1, 2))
[(0, 'Bonsoir'), (1, 'Bonjour'), (2, 1), (3, 2)]
```

## La fonction list()
C'est le constructeur d'une liste par recopie. En gros :
```python
new_list = list(old_list)
```
est plus ou moins équivalent à
```python
new_list = old_list[:]
```
