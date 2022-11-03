# Burning coins

Elise Chin - 28/10/22

Usage :

```bash
python burning_coins.py result.out < test.out
```

## Proposition de solution

On remarque que pour résoudre ce problème, on peut le découper en sous-problèmes plus simple à résoudre. D'où l'idée d'appliquer la programmation dynamique. 

### Programmation dynamique

```Python
# Iterative version, bottom-up approach
def largest_amount(n: int, coins: list[int]) -> int:
    # For n <= 2
    if n == 1:
        return coins[0]
    if n == 2:
        return max(coins)

    # Initialization of memo table with base case (for n > 2)
    memo = [[0] * n for _ in range(n)]
    if n % 2 == 1:
        for i in range(n):
            memo[i][i] = coins[i]

    # Fill the table
    # Start with the smallest problem (from bottom to the top in the table)
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if (n - j + i - 1) % 2 == 0:  # Player 1
                memo[i][j] = max(coins[i] + memo[i + 1][j], coins[j] + memo[i][j - 1])
            else:  # Player 2
                memo[i][j] = min(memo[i + 1][j], memo[i][j - 1])

    return memo[0][n - 1]
```


1. Cas simples : c'est lorsqu'on a qu'une seule pièce, donc `n = 1`. Ici, je traite les cas `n <= 2` à part. Pour `n > 2`, il faudra différencier le cas où c'est le premier joueur (nous) qui prenons la pièce, ou bien le second joueur (ami). Si c'est le premier joueur, on initialise alors la diagonale de la table à la valeur de la pièce correspondante.
2. Table : on crée une table 2D `memo` où `memo[i][j]` correspond à la plus grande somme garantie pour le joueur 1 pour les pièces allant de `i` à `j` (`0 <= i <= j < n`). On calcule ses valeurs en partant du problème le plus simple jusqu'au problème initial.
3. Formule de récursion : elle dépend du tour du joueur.
    - Joueur 1 va prendre la pièce qui va maximiser son gain. C'est donc un max entre ses deux choix : soit prendre la pièce à gauche, ou bien celle à droite plus le gain après le choix du joueur 2. Cela se traduit par `max(coins[i] + memo[i + 1][j], coins[j] + memo[i][j - 1])`.
    - Nous n'avons pas de supposition concernant la stratégie du joueur 2, donc on va supposer qu'il cherche à minimiser le gain du joueur 1. C'est donc un min du prochain choix du joueur 1, ce qui se traduit par `min(memo[i + 1][j], memo[i][j - 1])`. On n'ajoute pas `coins[]` puisqu'on ne souhaite pas compter le gain du joueur 2.

J'avais tout d'abord fait une version récursive, mais elle ne fonctionnait pas pour `n > 2500`, à cause d'un stackoverflow.

```Python
# Recursive version, doesn't work for n > 2500
def largest_amount(l, r, coins, memo):
    if l == r:  # One coin left
        return coins[l]
    if l == r - 1:  # Two coin left
        return max(coins[l], coins[r])
    if memo[l][r]:
        return memo[l][r]

    # -- Strategy of player 2 --
    # If player 1 chooses the left coin
    l_l = largest_amount(l + 2, r, coins, memo)  # player 2 chooses the next left coin
    l_r = largest_amount(l + 1, r - 1, coins, memo)  # player 2 chooses the right coin
    player2_min_left = min(l_l, l_r)

    # If player 1 chooses the right coin
    r_l = largest_amount(l + 1, r - 1, coins, memo)  # player 2 chooses the left coin
    r_r = largest_amount(l, r - 2, coins, memo)  # player 2 chooses the next right coin
    player2_min_right = min(r_l, r_r)

    # -- Strategy of player 1 --
    memo[l][r] = max(coins[l] + player2_min_left, coins[r] + player2_min_right)
    return memo[l][r]
```
J'avais écrit toutes les possibilités du joueur 2, ce qui m'a aidé pour la version itérative.


### Analyse de la complexité

__Complexité en temps__

Dépend du nombre de calculs à effectuer (S) et du nombre moyen de calculs pour obtenir la valeur d'un calcul (T).

- S = (n(n+1))/2 = O(n²), qui correspond à la moitié des valeurs de `memo`  qui est de taille n x n
- T = 2

=> Complexité en temps : O(n² * 2) = O(n²)

__Complexité en espace__

C'est le nombre de valeurs à stocker dans la table, donc S.

=> Complexité en espace : O(n²)


## Cheminement vers la solution
La première étape est de trouver un algorithme correct avant de l'optimiser.

- 1ère idée : prendre le max parmi les deux pièces. Faux, contre-exemple avec 1 4 9 4 où il faut prendre 1 puis 9.
- 2ème idée : un algorithme de min max, mais ça me semble bien compliqué. En tout cas l'idée du min max, bonne à prendre, car on souhaite avoir le montant maximum, indépendamment de la stratégie de l'autre joueur. On peut donc supposer que l'autre joueur va essayer de minimiser notre gain.
- 3ème idée : me fait penser à de la programmation dynamique, résoudre un gros problème en résolvant des sous problèmes ! Donc il faut trouver la formule de récursion et taille du tableau.

