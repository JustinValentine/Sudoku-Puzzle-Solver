import pulp
import matplotlib.pyplot as plt
import numpy as np


def sudoku_solver(grid):
    prob = pulp.LpProblem("SudokuSolver", pulp.LpMinimize)

    # Define the variables: 0-8
    choices = range(9) 
    x = pulp.LpVariable.dicts("Cell", (range(9), range(9), choices), cat=pulp.LpBinary)

    # Objective function 
    prob += 0

    # Single value constraints
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                prob += x[r][c][grid[r][c]-1] == 1
            else:
                prob += pulp.lpSum([x[r][c][v] for v in choices]) == 1

    # Row, column, and 3x3 block constraints
    for v in choices:
        for r in range(9):
            prob += pulp.lpSum([x[r][c][v] for c in range(9)]) == 1

        for c in range(9):
            prob += pulp.lpSum([x[r][c][v] for r in range(9)]) == 1

        for block_r in range(3):
            for block_c in range(3):
                prob += pulp.lpSum([x[r+3*block_r][c+3*block_c][v] for r in range(3) for c in range(3)]) == 1

    # Solve
    prob.solve()

    # Extract solution
    solution = [[0 for _ in range(9)] for _ in range(9)]
    for r in range(9):
        for c in range(9):
            for v in choices:
                if pulp.value(x[r][c][v]) == 1:
                    solution[r][c] = v + 1  # Translate back to 1-9 for Sudoku

    return solution


def display_sudoku(grid, ax, title="Sudoku"):
    ax.set_title(title)
    ax.set_xticks(np.arange(9)+0.5, minor=True)
    ax.set_yticks(np.arange(9)+0.5, minor=True)
    ax.grid(which="minor", color="black", linewidth=2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.5, 9)
    ax.set_ylim(-0.5, 9)
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                ax.text(j, 8-i, str(grid[i][j]), ha='center', va='center', fontsize=12)


# Test
# sudoku = [
#     [4, 8, 1,   3, 0, 0,   0, 6, 0],
#     [0, 6, 0,   0, 7, 0,   0, 2, 0],
#     [0, 0, 9,   6, 4, 8,   0, 0, 5],

#     [0, 0, 3,   7, 0, 0,   0, 5, 0],
#     [7, 0, 0,   4, 0, 3,   0, 0, 8],
#     [0, 1, 0,   0, 0, 5,   3, 0, 0],

#     [1, 0, 0,   5, 6, 9,   2, 0, 0],
#     [0, 3, 0,   0, 2, 0,   0, 4, 0],
#     [0, 2, 0,   0, 0, 4,   9, 8, 6]
# ]

# sudoku = [
#     [9, 0, 4,   0, 6, 0,   0, 0, 2],
#     [0, 0, 8,   5, 7, 1,   0, 0, 0],
#     [5, 0, 0,   0, 0, 4,   1, 3, 0],

#     [0, 0, 2,   0, 0, 8,   0, 0, 1],
#     [8, 0, 0,   1, 3, 7,   0, 0, 6],
#     [3, 0, 0,   4, 0, 0,   8, 0, 0],

#     [0, 2, 6,   3, 0, 0,   0, 0, 4],
#     [0, 0, 0,   6, 4, 2,   7, 0, 0],
#     [4, 0, 0,   0, 1, 0,   6, 0, 3]
# ]

# sudoku = [
#     [8, 0, 0,   9, 4, 3,   7, 0, 0],
#     [6, 0, 0,   0, 0, 2,   0, 1, 0],
#     [0, 0, 7,   0, 6, 0,   0, 0, 8],

#     [0, 0, 6,   3, 0, 4,   0, 7, 9],
#     [9, 0, 3,   0, 0, 0,   6, 0, 4],
#     [4, 2, 0,   7, 0, 6,   3, 0, 0],

#     [2, 0, 0,   0, 3, 0,   4, 0, 0],
#     [0, 3, 0,   4, 0, 0,   0, 0, 2],
#     [0, 0, 4,   2, 5, 9,   0, 0, 1]
# ]

sudoku = [
    [0, 2, 0,   4, 7, 8,   0, 0, 3],
    [0, 0, 1,   0, 0, 0,   8, 6, 0],
    [8, 0, 5,   0, 0, 2,   9, 4, 0],

    [0, 9, 4,   8, 1, 0,   0, 0, 6],
    [0, 0, 0,   0, 0, 0,   0, 0, 0],
    [7, 0, 0,   0, 3, 6,   4, 5, 0],

    [0, 4, 7,   6, 0, 0,   1, 0, 5],
    [0, 5, 9,   0, 0, 0,   6, 0, 0],
    [1, 0, 0,   7, 5, 9,   0, 3, 0]
]


solution = sudoku_solver(sudoku)

# Display
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
display_sudoku(sudoku, axes[0], "Initial Grid")
display_sudoku(solution, axes[1], "Solved Sudoku")
plt.tight_layout()
plt.show()