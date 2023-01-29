# Entropy_Simulation
A cellular automata inspired simulation to demonstrate the 2nd law of thermodynamics. 
The Simulations can be viewed within the file labelled GiFs. 

Author: Bowen Shiro Husin

Date: 2023-01-30

## About
Entropy is a fascinating concept in physics. The idea of quantifying the number of configurations that a system can occupy is a powerful idea with huge impact within the fields of mathematics, computer science and computational biology. 

In this project, I was inspired by Conway's game of life and I was curious of using Cellular Automata (CA) to model a stochastic process. The main source code is labelled [Automata.py](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Code/Automata.py)

As with any cellular automata project, the rules of the simulation needs to be established. For a more comprehensive explanation of the rules please see [here](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/rules.md).

For more details on the calculation of entropy, please see [here](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Entropy_Computation.pdf).

For a full explanation of what my thought process is, see [here](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Thoughts.pdf)

Examples of the simulations can be shown below in some of the Gifs. 

Simulation with a 10% move probability  |  Simulation with a 50% move probability |  
:-------------------------:|:-------------------------:|
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Entropy_alpha%3D10%25.gif)  |  ![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Entropy_alpha%3D50%25.gif)| 


Simulation with no restrictions |
:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Entropy_alpha%3D100%25.gif)

## Usage 
To start the code run [main.py](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Code/main.py) in your local machine and ensure that you have numpy, matplotlib and numba installed. 
At the same time ensure Automata.py is in the same directory as main.py

Once main.py is initialized you will be prompted with the following questions
 - The size of the grid (Recommended: 200 to 250)
 - What sort of move probability you want (Between 0-1)
 - What sort of shape you want as a start (Rectangle, circle or ellipse)
 - How many frames should the animation run for (Recommended: 300 to 600) 

Then the animation will run accordingly. As a small catch, make sure that your numpy is installed as 1.23.1 otherwise numba wouldn't work at all and your simulation will be incredibly slow. 
 
## Dependencies
- numpy=1.23.1
- matplotlib=3.6.3
- pandas=1.53
- numba=0.56.4

## Potential bugs
As seen from the gifs there are a slight trend towards the upwards direction. I ran the simulation for 6000 iterations and calculated how many times it wants to choose the top direction or the vector [0, -1] it turns out there is might be slight bias and I have no idea what is causing it. The bar chart for the results is shown below: 
Slight bias towards the top direction|
:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/bias.png)

Note that "T" is top, "B" is bottom, "R" is right, "L" is left. "TR" is top-right or vector [1, -1]. Top is chosen about 13.5% of the time about 1% higher than the rest.
