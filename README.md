# Visualizing the second law of thermodynamics through cellular automata

During the holiday season, I was reading Conway's game of life in wikipedia and rewatching Vertiasium's excellent video about [Math's fundamental flaw](https://www.youtube.com/watch?v=HeQX2HjkcNo&ab_channel=Veritasium). Likewise, I wanted to do something productive during the holiday season and learn the fundamentals of Python through doing coding projects. I think its about January the 1st or 2nd late at night when an idea popped in my mind. The question I asked was what if I borrowed some concepts from cellular automata to visualise and show what entropy is? Given the fact that quite a lot of people are unaware of this fascinating concept in Physics, I wanted to do a project that hopefully makes it a bit easier to see whats going on when entropy increases. After long hours of thinking and strategising what approach to take I came up with this gif as the final form: 

Entropy visualisation|
:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/animation_1.gif)  | 

I had a lot of fun in making this project and since I'm still not sure whether I "get" it. I figured that I should explain step by step and what I did to bring the idea into life. 

## Dependencies
-Python 3.10 or above 

-NumPy 1.23.5 

-Pandas 1.5.2

-Matplotlib 3.6.2

-Numba 0.56.4 

-Tkinter 8.6.12
Note that you can use newer versions of the packages listed above except for NumPy as NumPy 1.24 runs into errors with the numba JIT compiler. 

## Deciding on the rules
As the simulation is 
