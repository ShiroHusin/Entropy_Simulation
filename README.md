# Entropy_Simulation
A cellular automata inspired simulation to demonstrate the 2nd law of thermodynamics. 
The Simulations can be viewed within the file labelled GiFs. 

Author: Bowen Shiro Husin

Date: 2023-01-30

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

Then the animation will run accordingly. As a small catch, make sure that your numpy is installed as 1.23.1 otherwise numba wouldn't work at all and your simulation will be incredibly slow. 
 
## Dependencies
- numpy=1.23.1
- matplotlib=3.6.3
- pandas=1.53
- numba=0.56.4

The bug responsible for biased movement in version 1 has been resolved.

## Version 2 
Currently, each of the cells can only take 2 discrete values. 1 or 0. In actual quantum mechanical systems, a particle can have multiple discrete energy levels it can take. For instance, the ground state might be e, the first excited state is 2e, the second excited state is 3e and so forth. 

I thought what if each of the cells can take 9 discrete values these are 0, 1, 2, 3, 4, 5, 6, 7, and 8. 0 corresponds to the ground state and 8 is equivalent to the maximum amount of energy that each cell (particle) can take. 

It would be quite interesting to see if I tinker rule 1 in [rules.md](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/rules.md) while keeping everything else enforced. 

## Currently working in version 2. 
Doing some researching of using boltzmann distribution etc, to challenge the assumption of "equal a priori probabilities" becuase version 1 runs on that assumption which is actually incorrect for real life scenarios.  
