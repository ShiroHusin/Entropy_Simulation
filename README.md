# Table of contents
1. [Introduction](#introduction)
2. [Deciding the rules](#rules)
3. [Rules of movement](#movement)
4. [Computing entropy](#entropy)
5. [Other parameters](#other)
6. [Usage](#use)

## Visualizing entropy through cellular automata <a name="introduction"></a>

During the holiday season, I was reading Conway's game of life in wikipedia and rewatching Vertiasium's excellent video about [Math's fundamental flaw](https://www.youtube.com/watch?v=HeQX2HjkcNo&ab_channel=Veritasium). Likewise, its been 5 months when I started to take programming seriously and I wanted to do something productive by doing coding projects. From what I remember I think its about January the 1st or 2nd late at night when an idea popped in my mind. <strong> The question I asked was what if I borrowed some concepts from cellular automata to visualise and show what entropy is? </strong> This question was the fundamental driving force that I want answered.

Likewise, given the fact that quite a lot of people are unaware of this fascinating concept in Physics, I wanted to do a project that hopefully makes it a bit easier to see whats going on when entropy increases. After long hours of thinking and strategising what approach to take, I came up with this gif as the final form: 

Entropy visualisation|
:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/animation_1.gif)  | 

I had a lot of fun in making this project and since I'm still not sure whether I "get" it. I figured that I should explain step by step and what I did to bring the idea into life. 

### Dependencies
- Python 3.10 
- NumPy 1.23.5 
- Pandas 1.5.2
- Matplotlib 3.6.2
- Numba 0.56.4 
- Tkinter 8.6.12

Note that you can use newer versions of the packages listed above except for NumPy as NumPy 1.24 runs into errors with the numba JIT compiler. 

## Deciding on the rules <a name="rules"></a>
As cellular automata is the central idea behind the simulation. It is important to decide first on what the rules are. Just like in any physical system I wanted the rules to mirror the conservation of energy and another rule for movement of energy. Earlier versions of the simulation allowed for the cells to either be binary digits of 1 and 0 while later versions of the cells allowed for discrete values ranging from 0 to 8. The rules for version 1 and 2 are within this [link](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/rules.md) and this [link](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Rules.md). Basically the idea is the sum of all the numbers inside the grid cannot change over time and every non zero number can change one of its 8 neighbouring value by 1. For instance, in picture below,the cell labelled 6 can go to any one of its grey squares and but it cannot go to the 8 cell because its occupied and 8 is the maximum value it can reach.  

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/image.png)

At this point one can postulate that a unit of energy from the 6 cell can go to the grey cells at $\frac{1}{7}$ each right?

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/acutally_no.gif)

After running some prototypes, I noticed that something looks seriously wrong, where the grid animations seem to scream at me that a feature was missing. What was missing is the fact that energy will always want to occupy the particles that are of lowest energy first before going somewhere else. For instance, in chemistry the electron addition into ions don't go in the order of 4s, 4p but instead go in the order of 4s, 3d and then 4p. Hence, I needed some way to modify the probabilities.  


## A tweak on the rules of movement <a name="movement"></a>
Enter the boltzmann factor, or some form of it. According to wikipedia the boltzmann factor is defined as: 

$$\large \frac{p_{i}}{p_{j}}= \large e^{\dfrac{\epsilon_{j}-\epsilon_{i}}{kT}}$$


In this case the probability fraction tells us the probability that something is at state i divided by state j is equal to all the other stuff. After doing a bunch of reading, I decided that this concept is useful in solving my problem. However, it isn't all that clear on how am I going to apply this. For instance the fractions don't seem to help very much in explicity changing the probabilities. After much debate, I decided to do a little bit of a hack. This might be completely illegal to do but I decided to modify the equation to be: 

$$\large p_{j}= \large e^{\dfrac{8-\epsilon_{j}}{T}}$$

In this equation, j represeents the cells wiithin the neighbours and $\large \epsilon_{j}$ tells us the energy of the cell. An implicit assumption I made is that this equation doesn't care about what energy level the cell in question is but only cares about its 8 neighbouring elements. In this way we can calculate the individual cell's boltzmann factor by computing how far is it from the maximum energy value of 8. Likewise, I also decided to remove to the boltzmann constant $k_{b}$ so that any change in this parameter will easily change the outcome of the simulation. After thats done we can add all of them up similar to the partision function formalized as: 

$$\large \sum_{j=1}^{\kappa} e^{\frac{8-\epsilon_{j}}{T}}  $$

For the case above $\large \kappa$=7 as there are only 7 viable cells that it can go to and the 8 cell can be filtered out through boolean indexing. After doing some maths the probabilities of where each unit of energy can go to is: 

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/modified_probs.png)

Assuming that T=1, there is a 63.3% chance that the 6 cell gives up a unit of energy to the 0 cell and a 23.3% chance that the 6 cell transfers a unit of energy to the 1 cell. Likewise, the chances that the 6 cell sends a unit of energy to the 7 cell is close to 0. 

## Calculating entropy <a name="entropy"></a>
Now that the rules of movement are done, we now get to the meaty part which is how am I suppose to compute entropy? Before we start lets get back to the basics. The boltzmann equation to compute entropy is written as: 

$$\large S=k_{b}Ln(\Omega)$$ 

Our job is to find a way to compute $\large \Omega$. Yes simple right? But now what?  

I spent quite a long time thinking and trying to find information throughout the internet to find clues on how to compute $\large \Omega$ for this specific problem. Of course, I asked ChatGPT as well to give me suggestions but spoiler alert, that conversation was fruitless as it gave me suggestions that just made everthing much harder. After some despairing, It was late at night when a caveman moment struck me. Remembering the excellent video that I watched ParthG made on [entropy](https://www.youtube.com/watch?v=mg0hueOyoAw&ab_channel=ParthG). I knew that the method requires me to do something related to counting the total number of integer combinations possible that adds up to a number. Hence I thought, rather than computing the entire grid which would be insane to do, what if I break the grid down into smaller byte sized chunks or 2x2 matrices as follows: 

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/matrix_splitting.png)

For now, consider the fact that the middle matrix is the grid simulation itself and lets call each of the sub-matrices as $\large X_{j}$ and allow the grid to be square in shape and have its dimensions to be solely even integers.More formally let $\large l$ be the dimensions of the square grid and $\large l \in 2\mathbb{Z}$ From simple math, we can deduce that there should be $\large \frac{l^2}{4}$ different sub-matrices or $\large X_{j}$. Now, there are 4 cells within each element in $\large X_{j}$. Lets call this a, b, c, d. Noting that each cell can only be 0-8. This means that the energy level for each sub-matrix $X_{j}$ must range from 0-32. If we call this as $\large \Phi_{j}$, it means that: 

$$\large 0\leq \Phi_{j} \leq 32, \Phi_{j} \in \mathbb{Z} $$ 

Additionally, we have to find the total number of integer combinations possible for: 

$$\large  a_{j}+b_{j}+c_{j}+d_{j}=\Phi_{j}$$

Fortunately, this problem is not too hard to solve. As there are hundreds of examples from Stack Overflow. For each value of $\large \Phi_{j}$ ranging from 0 to 32. The total number of viable integer combinations is the microstate associated associated with $\large \Phi_{j}$. Lets call this value $\large \omega_{j}$. Some examples of these values can be seen in the table below and all the computer needs is to match the $\large \Phi_{j}$ value for each sub-matrix $X_{j}$ through a pandas dataframe or dictionary.

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/microstate_table.png)

Now due to the basic counting principles in math. The total amount of configurations that the grid can take is: 

$$\large \Omega=\prod_{j=1}^{\frac{l^2}{4}} \omega_{j} $$ 

For large grids, I might run into int32 or even int64 errors in my computer as the numbers can get way too big. However, using the product rules in logartihms we can write the entropy equation as: 

$$\large \dfrac{S}{k_{b}}=\sum_{j=1}^{\frac{l^2}{4}} ln(\omega_{j})$$

## Other dynamically changing parameter <a name="other"></a>
Now at this point, I was quite happy with the fact that I've cracked the nut. However, I wanted to include 1 more idea within the simulation in whuch the user can dynamically change. It's here when I thought you could actually try to put conductivity as well. In the older version where the code is in [here](https://github.com/ShiroHusin/Entropy_Simulation/tree/main/Code). I had already implemented a parameter called $\large \alpha$ or move probability. This parameter controls the rate at which the code responsible for moving the numbers of the cells is executed. Now I figured that this has could be related to how "conductive" my grid is. At least my intuition told me so. Hence, I decided that I should have a function which maps conductivity to $\large \alpha$ wjere alpha can only range from 0 to 1. 

At this stage, I could use a logistic function or $\large \tanh (x)$ but those 2 functions did not really provide me with the characteristics I would like. Namely, I wanted a function that grew quite fast from 0-100 and grows at an ever slower rate to 1. This is where GeoGebra proved useful and I decided to use a custom sin(x) function after playing around with the graphs. So If I define:

$$\large g(c)=\sin (\frac{1}{6000}c)^\frac{0.2}{0.1^c}$$

I can then construct a peice-wise function for 3 scenarios where $\large \alpha$ is equal 1 if $\large c>3000\pi$, else if $\large 0 < c \leq 3000\pi$ then $\large \alpha=g(c)$, else if c=0 then $\large \alpha=0.014$. If for for some reason, c is put as a negative, then a ValueError is raised because I don't think negative conductivity can ever exist. Finally to sum, up the entire code structure would probably look close to this diagram: 

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Process_flow_diagram.png)

While $\large K\leq I$ where $\large I$ is the number of iterations, do the following:

$\large a$ is the elements and I want it such that for all non zero elements of a within grid $\large M$ to first be filtered out by the random number generator and then apply the rules for movement. After that is compiled to a new grid $\large M_{K+1}$, I want it to also compute the entropy via the function $\large S(M_{k+1})$ and the microstates is inferred from the microstate dictionary or dataframe. This will form 1 datapoint in the graph. Once thats done add 1 to k and repeat it all over again until $\large k=I$ 

## Usage <a name="use"></a>
Now, at this point I was happy with how things are going. However, from version 1, I thought that inputting the initial conditions into the Python prompt over and over gain to be very annoying. Hence I decided to replace it with a GUI control panel using Tkinter. The example is shown here: 

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/GUI.png)

The GUI element shows sliders for parameters as grid length, conductivity, and temperature. 

At the current moment there are only 3 choices or starting shapes that you start with either "circle", "ellipse" or "rectangle". Once you have selected all the parameters you can then start the simulation by clicking the "Start Simulation" button. The "save" button saves the simulation as a gif in a file named "animation.gif" and the "Terminate" button halts the simulation. Once you click the "Start Simulation" button you will not be able to select or move any other sliders except the "Terminate" button which will reset all functiionality. Make sure that you do 1 task at a time because you might run into errors if try to do too many things at once. 

Once the simulation is started you can actually change 2 parameters while the simulation is running. These are the "Temperature" and "Conductivity". The sliders which allow you to change the simulation is shown in this picture below: 

![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Slider_example.png)

Finally, as a side note try not to use a potato pc as it would struggle a lot in trying to run this whole thing for large grids :)

As a closing remark, I hope that what I did here helps people to understand a little bit more about what entropy is and its significance within the natural world. As a said, I'm actually still suspicious on whether or not I implemented the physics correctly and I would be happy to change a part if it turns out to be wrong. Note that I'm not a physics major and I also never took a Statistical Mechanics course. However, I had an idea and I wanted to bring it to life no matter what as the first 22 years felt dissapointing in my mind. Finally, here are some more examples on how things look in version 2 and 1 respectively. 

### Version 2:
Simulation 1 |  Simulation 2 
:-------------------------:|:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/animation_2.gif)  |  ![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/animation_3.gif)

### Version 1:
Simulation 1 |  Simulation 2 
:-------------------------:|:-------------------------:
![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Entropy_alpha%3D89%25.gif)  |  ![](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/GiFs/Entropy_alpha%3D10%25.gif)


For additional information, please see the documents that I have written in [here](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Thoughts.pdf) for version 1 and [here](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Entropy_Computation.pdf) on the method in which I calculated entropy. 

For version 2, please see this [document](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Automata.pdf) for additional information.
