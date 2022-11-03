"""
burning_coins.py

For a given row of n coins with corresponding values v1, v2, ..., vn, we want to know
what is the largest amount of money we are guaranteed to win if we manage to play optimally, 
assuming we start the game, and independently of the strategy of the opponent.

- n coins
- values v1, v2, ..., vn
- Player 1: us
- Player 2: opponent. We suppose its strategy is to minimize our gain.

We can solve this problem using dynamic programming, so by solving sub-problems. 
"""

import sys


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


if __name__ == "__main__":
    t = int(input())
    f = open(sys.argv[1], "w")
    for _ in range(t):
        n = int(input())
        coins = list(map(int, input().split()))
        f.write(str(largest_amount(n, coins)) + "\n")
    f.close()
