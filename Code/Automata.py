"""
A cellular automata inspired simulation to demonstrate and visualise what entropy actually is
Author: Bowen Shiro Husin
Date: 28/01/2023
Version = Automata_v1
Note: This file is not meant to be run on its own
"""
import sys
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
## Because the animation gets so computationally slow for large grids
from numba import njit
"""
Within the Object class Questions. The user is asked what the length of the grid should be, 
what the shape choice you want, circle, ellipse or rectangle as the initial shape,
what the move_probability or alpha you want to use, 
and how many frames of animations you want to run. 
Try to choose the recommended shapes or numbers within the prompt
"""
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

# This initialize_grid function is to start the environment for the simulation
def initialize_grid(length, choice, alpha, no_of_frames):
    length = int(length)
    n=length
    grid = np.pad(np.zeros((n, n)), pad_width=1, mode='constant', constant_values=1)
    if choice == "rectangle":
        x,y=int(n/2), int(n/2)
        z=int(0.35*x)
        w=int(0.5*y)
        grid[x : x+z, y : y+w] = 1
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


"""
The functions check_energy_conversion_2D, apply_rules_2d and calculate_xor_sum is to implement, 
the critical functions required for applying the rules, making sure that the 1st law of thermodyanimcs isn't broken, 
and the calculate a proxy measurement of the entropy. 
"""
## @njit used to compile the code below into Machine code
## This code is to enforce the 1st law. If this is broken the animation completely halts
@njit
def check_energy_conversion_2D(test_grid, input):
    if np.sum(test_grid[1:-1,1:-1]) == np.sum(input[1:-1,1:-1]):
        return True
    else:
        raise ValueError("Energy within grid not Conserved !")

@njit
## This is to apply the big function F(M,\alpha) = M_{k+1} iteration.
## This function is conceptually the hardest to make
def apply_rules_2d(grid,heat_transfer_probability):
    black_cells = np.where(grid[1:-1, 1:-1] == 1)     ## Only find tuples where the black cells are
    for i in range(len(black_cells[0])):              ## For every black cell
        x, y = black_cells[0][i] + 1, black_cells[1][i] + 1    ## get the x and y axis or positions

        if np.random.rand() < heat_transfer_probability:
            ## Choose which direction it can go
            direction_vector = np.array([[0, -1],[-1, 0], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]])
            ## Check whats happening on all 8 sides of a 1 cell
            neighbors = np.array(
                [grid[x][y - 1], grid[x - 1][y], grid[x + 1][y], grid[x][y + 1], grid[x - 1][y - 1], grid[x + 1][y - 1],
                 grid[x + 1][y + 1], grid[x - 1][y + 1]])
            ## If all the surroundings of a 1 cell is occupied, do nothing
            if np.all(neighbors == 1) == True:
                pass
            ## Else select only the lists within direction_vector_array that matches with the truth values of neighbors
            ## If neighbors==0 select True and randomly select what is available within direction_vector
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
    ## do a XOR operation of the flattened grid and move 1 unit at a time and output the values until the end
    xor_result = np.bitwise_xor(flat_grid[:-1], flat_grid[1:])
    xor_value=np.sum(xor_result)
    return xor_value

"""
The class AutomataSimulation is to house an object class where the simulation is held. 
It requires the output from initialize_grid function to run properly 
"""
class AutomataSimulation:
    def __init__(self, grid, alpha, no_of_frames,length):
        ## Declare all the attributes associated within the class AutomataSimulation
        self.n=length
        self.grid = grid
        self.alpha = alpha
        self.no_of_frames = no_of_frames
        self.test_grid = np.copy(self.grid)
        self.fig, (self.ax,self.ax2) = plt.subplots(1,2, figsize=(10,5), width_ratios=[1.8, 1])
        self.im = self.ax.imshow(grid[1:-1, 1:-1], cmap='inferno', vmin=0, vmax=1)
        self.ax.set_xlabel("Rows")
        self.ax.set_ylabel("Columns")
        self.xor_values = []
        self.ani = animation.FuncAnimation(self.fig, self.update, frames=self.no_of_frames, repeat=False, interval=50)
        plt.show()
     
    ## Saves the animation into an appropriate name
    def save_animation(self, filename):
        self.ani.save(filename, writer="pillow")

    ## This function is to run the frames and is for the animation module in matplotlib
    def update(self, frame):
        grid = apply_rules_2d(self.grid,  self.alpha)
        self.im.set_data(grid[1:-1, 1:-1])
        self.ax.set_title("Generation: {}".format(frame),loc="left")
        self.ax.set_title("Move probability: {:.0f}%".format(self.alpha*100),loc="right")
        xor_result = calculate_xor_sum(grid)
        self.xor_values.append(xor_result)
        self.ax2.plot(self.xor_values, color='blue')
        self.ax2.set_xlabel("Generations")
        self.ax2.set_ylabel("Proxy entropy measure")
        self.ax2.set_title("Heated particles: {:.1f}%".format(np.sum(grid[1:-1, 1:-1]) / (self.n * self.n) * 100), loc="center")

        if not check_energy_conversion_2D(self.test_grid, grid) or frame > self.no_of_frames:
            self.ani.event_source.stop()
            sys.exit()


"""
The final class of DataCollector is just a means to collect some data from a simulation run and plot it. 
It has its own defined parameters and collect_data is just a function to compute the datapoints. 
"""
class DataCollector:
    def __init__(self):
        pass

    def collect_data(self, alphas, n_generations, n_runs,length=250):
        n=length
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
