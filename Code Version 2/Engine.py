"""
A cellular automata inspired simulation to demonstrate and visualise what entropy actually is
Author: Bowen Shiro Husin
Date:22/02/2023
Version = Automata_v2
Note: This file is not meant to be run on its own
"""
import sys
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.widgets import Slider
from matplotlib.widgets import Button as button
import matplotlib.animation as animation
import itertools
## Because the animation gets so computationally slow for large grids
from numba import njit
from tkinter import *
"""
Within the Object class GUI The user is asked what the length of the grid should be, 
what the shape choice you want, circle, ellipse or rectangle as the initial shape,
what the conductivity or alpha you want to use, 
and how many frames of animations you want to run. This replaces the old method of asking user inputs.
"""
## Incomplete at the moment.
class GUI():
    def __init__(self):
        ## Declare lots of things
        self.Window=Tk()
        self.Window.title("Initial Conditions")
        self.Window.geometry("700x500")
        self.font = "Consolas"
        self.is_clicked=0
        ## Placeholder values for all the scale widgets
        self.length_val=100
        self.frame_val=200
        self.conduct_val=300
        self.temp_val=1
        self.choice_val=""
        """
        Initialize all the widgets 
        """

        ## Length widget (non-movable)
        self.Length_scale = Scale(self.Window, from_=80, to=300, length=500, orient=HORIZONTAL, font=("font", 10),
                             tickinterval=20, showvalue=True)
        self.Length_scale.grid(row=0, column=1)
        self.Length_label = Label(self.Window, text="Grid size: ", font=("font", 10, "bold"))
        self.Length_label.grid(row=0, column=0)

        ## Iterations widgets (non-movable)
        self.frame_scale = Scale(self.Window, from_=50, to=1000, length=500, orient=HORIZONTAL, font=("font", 10),
                            tickinterval=95, showvalue=True)
        self.frame_scale.grid(row=1, column=1)
        self.frame_label = Label(self.Window, text="Iterations: ", font=("font", 10, "bold"))
        self.frame_label.grid(row=1, column=0)

        ## Conductivity widget (movable)
        self.Conductivity_scale = Scale(self.Window, from_=0, to=3000, length=500, orient=HORIZONTAL, font=("font", 10),
                                   tickinterval=600, showvalue=True)
        self.Conductivity_scale.grid(row=2, column=1)
        self.Conductivity_label = Label(self.Window, text="Conductivity: ", font=("font", 10, "bold"))
        self.Conductivity_label.grid(row=2, column=0)

        ## Temperature widget (movable)
        self.Temp_scale = Scale(self.Window, from_=0, to=7, length=500, orient=HORIZONTAL, font=("font", 10), tickinterval=1,
                           showvalue=True)
        self.Temp_scale.grid(row=3, column=1)
        self.Temp_label = Label(self.Window, text="Temperature: ", font=("font", 10, "bold"))
        self.Temp_label.grid(row=3, column=0)

        ## Choice widget
        self.Choice = Scale(self.Window, from_=1, to=3, length=500, orient=HORIZONTAL, font=("font", 10), tickinterval=1,
                       showvalue=False)
        self.Choice.grid(row=4, column=1)
        self.Choice_label = Label(self.Window, text="Grid config: ", font=("font", 10, "bold"))
        self.Choice_label.grid(row=4, column=0)

        # Create a canvas below the scale
        self.canvas = Canvas(self.Window, width=500, height=20)
        self.canvas.grid(row=5, column=1)
        # Add the text labels to the canvas
        self.canvas.create_text(20, 10, text="Circle", font=("font", 10))
        self.canvas.create_text(250, 10, text="Ellipse", font=("font", 10))
        self.canvas.create_text(470, 10, text="Rectangle", font=("font", 10))

        ## Start button
        self.start_status = BooleanVar(value=False)
        self.start = Button(self.Window, text="Start Simulation", font=("font", 12),command=self.toggle_button)
        self.start.grid(row=7, column=1)
        self.start.config(bg="SystemButtonFace")
        self.start.bind("<Button-1>", lambda event: self.start.config(bg="SystemHighlight"))
        self.start.bind("<ButtonRelease-1>", lambda event: self.start.config(bg="SystemButtonFace"))

        ## Terminate button
        self.stop = Button(self.Window, text="Terminate", font=("font", 12), command=self.stop_button)
        self.stop.grid(row=8, column=1, pady=20)
        self.stop.config(bg="SystemButtonFace")
        self.stop.bind("<Button-1>", lambda event: self.stop.config(bg="SystemHighlight"))
        self.stop.bind("<ButtonRelease-1>", lambda event: self.stop.config(bg="SystemButtonFace"))

        self.animation = AutomataSimulation()
        self.animation.is_running = True

        ## Save button for gifs
        self.save = Button(self.Window, text="Save", font=("font", 10), command=self.save_button)
        self.save.grid(row=8, column=0, padx=20)
        self.save.config(bg="SystemButtonFace")
        self.save.bind("<Button-1>", lambda event: self.stop.config(bg="SystemHighlight"))
        self.save.bind("<ButtonRelease-1>", lambda event: self.stop.config(bg="SystemButtonFace"))

        self.Window.mainloop()

    # Start Button
    def toggle_button(self):
        if self.start.config('relief')[-1] == 'sunken':
            self.start.config(relief="raised", bg="SystemButtonFace")
            self.start_status.set(False)
        else:
            self.is_clicked+=1
            self.start.config(relief="sunken", bg="SystemHighlight")
            # Initialize the grid using the values here.
            if self.is_clicked==1:
                self.start_status.set(True)
                self.Choice.config(state='disabled')
                self.frame_scale.config(state="disabled")
                self.Length_scale.config(state="disabled")
                self.Conductivity_scale.config(state="disabled")
                self.Temp_scale.config(state="disabled")
                x = int(self.Length_scale.get())
                if x % 2 == 0:
                    self.length_val = x
                else:
                    self.length_val = x - 1
                self.frame_val = int(self.frame_scale.get())
                self.conduct_val = float(self.Conductivity_scale.get())
                self.temp_val = float(self.Temp_scale.get())
                string = self.Choice.get()
                if string == 1:
                    self.choice_val = "circle"
                elif string == 2:
                    self.choice_val = "ellipse"
                elif string == 3:
                    self.choice_val = "rectangle"
                global grid
                start_grid = grid(self.length_val, self.choice_val, self.conduct_val, self.frame_val, self.temp_val)
                global_grid, test_grid, alpha, no_of_frames, conductivity, temperature = start_grid.initialize_grid()

                ## Initialize the microstate table
                Table = Microstate_table()
                microstate_dict = Table.get_table()
                self.animation.run_simulation(global_grid, no_of_frames, length=self.length_val,
                                               microstates_dict=microstate_dict,
                                               conductivity=conductivity, temperature=temperature,save=False)

    ## Terminate button
    def stop_button(self):
        self.start.config(relief="raised", bg="SystemButtonFace")
        self.start.config(state="normal")
        self.Choice.config(state='normal')
        self.frame_scale.config(state="normal")
        self.Length_scale.config(state="normal")
        self.Conductivity_scale.config(state="normal")
        self.Temp_scale.config(state="normal")
        self.animation.on_terminate_clicked()
        ## Reset all the values
        self.length_val=100
        self.frame_val=200
        self.conduct_val=300
        self.temp_val=1
        self.is_clicked = 0
        self.choice_val=""
        raise Exception("Simulation Terminated")

    def save_button(self):
        self.start.config(relief="raised", bg="SystemButtonFace")
        self.start.config(state="disabled")
        self.Choice.config(state='disabled')
        self.frame_scale.config(state="disabled")
        self.Length_scale.config(state="disabled")
        self.Conductivity_scale.config(state="disabled")
        self.Temp_scale.config(state="disabled")
        x = int(self.Length_scale.get())
        if x % 2 == 0:
            self.length_val = x
        else:
            self.length_val = x - 1
        self.frame_val = int(self.frame_scale.get())
        self.conduct_val = float(self.Conductivity_scale.get())
        self.temp_val = float(self.Temp_scale.get())
        string = self.Choice.get()
        if string == 1:
            self.choice_val = "circle"
        elif string == 2:
            self.choice_val = "ellipse"
        elif string == 3:
            self.choice_val = "rectangle"
        global grid
        start_grid = grid(self.length_val, self.choice_val, self.conduct_val, self.frame_val, self.temp_val)
        global_grid, test_grid, alpha, no_of_frames, conductivity, temperature = start_grid.initialize_grid()

        ## Initialize the microstate table
        Table = Microstate_table()
        microstate_dict = Table.get_table()
        self.animation.run_simulation(global_grid, no_of_frames, length=self.length_val,
                                      microstates_dict=microstate_dict,
                                      conductivity=conductivity, temperature=temperature, save=True)

