"""
A cellular automata inspired simulation to demonstrate and visualise what entropy actually is. Simplified compared to previous versions
Author: Bowen Shiro Husin
Date:30/08/2023 
Version = Automata_v3
Note: This file is not meant to be run on its own
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from matplotlib.widgets import Button
from scipy import signal
from copy import deepcopy
import itertools
from numba import njit
from PIL import Image
import cv2
from skimage.transform import resize
from tqdm import trange

class image_processor:
    def __init__(self):
        pass

    def image_selector(self,image_paths, max_size, plot, max_grid_int ,random ):

        if (random==True) and ( type(random)==type(True) ):
            image_index=np.random.randint(0, len(image_paths))
            image_choice=image_paths[image_index]
        else:
            image_choice=image_paths[random]

        img=np.asarray(Image.open(image_choice))

        color_channel_index=np.random.randint(0, high=3)
        image_data=img[:, :, color_channel_index]
        # Resize the image

        if max_size>300:
            raise Exception("Put a size lower than 300")

        else:
            ratio= image_data.shape[1]/image_data.shape[0]
            y_size= int(max_size*ratio)

            ### Make max_size and y_size to be even numbers
            if max_size % 2 != 0:
                max_sized=max_size-1
            else:
                max_sized=max_size

            if y_size % 2 !=0:
                y_sized=y_size-1
            else:
                y_sized=y_size

            resized_image_data = resize(image_data, (max_sized, y_sized), order=1, preserve_range=True).astype(np.uint8)
            equalized_image_data = cv2.equalizeHist(resized_image_data)

            constant= np.max(equalized_image_data)/max_grid_int
            reduced_range_image=(equalized_image_data / constant).astype(int)

            if plot:
                plt.style.use('dark_background')
                fig, ax = plt.subplots(1, 1, figsize=(8,6))
                im = ax.imshow(reduced_range_image, cmap="plasma",vmin=0, vmax=max_grid_int)
                fig.colorbar(im, ax=ax, label= "Energy level", shrink=0.55)
                plt.title("Processed image for entropy")
                plt.show()

            else:
                image_grid=np.pad(reduced_range_image, pad_width=1, mode="constant",constant_values=np.max(reduced_range_image))
                return image_grid
"""
These 2 classes are designed to resize an ImageMobject into the Manim environment later. 
This would not work if the Collect class has not been triggered
"""
class ImageResize:
    def __init__(self):
        self.grid_data = np.load(r'C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\grids.npy')
        self.prime_data = np.load(r'C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\prime_grids.npy')
        self.loaded_entropies = np.load(r'C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\entropies.npy')
        self.microstate_data = pd.read_csv(
            r"C:\Users\Bowen\PycharmProjects\Entropy_Game\Code\Manim\Data\Microstate_dataframe.csv")

        ## Get some class attibutes where the later Manim Scene can see
        self.Grid_copies = self.grid_data.shape[0]

    def get_rgb_values(self):
        RGB=np.array([self.convert_to_rgb_image(self.grid_data[i, :, :],
                    cmap=plt.get_cmap("plasma")) for i in range(self.Grid_copies)])
        return RGB

    def convert_to_rgb_image(self, grid_data, cmap="plasma", vmin=0, vmax=16):
        self.cmap = matplotlib.colormaps.get_cmap(cmap)
        self.norm = plt.Normalize(vmin, vmax)
        self.grid_data_rgb = self.cmap(self.norm(grid_data))
        return (self.grid_data_rgb[:, :, :3] * 255).astype(np.uint8)

    def image_resize(self, length=40, height=70):
        Im = self.get_rgb_values()  # shape: (401, 300, 532, 3)
        resized_grids = []
        for j in range(Im.shape[0]):
            smaller_image = resize(Im[j, :, :, :], (length, height), order=1, preserve_range=True).astype(np.uint8)
            resized_grids.append(deepcopy(smaller_image))

        return np.array(resized_grids)

    def check_image_and_plot(self , check : bool, save : bool):
        Smaller_images=self.image_resize()
        if check==True and save==False:
            print(f"The size is {Smaller_images.shape}")

        if check==True and save==True:
            np.save("smaller_images", Smaller_images)

## Run the resize script
CHECK=ImageResize()
sizes=CHECK.check_image_and_plot(False, False)

"""
End of the 2 classes
"""

class Microstate_table:
    def get_table(self, max_val):
        result = []
        for E in range(max_val*4+1):
            for a, b, c, d in itertools.product(range(max_val+1), repeat=4):
                if a + b + c + d == E:
                    result.append([E, a, b, c, d])
        df = pd.DataFrame(result, columns=["E", "a", "b", "c", "d"])
        df_grouped = df.groupby("E")[["a"]].count().reset_index()
        df_grouped.rename(columns={"a": "Microstates"}, inplace=True)
        data = df_grouped.to_dict(orient="records")
        entropy_list=[]
        for i in range(len(data)):
          element=data[i]["Microstates"]
          entropy_list.append(element)
        entropies=np.array(entropy_list)

        return entropies


"""
The functions check_energy_conversion_2D, apply_rules_2d and calculate_xor_sum is to implement, 
the critical functions required for applying the rules, making sure that the 1st law of thermodynamics isn't broken, 
and the calculate a proxy measurement of the entropy. 
"""

@njit
def energy_conservation_2d(test_grid, input):
    if np.sum(test_grid[1:-1, 1:-1]) == np.sum(input[1:-1, 1:-1]):
        return True
    else:
        raise ValueError("The simulation broke the first law of thermodynamics !")

## This is to apply the big function F(M,\alpha) = M_{k+1} iteration.
## This function is conceptually the hardest to make
@njit
def apply_rules_2d(grid, heat_transfer_probability, temperature):
    max_val = np.max(grid[1:-1, 1:-1])
    non_zero_cells = np.where(grid[1:-1, 1:-1] >= 1)  ## Only find tuples where the non_zero_cells are
    # Random assortment of non_zero_cells locations while maintaining correspondance between rows and columns
    indices = np.arange(len(non_zero_cells[0]))
    np.random.shuffle(indices)
    non_zero_cells = (non_zero_cells[0][indices], non_zero_cells[1][indices])
    direction_vector = np.array([[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]])

    for i in range(len(non_zero_cells[0])):  ## For every non-zero cell
        row, col = non_zero_cells[0][i] + 1, non_zero_cells[1][i] + 1  ## get the x and y axis or positions

        if np.random.rand() < heat_transfer_probability:
            ## Choose which direction it can go
            ## Check whats happening on all 8 sides of a non-zero cell
            neighbors = np.array(
                [grid[(row - 1), (col - 1)], grid[(row), (col - 1)], grid[(row + 1), (col - 1)],
                 grid[(row + 1), (col)],
                 grid[(row + 1), (col + 1)],
                 grid[(row), (col + 1)],
                 grid[(row - 1), (col + 1)], grid[(row - 1), (col)]])

            difference = np.array([max_val - grid[(row - 1), (col - 1)],
                                   max_val - grid[(row), (col - 1)],
                                   max_val - grid[(row + 1), (col - 1)],
                                   max_val - grid[(row + 1), (col)],
                                   max_val - grid[(row + 1), (col + 1)],
                                   max_val - grid[(row), (col + 1)],
                                   max_val - grid[(row - 1), (col + 1)],
                                   max_val - grid[(row - 1), (col)]
                                   ])
            ## If all the surroundings of a 8 cell is occupied, do nothing
            if np.all(neighbors == max_val) == True:
                pass
            ## Else select only the lists within direction_vector_array that matches with the truth values of neighbors
            ## If neighbors==0 select True and randomly select what is available within direction_vector
            else:
                boolean_dir_index = (neighbors <= max_val - 1)
                valid_directions = direction_vector[boolean_dir_index]
                delta_E = difference[boolean_dir_index]
                ### Applying the boltzmann factor to modify probabilities based on energy difference to a 8.
                energy_diff = np.abs(delta_E)
                boltzmann_factors = np.exp(energy_diff * (1 / temperature))
                partition_function = np.sum(boltzmann_factors)
                direction_probabilities = boltzmann_factors / partition_function
                cumsum_probs = np.cumsum(direction_probabilities)
                sampling = np.random.rand()
                dir_indexing = np.searchsorted(cumsum_probs, sampling)
                possible_directions = valid_directions[dir_indexing]
                grid[(row + possible_directions[0], col + possible_directions[1])] += 1
                grid[row, col] -= 1
    return grid

# This code is to compute the entropy for version 2 of Automata
def calculate_entropy(grid, microstates_dict, extend = False):

    # The code slices the grid into 2x2 matrices. For example, if length=10. There should be 25 2x2 matrices.
    # Works as long as the length and width of the grid are even numbers
    subsize=(2,2)
    shape = grid[1:-1, 1:-1].shape[0] // subsize[0], grid[1:-1, 1:-1].shape[1] // subsize[1], subsize[0], subsize[1]
    strides = grid[1:-1, 1:-1].strides[0] * subsize[0], grid[1:-1, 1:-1].strides[1] * subsize[1], \
              grid[1:-1, 1:-1].strides[0], grid[1:-1, 1:-1].strides[1]
    sliced_grid = np.lib.stride_tricks.as_strided(grid[1:-1, 1:-1], shape=shape, strides=strides)

    ## This line will find for each subgrid what is its energy level
    sub_energy = np.sum(sliced_grid, axis=(2, 3))
    microstates = microstates_dict[sub_energy]
    no_of_microstates = np.array(microstates)
    entropy_per_subgrid=np.log(no_of_microstates)
    entropy = np.sum(entropy_per_subgrid)
    if extend:
        return entropy, no_of_microstates
    else:
        return entropy

def grid_conversion(grid):
    array=(grid[1:-1, 1:-1] % 2 ==0 ) | (grid[1:-1, 1:-1] % 3 == 0) | (grid[1:-1, 1:-1] % 5 ==0)
    return array

def game_of_life(array):
    neighbor_vector=np.array([[1, 1, 1],
                              [1, 0, 1],
                              [1, 1, 1]], dtype=np.uint8)

    num_neighbors = signal.convolve2d(array, neighbor_vector,
                                      mode='same', boundary='wrap')

    next_state = np.logical_or(num_neighbors == 3,
                               np.logical_and(num_neighbors == 2,
                                              array)
                               ).astype(np.uint8)
    array = next_state
    return array

class Automata_Simulation:
    def __init__(self, controllable, image_paths, max_size, plot, max_grid_int ,random ,temperature, move_probability):
        if controllable:
            self.controllable=True
        else:
            self.controllable=False
        self.frame_tracker=0
        self.is_running=False
        self.GRID = image_processor()
        self.show_image=plot

        ###
        self.alpha = move_probability
        self.temperature = temperature

        if self.show_image:
            self.GRID.image_selector(image_paths, max_size, plot, max_grid_int ,random)
        elif self.show_image == False:
            self.grid= self.GRID.image_selector(image_paths, max_size, plot, max_grid_int ,random)
        elif self.show_image == None:
            arr = np.zeros((200, 300))
            arr[:, 0:150] = 1
            arr[:, 150:300] = 16
            arr = np.pad(arr, pad_width=1, mode='constant', constant_values=np.max(arr)).astype(int)
            self.grid = arr

    def run_simulation(self,no_of_frames, microstate_dict, show_primes, save=False):
        self.intial_grid=np.copy(self.grid)
        self.no_of_frames=no_of_frames
        self.microstate_dictionary=microstate_dict
        self.primes=show_primes
        self.max_val=np.max(self.grid[1:-1 , 1:-1])

        # plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(10, 5))
        plt.subplots_adjust(top=0.95, wspace=0.4)

        if show_primes:
            self.gs = GridSpec(1, 2 , width_ratios=[1.2, 0.98])
        else:
            self.gs = GridSpec(1, 2,  width_ratios=[1.5, 0.98])
        self.ax = plt.subplot(self.gs[0, 0])
        self.ax2 = plt.subplot(self.gs[0, 1])

        self.im = self.ax.imshow(self.grid[1:-1, 1:-1], cmap='plasma', vmin=0, vmax=self.max_val)
        self.ax.axis("off")
        if show_primes:
            self.im2= self.ax2.imshow( grid_conversion(self.grid), cmap="binary", vmin=0, vmax=1)
            self.ax2.axis("off")

        self.fig.colorbar(self.im, ax=self.ax, label='Energy level', shrink=0.55, location="bottom",  pad=0.08)
        self.entropies=[]

        if save==False and self.controllable==True:
            plt.subplots_adjust(top=0.95, wspace=0.2)
            # Add the sliders for conductivity and temperature
            self.prob_slider_ax = self.fig.add_axes([0.1, 0.05, 0.5, 0.04])
            self.prob_slider = Slider(self.prob_slider_ax, 'Probability', 0.0, 1.0,
                                              valinit=self.alpha)
            self.prob_slider.on_changed(self.update_moveprob)

            self.temperature_slider_ax = self.fig.add_axes([0.1, 0.0, 0.5, 0.04])
            self.temperature_slider = Slider(self.temperature_slider_ax, 'Temperature', 0.0, 7.0,
                                             valinit=self.temperature)
            self.temperature_slider.on_changed(self.update_temperature)

            ## Add a pause button
            self.pause_button = Button(plt.axes([0.04, 0.92, 0.06, 0.07]), 'Pause', color='black')
            self.pause_button.on_clicked(self.on_pause_clicked)
            self.ani = FuncAnimation(self.fig, self.update, frames=self.no_of_frames, repeat=False,
                                               interval = 60)
            plt.show()

        elif save==False and self.controllable==False:

           self.ani = FuncAnimation(self.fig, self.update, frames=self.no_of_frames, repeat=False,
                                              interval = 60)
           plt.show()

        else:
            self.ani=FuncAnimation(self.fig, self.update, frames=self.no_of_frames, repeat=False,
                                              interval = 60)
            self.ani.save("cellular_animation.gif", writer="pillow")

    def on_pause_clicked(self, *args, **kwargs):
        if self.is_running:
            self.ani.resume()
            self.pause_button.label.set_text('Pause')
        else:
            self.ani.pause()
            self.pause_button.label.set_text('Resume')
        self.is_running = not self.is_running

    def update_moveprob(self, value):
        self.alpha = float(value)
        self.ax2.set_title("Probability: {:.1f} W/m.K".format(self.alpha), loc="center")

    def update_temperature(self, value):
        self.temperature = float(value)
        self.ax.set_title("T: {:.0f}".format(self.temperature), loc="left")

    def update(self, frame):
        self.grid = apply_rules_2d(self.grid, self.alpha, self.temperature)
        self.im.set_data(self.grid[1:-1, 1:-1])
        self.ax.set_title(r"$\beta$: {:.1f} ".format(self.temperature), loc="left")
        self.ax.set_title(r"$\alpha$: {:.1f} ".format(self.alpha), loc="right")
        self.ax.set_title("Automata grid", loc="center")

        ## Entropy plot
        if self.primes==False:
            entropy = calculate_entropy(self.grid, self.microstate_dictionary) / 10000
            self.entropies.append(entropy)
            self.ax2.plot(self.entropies, color='blue')
            self.ax2.set_xlabel("Epoch")
            self.ax2.set_ylabel("Entropy $S.10^{{4}}/k_b$")

        # Number detection
        elif self.primes==True:
            array=grid_conversion(self.grid)
            self.im2.set_data(array)
            self.ax2.set_title("Non prime number locations")

        if not energy_conservation_2d(self.intial_grid, self.grid) or frame>self.no_of_frames:
            self.ani.event_source.stop()
            sys.exit()


"""
Additional functions for data analysis and plotting as required
The final class of DataCollector is just a means to collect data for a 3D/2D plots from the simulation run and plot it. 
It has its own defined parameters and collect_data is just a function to compute the datapoints. 
You need to specify the conductivity range, number of iterations (frames), temperature range and number of points for 
the conductivity and temperature range. 
After that's done you can call the method plot_entropy to see the nice 3D plot that is produced. 
WARNING: THIS SCRIPT WILL KILL YOUR CPU IF ITS A POTATO CPU or take 1 day to run. 
"""

class collect(Automata_Simulation):

    def collect_data(self, microstates_df, frames, collect=True):
        array_config = []
        prime_config = []
        entropy_data = []
        state_density = []
        grid = np.copy(self.grid)
        self.frames_to_render = frames
        if collect == True:
            for k in (t:=trange(self.frames_to_render)):
                new_grid = apply_rules_2d(grid, self.alpha, self.temperature)
                entropy_x, density_of_states = calculate_entropy(new_grid, microstates_df, extend=True)
                entropy_x = entropy_x / 1000                             # --> Divide this by 1000 to get reasonable values
                if (k%4==0) or (k==self.frames_to_render-1):
                    array_config.append(deepcopy(new_grid[1:-1, 1:-1]))
                    entropy_data.append(entropy_x)
                    state_density.append(density_of_states)

                grid = new_grid
                t.set_description(f"Progress: ")

        return array_config, prime_config, entropy_data, state_density




