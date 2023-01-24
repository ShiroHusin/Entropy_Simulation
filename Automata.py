import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numba import njit                        ## Because the animation gets so computationally slow for large grids

@njit
def check_energy_conversion_2D(test_grid, input):
    if np.sum(test_grid[1:-1,1:-1]) == np.sum(input[1:-1,1:-1]):
        return True
    else:
        raise ValueError("Energy within grid not Conserved !")

## Code for a 2D numpy array.
@njit
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
def calculate_xor_sum(grid):
    grid_i_care=grid[1:-1,1:-1]
    flat_grid = grid_i_care.flatten().astype(np.int64)
    xor_result = np.bitwise_xor(flat_grid[:-1], flat_grid[1:])
    xor_value=np.sum(xor_result)
    return xor_value

## Initialise matplotlib conditions
n = 250
grid = np.pad(np.zeros((n, n)), pad_width=1, mode='constant', constant_values=1)
grid[100:146,125:178]=1
test_grid=np.copy(grid)
fig, (ax,ax2) = plt.subplots(1,2, figsize=(10,5), width_ratios=[1.8, 1])


im = ax.imshow(grid[1:-1, 1:-1], cmap='inferno', vmin=0, vmax=1)

ax.set_xlabel("Rows")
ax.set_ylabel("Columns")
alpha=1
no_of_frames=600

# Initialize an empty list to store the values of np.sum(xor_result)
xor_values = []

def update(frame,grid):
    grid = apply_rules_2d(grid, alpha)
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


ani = animation.FuncAnimation(fig, update, fargs=(grid,), frames=no_of_frames, repeat=False,interval=100)
plt.show()

## ani.save("Entropy.gif")  # If you want to save the file you can uncomment this line.  

