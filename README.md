# Entropy_Simulation
A cellular automata inspired simulation to demonstrate the 2nd law of thermodynamics. 
The Simulations can be viewed within the file labelled GiFs. 

Developer: Bowen Shiro Husin

Date: 2023-02-22

## About
Entropy is a fascinating concept in physics. The idea of quantifying the number of configurations that a system can occupy is a powerful idea with huge impact within the fields of mathematics, computer science and computational biology. 

In this project, I was inspired by Conway's game of life and I was curious of using Cellular Automata (CA) to model a stochastic process. The main source code is labelled [Automata.py](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Code/Automata.py).

As with any cellular automata project, the rules of the simulation needs to be established. For a more comprehensive explanation of the rules please see [here](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/rules.md).

For more details on the calculation of entropy, please see [here](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Entropy_Computation.pdf).

For a full explanation of what my thought process is, see [here](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Thoughts.pdf).

Examples of the simulations can be shown below in some of the Gifs. 

Simulation with a 10% move probability  |  Simulation with a 50% move probability |  
:-------------------------:|:-------------------------:|
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Entropy_alpha%3D10%25.gif)  |  ![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Entropy_alpha%3D50%25.gif)| 


Simulation with no restrictions |
:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Entropy_alpha%3D100%25.gif)

## Usage 
To start the code run [main.py](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Code/main.py) in your local machine and ensure that you have numpy, matplotlib and numba installed. 
At the same time ensure Automata.py is in the same directory as main.py.

Once main.py is initialized you will be prompted with the following questions.
 - The size of the grid (Recommended: 200 to 250)
 - What sort of move probability you want (Between 0-1)
 - What sort of shape you want as a start (Rectangle, circle or ellipse)
 - How many frames should the animation run for (Recommended: 300 to 600) 

The bug responsible for biased movement in version 1 has been resolved.

## Version 2 
While version 1 successfully simulates random movement and brownian motion in some ways, I wasn't really done or satisfied that it only shows idealised systems. Hence, I wanted to add multiple features towards the code. The modifications of version 2 are seen [here](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Rules.md)

Version 2 brings a lot more features into the code compared to version 1. Parameters such as Conductivity and Temperature are added into the simulation and the "move probability" or "alpha" is a calculated value where Conductivity is mapped to it via a function. Likewise, the method of using a prompt in order to unput the initial values is replaced with a GUI element using the tkinter library. 

The GUI element looks like this: 
Initial inputs |
:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/GUI.png)

To use it use the slides to select what sort of variable you want and click the "Start Simulation" button to start the simulation. When the simulation is runned you can no longer change any inputs within the slider but you can make changes into the simulation via the matplotlib window that shows up after. 

Sliders in the matplotlib animation |
:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Slider_example.png)

You can click the pause button to stop/resume the simulation and dynamically change the temperature and conductivity and see the results. 

Within the GUI element, the "Terminate" button will delete the matplotlib figure and reset all the buttons. The "Save" button is to save the animation. By default, the animation is saved as a gif labelled "animation.gif" and contains no sliders or buttons in the frames of the gifs. To avoid unexpected errors, please try to do the tasks one at a time and not try to save or terminate the simulation when it is running. 

Computations and the tought process in calculating entropy can be seen [here](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Automata.pdf)

The source code for running version 2 of Automata is [Engine.py](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Code%20Version%202/Engine.py). The [run.py](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Code%20Version%202/run.py) file runs the entire code and [Plots.py](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Code%20Version%202/Plots.py) is meant to do some rudimentary analysis using defined classes in Engine.

Examples of some of the simulation for version 2 are seen down below: 

Low temperature, medium conductivity  |  High temperature, higher conductivity |  
:-------------------------:|:-------------------------:|
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/animation_2.gif)  |  ![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/animation_3.gif)| 


Low Temp, High conductivity |
:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/animation_1.gif)
## Usage 
To start the code run [run.py](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Code%20Version%202/run.py) in your local machine and ensure that you have numpy, matplotlib numba, pandas and tkinter installed.
At the same time ensure that Engine.py is within the same directory as run.py. After that choose your values through the GUI that pops up and click the "Start Simulation" button to start the animation. 

As a small catch, make sure that your numpy is a version that is less than 1.24 Otherwise, the @njit decorator will not work as intended and massively slows down the simulation. 
 
## Dependencies
- numpy=1.23.5
- matplotlib=3.6.3
- pandas=1.53
- numba=0.56.4
- tk=8.6.12
