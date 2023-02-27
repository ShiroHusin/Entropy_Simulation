# Visualizing entropy through cellular automata

During the holiday season, I was reading Conway's game of life in wikipedia and rewatching Vertiasium's excellent video about [Math's fundamental flaw](https://www.youtube.com/watch?v=HeQX2HjkcNo&ab_channel=Veritasium). Likewise, I wanted to do something productive during the holiday season and learn the fundamentals of Python through doing coding projects. From what I remember I think its about January the 1st or 2nd late at night when an idea popped in my mind. The question I asked was what if I borrowed some concepts from cellular automata to visualise and show what entropy is? Given the fact that quite a lot of people are unaware of this fascinating concept in Physics, I wanted to do a project that hopefully makes it a bit easier to see whats going on when entropy increases. After long hours of thinking and strategising what approach to take, I came up with this gif as the final form: 

Entropy visualisation|
:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/animation_1.gif)  | 

I had a lot of fun in making this project and since I'm still not sure whether I "get" it. I figured that I should explain step by step and what I did to bring the idea into life. 

## Dependencies
- Python 3.10 
- NumPy 1.23.5 
- Pandas 1.5.2
- Matplotlib 3.6.2
- Numba 0.56.4 
- Tkinter 8.6.12

Note that you can use newer versions of the packages listed above except for NumPy as NumPy 1.24 runs into errors with the numba JIT compiler. 

## Deciding on the rules
As cellular automata is the central idea behind the simulation. It is important to decide first on what the rules are. Just like in any physical system I wanted the rules to mirror the conservation of energy and another rule for movement of energy. Earlier versions of the simulation allowed for the cells to either be binary digits of 1 and 0 while later versions of the cells allowed for discrete values ranging from 0 to 8. The rules for version 1 and 2 are within this [link](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/rules.md) and this [link](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Rules.md). Bascially the idea is the sum of all the numbers inside the grid cannot change over time and every non zero number can change one of its 8 neighbouring value. For instance, in picture below,the cell labelled 6 can go to any one of its grey squares and but it cannot go to the 8 cell because its occupied and 8 is the maximum value it can reach.  

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/image.png)

At this point one can postulate that a unit of energy from the 6 cell can go to the grey cells at $\frac{1}{7}$ each right?

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/acutally_no.gif)

After running some prototypes, I noticed that something looks seriously wrong, where the grid animations seem to scream at me that a feature was missing. What was missing is the fact that energy will always want to occupy the particles that are of lowest energy first before going somewhere else. For instance, in chemistry the electron addition into ions don't go in the order of 4s, 4p but instead go in the order of 4s, 3d and then 4p. Hence, I needed some way to modify the probabilities.  


## A tweak on the rules of movement 
Enter the boltzmann factor, or some form of it. According to wikipedia the boltzmann factor is defined as: 

$$\large \frac{p_{i}}{p_{j}}= \large e^{\dfrac{\epsilon_{j}-\epsilon_{i}}{kT}}$$


In this case the probability fraction tells us the probability that something is at state i divided by state j is equal to all the other stuff. After doing a bunch or reading, I decided that this concept is useful in solving my problem. However, it isn't all that clear on how am I going to apply this. For instance the fractions don't seem to help very much in explicity changing the probabilities. After much debate, I decided to do a little bit of a hack. This might be completely illegal to do but I decided to modify the equation to be: 

$$\large p_{j}= \large e^{\dfrac{8-\epsilon_{j}}{T}}$$

In this way we can calculate the individual cell's boltzmann factor by computing how far is it from the maximum energy value of 8. Likewise, I also decided to remove to the boltzmann constant $k_{b}$ so that any change in this parameter will easily change the outcome of the simulation. After thats done we can add all of them up similar to the partision function formalized as: 

$$\large \sum_{j=1}^{\kappa} e^{\frac{8-\epsilon_{j}}{T}}  $$
For the case above $\large \kappa$=7 as there are only 7 viable cells that it can go to. After doing some maths the probabilities of where each unit of energy can go to is: 

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/modified_probs.png)

Assuming that T=1, there is a 63.3% chance that the 6 cell gives up a unit of energy to the 0 cell and a 23.3% chance that the 6 cell transfers a unit of energy to the 1 cell. Likewise, the chances that the 6 cell sends a unit of energy to the 7 cell is close to 0. 

## Calculating entropy
Now that the rules of movement are done, we now get to the meaty part which is how am I suppose to compute entropy? Before we start lets get back to the basics. The boltzmann equation to compute entropy is written as: 

$$\large S=k_{b}Ln(\Omega)$$ 

Our job is to find a way to compute $\large \Omega$. Yes simple right? But now what?  
For this problem I spent quite a long time thinking and trying to find information throughout the internet to find clues on how to compute $\large \Omega$ for this specific problem. Of course, I asked ChatGPT as well to give me suggestions but spoiler alert that conversation was fruitless as it gave me suggestions that just made everthing much harder. After some despairing, It was late at night when a caveman moment struck me. Remembering the excellent video that I watched ParthG made on [entropy](https://www.youtube.com/watch?v=mg0hueOyoAw&ab_channel=ParthG). I knew that the method requires me to do something related to counting the total number of integer combinations possible that adds up to a number. Hence I thought, rather than computing the entire grid which would be insane to do, what if I break the grid down into smaller byte sized chunks or 2x2 matrices as follows: 

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/matrix_splitting.png)

For now, consider the fact that the middle matrix is the grid simulation itself and lets call each of the sub-matrices as $\large X_{j}$ and allow the grid to be square in shape and have its dimensions to be solely even integers. From simple math, we can deduce that there should be $\large \frac{l^2}{4}$ different sub-matrices or $\large X_{j}$. Now, there are 4 cells within each element in $\large X_{j}$. Lets call this a, b, c, d. Noting that each cell can only be 0-8. This means that the energy level for each sub-matrix $X_{j}$ must range from 0-32. If we call this as $\large \Phi_{j}$, it means that: 

$$\large 0\leq \Phi_{j} \leq 32, \;\;\; \Phi_{j} \in \mathbb{Z} $$ 
Additionally, we have to find the total number of integer combinations possible for: 
$$\large  a_{j}+b_{j}+c_{j}+d_{j}=\Phi_{j}$$
