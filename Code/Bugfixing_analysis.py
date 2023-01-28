"""
This code is to run and test apply_rules_2d its just a copy paste of some old code and the apply_rules_2d function from Automata.py
This is because I realize that it tends to choose the up direction [0, -1] slightly more often and I'm not sure why.
"""

import numpy as np
import random
import matplotlib.pyplot as plt

def apply_rules_1D(grid):
    dx = [1, 0, -1]
    a = np.copy(grid)
    one_index = np.where(a == 1)
    for i in one_index[0]:
        if i > 0 and i < len(a) - 1:
            neighbors = [a[i - 1], a[i + 1]]
            if neighbors[0] == 0 and neighbors[1] == 0:
                possible_directions = random.choice(dx)
                if possible_directions != 0:
                    a[i + possible_directions] = 1
                    a[i] = 0
                else:
                    pass

            elif neighbors[0] == 1 and neighbors[1] == 0:
                possible_directions = random.choice(dx[:2])
                if possible_directions != 0:
                    a[i + possible_directions] = 1
                    a[i] = 0
                else:
                    pass

            elif neighbors[0] == 0 and neighbors[1] == 1:
                possible_directions = random.choice(dx[1:])
                if possible_directions != 0:
                    a[i + possible_directions] = 1
                    a[i] = 0
                else:
                    pass

            elif neighbors[0] == 1 and neighbors[1] == 1:
                possible_directions = dx[1]
                a[i] = a[i]
    return (a)

## Checking for bias in np.random.choice function
str_to_choose=np.array(["A","B","C","D","E","F","G","H"])

def apply_rules_2d(grid,heat_transfer_probability):
    direction_list=[]
    black_cells = np.where(grid[1:-1, 1:-1] == 1)
    for i in range(len(black_cells[0])):
        x, y = black_cells[0][i] + 1, black_cells[1][i] + 1

        if np.random.rand() < heat_transfer_probability:
            direction_vector = np.array([[0, -1],[-1, 0], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]])
            associated_direction_vector_str=np.array(["T","L","R","B","TL","TR","BR","BL"])
            neighbors = np.array(
                [grid[x][y - 1], grid[x - 1][y], grid[x + 1][y], grid[x][y + 1], grid[x - 1][y - 1], grid[x + 1][y - 1],
                 grid[x + 1][y + 1], grid[x - 1][y + 1]])
            if np.all(neighbors == 1) == True:
                pass
            else:
                boolean_dir_index = (neighbors == 0)
                valid_directions = direction_vector[boolean_dir_index]
                str_directions=associated_direction_vector_str[boolean_dir_index]
                valid_directions_flat = valid_directions.reshape(-1, 2)
                possible_directions = valid_directions_flat[np.random.choice(valid_directions_flat.shape[0])]
                str_choice=np.random.choice(str_directions)
                direction_list.append(str_choice)
                grid[x + possible_directions[0]][y + possible_directions[1]] = 1
                grid[x][y] = 0
    return grid,direction_list

# Initialise matplotlib conditions
n = 100
grid = np.pad(np.zeros((n, n)), pad_width=1, mode='constant', constant_values=1)
grid[10:25,15:31]=1

test_grid=np.copy(grid)
i=1
direction_string=[]
while i<1001:
    grid,list=apply_rules_2d(grid,1)
    direction_string.append(list)
    i=i+1
direction_string=np.concatenate(direction_string)
unique, counts = np.unique(direction_string, return_counts=True)

plt.hist(direction_string, bins=len(unique), density=True, color='blue', alpha=0.5)
plt.xlabel("Strings")
plt.ylabel("Frequency")
plt.title("Frequency of Strings")
plt.show()