"""
Within the Object class Microstate_table, it stores precomputed values for the number of microstates which is necessary for entropy calculation. 
The problem solved within this class is that it needs to find the number of integer combinations such that a+b+c+d=E where all the variables are integers. 
Now a,b,c,d each can be any integer from 0 all the way to 8 and E can be anywhere from 0 to 32. E is just whats the energy value of each 2x2 subgrid. 
The get_table function relies on recursion to find all the possible combinations of a,b,c,d. These precomputed values are stored within a class. 
When the main code is run, all it needs to do is to check what sort of E value is within each subgrid and take note of its microstate value. 
"""
class Microstate_table:
    def get_table(self):
        result = []
        for E in range(33):
            for a, b, c, d in itertools.product(range(9), repeat=4):
                if a + b + c + d == E:
                    result.append([E, a, b, c, d])
        df = pd.DataFrame(result, columns=["E", "a", "b", "c", "d"])
        df_grouped = df.groupby("E")[["a"]].count().reset_index()
        df_grouped.rename(columns={"a": "Microstates"}, inplace=True)
        return df_grouped.to_dict(orient="records")


# This initialize_grid function is to calculate the move probabilities and environment of the grid
class move_prob:
    def __init__(self):
        pass

    def heat_transfer_prob(self,thermal_conductivity):
        ## Define the constants first
        k = 1 / 6000
        c = 0.2
        a = 0.1
        if isinstance(thermal_conductivity, np.ndarray):
            if np.any(thermal_conductivity) <= 0:
                raise ValueError("Invalid thermal conductivity, conductivity should be a positive number")
            else:
                x = thermal_conductivity
                y = (np.sin(k * x)) ** (c / (x ** a))
                y[thermal_conductivity >= (math.pi / 2) / (k)] = 1
                return y
        else:
            x=thermal_conductivity
            if x<0:
                raise ValueError("Invalid thermal conductivity, conductivity should be a positive number")
            elif thermal_conductivity==0:
                x=0.002
                y = (math.sin(k * x)) ** (c / (x ** a))
                return y
            elif thermal_conductivity>3000*(math.pi):
                y=1
                return y
            else:
                y=(math.sin(k * x)) ** (c / (x ** a))
                return y

