import sys
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
## Because the animation gets so computationally slow for large grids
from numba import njit

# User defined inputs Code will keep asking until the user is correct.
# Asks what you want l (the length and width) of the Matrix to be
class Questions:
    def get_length(self):
        while True:
            length = int(input("Enter the length of the square grid (between 200 and 250): "))
            if 200 <= length <= 250:
                return length
            else:
                print("Please put a number between 200 and 250")

    def get_shape(self):
        while True:
            choice = input("Now what do you want your initial shape to be, rectangle,ellipse or circle? ")
            if choice in ["rectangle", "ellipse", "circle"]:
                return choice
            else:
                print("Invalid Choice")

    def get_alpha(self):
        while True:
            alpha = float(input("Enter the move probability (between 0 and 1): "))
            if 0 <= alpha <= 1:
                return alpha
            else:
                print("Invalid choice of move probability")

    def get_frames(self):
        while True:
            no_of_frames = int(
                input("How many frames do you want the animation to consider (Recommended between 300 to 600): "))
            if 200 <= no_of_frames <= 700:
                return no_of_frames
            else:
                print("Choose a number between 300 and 600")

## @njit used to compile the code below into Machine code
@njit
# check_energy_conversion_2D is to check so that the 1st law is not broken.
def check_energy_conversion_2D(test_grid, input):
    if np.sum(test_grid[1:-1,1:-1]) == np.sum(input[1:-1,1:-1]):
        return True
    else:
        raise ValueError("Energy within grid not Conserved !")

## Code for a 2D numpy array.
@njit
## This is to apply the big function F(M,\alpha) = M_{k+1} iteration.
def apply_rules_2d(grid,heat_transfer_probability):
    black_cells = np.where(grid[1:-1, 1:-1] == 1)
    for i in range(len(black_cells[0])):
        x, y = black_cells[0][i] + 1, black_cells[1][i] + 1

        if np.random.rand() < heat_transfer_probability:
            direction_vector = np.array([[0, -1],[-1, 0], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]])
            neighbors = np.array(
                [grid[x][y - 1], grid[x - 1][y], grid[x + 1][y], grid[x][y + 1], grid[x - 1][y - 1], grid[x + 1][y - 1],
                 grid[x + 1][y + 1], grid[x - 1][y + 1]])
            if np.all(neighbors == 1) == True:
                pass
            else:
                boolean_dir_index = (neighbors == 0)
                valid_directions = direction_vector[boolean_dir_index]
                valid_directions_flat = valid_directions.reshape(-1, 2)
                possible_directions = valid_directions_flat[np.random.choice(valid_directions_flat.shape[0])]
                grid[x + possible_directions[0]][y + possible_directions[1]] = 1
                grid[x][y] = 0
    return grid

@njit
## This to to compute the entropy
def calculate_xor_sum(grid):
    grid_i_care=grid[1:-1,1:-1]
    flat_grid = grid_i_care.flatten().astype(np.int64)
    xor_result = np.bitwise_xor(flat_grid[:-1], flat_grid[1:])
    xor_value=np.sum(xor_result)
    return xor_value

# This function is to initialise everything
def initialize_grid(length, choice, alpha, no_of_frames):
    length = int(length)
    n=length
    grid = np.pad(np.zeros((n, n)), pad_width=1, mode='constant', constant_values=1)
    if choice == "rectangle":
        grid[100:146, 125:178] = 1
    elif choice == "circle":
        center = ((length/2), (length/2))
        radius = int(math.sqrt(0.04 * length ** 2 / math.pi))
        x, y = np.meshgrid(np.linspace(0, length+2, length+2), np.linspace(0, length+2, length+2))
        distance = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
        grid[distance <= radius] = 1
    elif choice == "ellipse":
        center = (length // 2, length // 2)
        x, y = np.meshgrid(np.linspace(0, length+2, length+2), np.linspace(0, length+2, length+2))
        a = 0.13 * length  # x-radius
        b = 0.09 * length  # y-radius
        ellipse = (x - center[0]) ** 2 / a ** 2 + (y - center[1]) ** 2 / b ** 2
        grid[ellipse <= 1] = 1
    else:
        print("Invalid choice")
        sys.exit()

    test_grid=np.copy(grid)
    return grid, test_grid, float(alpha), int(no_of_frames),n

# Initialise the questions
questions = Questions()
length = questions.get_length()
choice = questions.get_shape()
alpha = questions.get_alpha()
no_of_frames = questions.get_frames()
grid, test_grid, alpha, no_of_frames,n = initialize_grid(length, choice, alpha, no_of_frames)

# Initialise plots
fig, (ax,ax2) = plt.subplots(1,2, figsize=(10,5), width_ratios=[1.8, 1])
im = ax.imshow(grid[1:-1, 1:-1], cmap='inferno', vmin=0, vmax=1)
ax.set_xlabel("Rows")
ax.set_ylabel("Columns")
xor_values = []

def update(frame,grid):
    grid = apply_rules_2d(grid,  alpha)
    im.set_data(grid[1:-1, 1:-1])
    ax.set_title("Generation: {}".format(frame),loc="left")
    ax.set_title("Move probability: {:.0f}%".format(alpha*100),loc="right")
    ## Compute the xor values of the original simulation as a proxy measure of its entropy.
    xor_result = calculate_xor_sum(grid)
    xor_values.append(xor_result)
    ax2.plot(xor_values, color='blue')
    ax2.set_xlabel("Generations")
    ax2.set_ylabel("Proxy entropy measure")
    ax2.set_title("Heated particles: {:.1f}%".format(np.sum(grid[1:-1, 1:-1]) / (n * n) * 100), loc="center")

    if not check_energy_conversion_2D(test_grid, grid) or frame > no_of_frames:
        ani.event_source.stop()
        sys.exit()

ani = animation.FuncAnimation(fig, update, fargs=(grid,), frames=no_of_frames, repeat=False,interval=50)
plt.show()

class DataCollector:
    def __init__(self):
        pass

    def collect_data(self, alphas, n_generations, n_runs):
        results = {'alpha': [], 'xor_result': []}
        for alpha in alphas:
            for i in range(n_runs):
                grid = np.pad(np.zeros((n, n)), pad_width=1, mode='constant', constant_values=1)
                grid[100:146, 125:178] = 1
                for frame in range(n_generations):
                    grid = apply_rules_2d(grid, alpha)
                xor_result = calculate_xor_sum(grid)
                results['alpha'].append(alpha)
                results['xor_result'].append(xor_result)

        df = pd.DataFrame(results)
        return df
