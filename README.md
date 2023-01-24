# Entropy_Simulation
A cellular automata inspired simulation to demonstrate the 2nd law of thermodynamics. 
The Simulations can be viewed within the file labelled GiFs. 
# Entropy_Simulation

Author: Bowen Shiro Husin

Date: 2023-01-25

## About
Entropy is a fascinating concept in physics. The idea of quantifying the number of configurations that a system can occupy is a powerful idea with huge impact within the fields of mathematics, computer science and computational biology. 

In this project, I was inspired by Conway's game of life and I was curious of using Cellular Automata (CA) to model a stochastic process. The main source code is labelled [Automata](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Automata.py)

As with any cellular automata project, the rules of the simulation needs to be established. For a more comprehensive explanation of the rules please see [here](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/rules.md).

For more details on the calculation of entropy, please see [here].

Examples of the simulations can be shown below in some of GiFs.

Simulation with a 10% move probability  |  Simulation with a 50% move probability |  
:-------------------------:|:-------------------------:|
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Entropy_alpha%3D10%25.gif)  |  ![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Entropy_alpha%3D50%25.gif)| 


Simulation with a 100% move probability |
:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Entropy_alpha%3D100%25.gif)


## Dependencies
- numpy=1.23.1
- matplotlib=3.6.3
- python=3.10
- numba=0.56.4

## Work in progress