class grid:
    def __init__(self,length, choice, thermal_conductivity, no_of_frames, temperature):
        self.length=int(length)
        self.choice=choice
        self.thermal_conductivity=thermal_conductivity
        self.no_of_frames=no_of_frames
        self.temperature=temperature
        self.move_prob=move_prob()

    def initialize_grid(self):
        n = self.length
        grid = np.pad(np.zeros((n, n)), pad_width=1, mode='constant', constant_values=8)
        if self.choice == "rectangle":
            x, y = int(n / 2), int(n / 2)
            z = int(0.35 * x)
            w = int(0.5 * y)
            grid[x: x + z, y: y + w] = 7
        elif self.choice == "circle":
            center = ((self.length / 2), (self.length / 2))
            radius = int(math.sqrt(0.08 * self.length ** 2 / math.pi))
            x, y = np.meshgrid(np.linspace(0, self.length + 2, self.length + 2), np.linspace(0, self.length + 2, self.length + 2))
            distance = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
            grid[distance <= radius] = 7
        elif self.choice == "ellipse":
            center = (self.length // 2, self.length // 2)
            x, y = np.meshgrid(np.linspace(0, self.length + 2, self.length + 2), np.linspace(0, self.length + 2, self.length + 2))
            a = 0.15 * self.length  # x-radius
            b = 0.10 * self.length # y-radius
            ellipse = (x - center[0]) ** 2 / a ** 2 + (y - center[1]) ** 2 / b ** 2
            grid[ellipse <= 1] = 7
        elif self.choice == "small":
            grid = np.array([[8, 8, 8, 8, 8], [8, 3, 1, 0, 8], [8, 2, 7, 4, 8], [8, 1, 6, 5, 8], [8, 8, 8, 8, 8]])
        else:
            print("Invalid choice")
            sys.exit()
        test_grid = np.copy(grid)
        alpha=self.move_prob.heat_transfer_prob(self.thermal_conductivity)

        return grid.astype(int), test_grid.astype(int), alpha, \
               int(self.no_of_frames), self.thermal_conductivity, self.temperature

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
        raise ValueError("The simulation broke the first law of thermodynamics !")

## This is to apply the big function F(M,\alpha) = M_{k+1} iteration.
## This function is conceptually the hardest to make
@njit
def apply_rules_2d(grid,heat_transfer_probability,temperature):
    max_val=8
    non_zero_cells = np.where(grid[1:-1, 1:-1] >= 1)   ## Only find tuples where the non_zero_cells are
    ## Random assortment of non_zero_cells locations while maintaining correspondance between rows and columns
    indices = np.arange(len(non_zero_cells[0]))
    np.random.shuffle(indices)
    non_zero_cells = (non_zero_cells[0][indices], non_zero_cells[1][indices])

    for i in range(len(non_zero_cells[0])):              ## For every non-zero cell
        row, col = non_zero_cells[0][i] + 1, non_zero_cells[1][i] + 1    ## get the x and y axis or positions

        if np.random.rand() < heat_transfer_probability:
            ## Choose which direction it can go
            direction_vector = np.array([[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]])
            ## Check whats happening on all 8 sides of a non-zero cell
            neighbors = np.array(
                [grid[(row - 1), (col - 1)], grid[(row), (col - 1)], grid[(row + 1), (col - 1)], grid[(row + 1), (col)],
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
            if np.all(neighbors == 8) == True:
                pass
            ## Else select only the lists within direction_vector_array that matches with the truth values of neighbors
            ## If neighbors==0 select True and randomly select what is available within direction_vector
            else:
                boolean_dir_index = (neighbors <= 7)
                valid_directions = direction_vector[boolean_dir_index]
                delta_E=difference[boolean_dir_index]
                ### Applying the boltzmann factor to modify probabilities based on energy difference to a 8.
                energy_diff = np.abs(delta_E)
                boltzmann_factors=np.exp(energy_diff*(1/temperature))
                partition_function=np.sum(boltzmann_factors)
                direction_probabilities=boltzmann_factors/partition_function
                cumsum_probs=np.cumsum(direction_probabilities)
                sampling=np.random.rand()
                dir_indexing=np.searchsorted(cumsum_probs,sampling)
                possible_directions = valid_directions[dir_indexing]
                grid[(row + possible_directions[0], col + possible_directions[1])] += 1
                grid[row, col] -= 1
    return grid


# This code is to compute the entropy for version 2 of Automata
def calculate_entropy(grid, microstates_dict):
    ## This section of the code is suggested by ChatGPT-3. I am impressed by its capabilities. I didn't know that np.strides is a function!
    # The code slices the grid into 2x2 matrices. For example, if length=10. There should be 25 2x2 matrices.
    subsize=(2,2)
    shape = grid[1:-1, 1:-1].shape[0] // subsize[0], grid[1:-1, 1:-1].shape[0] // subsize[1], subsize[0], subsize[1]
    strides = grid[1:-1, 1:-1].strides[0] * subsize[0], grid[1:-1, 1:-1].strides[1] * subsize[1], \
              grid[1:-1, 1:-1].strides[0], grid[1:-1, 1:-1].strides[1]
    sliced_grid = np.lib.stride_tricks.as_strided(grid[1:-1, 1:-1], shape=shape, strides=strides)

    ## This line will find for each subgrid what is its energy level
    sub_energy = np.sum(sliced_grid, axis=(2, 3))
    microstates = [d['Microstates'] for d in [microstates_dict[e] for e in sub_energy.flatten()]]
    no_of_microstates = np.array(microstates)
    entropy_per_subgrid=np.log(no_of_microstates)
    entropy = np.sum(entropy_per_subgrid)
    return entropy

"""
The class AutomataSimulation is to house an object class where the simulation is held. 
It requires the output from initialize_grid function to run properly 
"""
class AutomataSimulation:
    def __init__(self):
        self.is_running = False
        self.Terminated = False

    def run_simulation(self, grid, no_of_frames, length, microstates_dict, conductivity, temperature,save):
        if self.is_running == True:
            self.rate = 50
        elif self.is_running==False:
            self.rate = 10000000
        self.n = length
        self.grid = grid
        self.conductivity = conductivity
        if temperature == 0:
            self.temperature = 0.5
        else:
            self.temperature = temperature
        self.no_of_frames = no_of_frames
        self.test_grid = np.copy(self.grid)
        self.fig, (self.ax, self.ax2) = plt.subplots(1, 2, figsize=(10, 6), width_ratios=[1.7, 0.95])

        self.im = self.ax.imshow(grid[1:-1, 1:-1], cmap='plasma', vmin=0, vmax=8)
        self.fig.colorbar(self.im, ax=self.ax, label='Energy level')
        self.microstates_dict = microstates_dict
        self.entropy = []
        if save==False:
            plt.subplots_adjust(top=0.95, wspace=0.2)
            # Add the sliders for conductivity and temperature
            self.conductivity_slider_ax = self.fig.add_axes([0.1, 0.05, 0.5, 0.04])
            self.conductivity_slider = Slider(self.conductivity_slider_ax, 'Conductivity', 0, 3000,
                                              valinit=self.conductivity)
            self.conductivity_slider.on_changed(self.update_conductivity)

            self.temperature_slider_ax = self.fig.add_axes([0.1, 0.0, 0.5, 0.04])
            self.temperature_slider = Slider(self.temperature_slider_ax, 'Temperature', 0.0, 7.0,
                                             valinit=self.temperature)
            self.temperature_slider.on_changed(self.update_temperature)

            ## Add a pause button
            self.pause_button = button(plt.axes([0.04, 0.92, 0.06, 0.07]), 'Pause')
            self.pause_button.on_clicked(self.on_pause_clicked)
            self.ani = animation.FuncAnimation(self.fig, self.update, frames=self.no_of_frames, repeat=False,
                                               interval=self.rate)
            plt.show()

        elif save==True:
            self.ani = animation.FuncAnimation(self.fig, self.update, frames=self.no_of_frames, repeat=False,
                                               interval=self.rate)
            self.ani.save("animation.gif",writer="pillow")



    def on_pause_clicked(self, *args, **kwargs):
        if self.is_running:
            self.ani.resume()
            self.pause_button.label.set_text('Pause')
        else:
            self.ani.pause()
            self.pause_button.label.set_text('Resume')
        self.is_running = not self.is_running

    def on_terminate_clicked(self, *args, **kwargs):
        self.ani.event_source.stop()
        plt.close(self.fig)

    def update_conductivity(self, value):
        self.conductivity = float(value)
        self.ax2.set_title("Conductivity: {:.1f} W/m.K".format(self.conductivity), loc="center")

    def update_temperature(self, value):
        self.temperature = float(value)
        self.ax.set_title("T: {:.0f} Kelvin".format(self.temperature), loc="left")

    def update(self, frame):
        alpha = move_prob().heat_transfer_prob(self.conductivity)
        grid = apply_rules_2d(self.grid, alpha, self.temperature)
        self.im.set_data(grid[1:-1, 1:-1])
        self.ax.set_title("T: {:.1f} Kelvin".format(self.temperature), loc="left")
        self.ax.set_title("Move probability: {:.2f} ".format(alpha), loc="right")
        entropy = calculate_entropy(grid, self.microstates_dict)
        self.entropy.append(entropy)
        self.ax2.plot(self.entropy, color='blue')
        self.ax2.set_xlabel("Generation")
        self.ax2.set_ylabel("Entropy $S/k_b$")
        self.ax2.set_title("Conductivity: {:.1f} W/m.K ".format(self.conductivity), loc="center")

        if not check_energy_conversion_2D(self.test_grid,grid) or frame>self.no_of_frames:
            self.ani.event_source.stop()
            sys.exit()

"""
The final class of DataCollector is just a means to collect data for a 3D/2D plots from the simulation run and plot it. 
It has its own defined parameters and collect_data is just a function to compute the datapoints. 
You need to specify the conductivity range, number of iterations (frames), temperature range and number of points for 
the conductivity and temperature range. 
After that's done you can call the method plot_entropy to see the nice 3D plot that is produced. 
WARNING: THIS SCRIPT WILL KILL YOUR CPU IF ITS A POTATO CPU or take 1 day to run. 
"""
class DataCollector:
    def __init__(self,conductivities, temperature, frames, points):
        ## Initialize necessary standardized inputs
        self.choice="circle"
        self.length=100
        self.conductivities=conductivities
        self.frames=frames
        self.temperature=temperature
        self.points=points
        ## Create an instance from another class using standardized measures
        self.begin=grid(self.length,self.choice,self.conductivities,self.frames,self.temperature)
        self.move=move_prob()

    def data_entropy_3D(self):
        if isinstance(self.conductivities,np.ndarray) ^ isinstance(self.temperature, np.ndarray)==True:
            raise TypeError("In this method both inputs need to be a float or integer")

        else:
            try:
                C_array=np.linspace(0.1, self.conductivities, self.points)
                T_array=np.linspace(0.1, self.temperature, self.points)
                ## Creating the arrays from the object class
                grid, test_grid, alpha, no_of_frames, conductivity, temperature=self.begin.initialize_grid()
                alpha_array=self.move.heat_transfer_prob(C_array)
                ## Get the table
                Table = Microstate_table()
                microstate_dict = Table.get_table()
                entropies=[]
                alpha_str=alpha_array.astype(str)
                T_str=T_array.astype(str)
                for j in range(len(T_array)):
                    for k in range(len(alpha_str)):
                        grid = np.copy(test_grid)
                        for n in range(self.frames):
                            grid = apply_rules_2d(grid, float(alpha_str[k]) , float(T_str[j]))

                        entropy = calculate_entropy(grid, microstates_dict=microstate_dict)
                        entropies.append(entropy)

                    ## Entropy should run on another indentation line only when its done with the number of simulations
                return C_array, T_array, np.array(entropies).reshape( (len(T_array),len(alpha_str)) )

            except:
                raise TypeError("Both inputs cannot be an array")


    def data_entropy_2D_C(self):
        if isinstance(self.temperature, np.ndarray)==False:
            raise TypeError("This method requires temperature to be an object of class ndarray")
        else:
            C_array = np.linspace(0.1, self.conductivities, self.points)
            ## Creating the arrays from the object class
            grid, test_grid, alpha, no_of_frames, conductivity, temperature = self.begin.initialize_grid()
            alpha_array=self.move.heat_transfer_prob(C_array)
            ## Get the table
            Table = Microstate_table()
            microstate_dict = Table.get_table()
            entropies = []
            alpha_str = alpha_array.astype(str)
            T_str = self.temperature.astype(str)
            for j in range(len(T_str)):
                for k in range(len(alpha_str)):
                    ## reset the grid
                    grid=np.copy(test_grid)
                    for n in range(self.frames):
                        grid = apply_rules_2d(grid, float(alpha_str[k]), float(T_str[j]))

                    entropy = calculate_entropy(grid, microstates_dict=microstate_dict)
                    entropies.append(entropy)

            return C_array, self.temperature, np.array(entropies).reshape(len(self.temperature), len(alpha_str))

    def data_entropy_2D_T(self):
        if isinstance(self.conductivities, np.ndarray)==False:
            raise TypeError("This method requires conductivity to be an object of class ndarray")
        else:
            T_array = np.linspace(0.1, self.temperature, self.points)
            ## Creating the arrays from the object class
            grid, test_grid, alpha, no_of_frames, conductivity, temperature = self.begin.initialize_grid()
            alpha_array=self.move.heat_transfer_prob(self.conductivities)
            ## Get the table
            Table = Microstate_table()
            microstate_dict = Table.get_table()
            entropies = []
            alpha_str = alpha_array.astype(str)
            T_str = T_array.astype(str)
            for j in range(len(alpha_str)):
                for k in range(len(T_array)):
                    ## reset the grid
                    grid=np.copy(test_grid)
                    for n in range(self.frames):
                        grid = apply_rules_2d(grid, float(alpha_str[j]), float(T_str[k]))

                    entropy = calculate_entropy(grid, microstates_dict=microstate_dict)
                    entropies.append(entropy)

            return self.conductivities, T_array, np.array(entropies).reshape(len(alpha_str), len(T_array))

    def plot_entropy_3D(self,Conductivity_array,Temperature_array,entropy_array):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Generate some example data
        x = Conductivity_array
        y = Temperature_array
        X, Y = np.meshgrid(x, y)
        Z = entropy_array

        # Plot the surface with a color map
        # Z = np.array([[1031.81782308, 3100.89827299],[ 783.04357599, 1289.5916573 ]])
        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True)

        # Add a color bar
        fig.colorbar(surf, shrink=0.5, aspect=5)

        # Set axis labels
        ax.set_xlabel('Conductivity: W/m.K')
        ax.set_ylabel('Temperature: Kelvin')
        ax.set_zlabel('Entropy $S/k_b$')

        # Rotate the view
        ax.view_init(azim=-120, elev=30)

        plt.show()

    def plot_entropy_2D(self,Conductivity_array,Temperature_array,entropy_array):
        if len(Conductivity_array) > len(Temperature_array):
            x_data=Conductivity_array
            y_matrix=entropy_array
            T_legends=Temperature_array.astype("str")
            for i in range(len(T_legends)):
                labels=T_legends[i] + "K"
                plt.plot(x_data,y_matrix[i],label=labels)

            plt.xlabel("Conductivities W/m.K")
            plt.ylabel("Entropy $S/k_b$")
            plt.title(f"Entropy after {self.frames} iterations")
            plt.legend(loc="lower center", ncols=3)
            plt.show()

        elif len(Conductivity_array) < len(Temperature_array):
            x_data=Temperature_array
            y_matrix=entropy_array
            C_legends=Conductivity_array.astype(str)
            for g in range(len(C_legends)):
                labels = C_legends[g] + " W/m.K"
                plt.plot(x_data,y_matrix[g], label=labels)

            plt.xlabel("Temperatures K")
            plt.ylabel("Entropy $S/k_b$")
            plt.title(f"Entropy after {self.frames} iterations")
            plt.legend(loc="upper right", ncols=2)
            plt.show()

        else:
            raise ValueError("Conductivities and Temperatures array cannot be of the same size.")

