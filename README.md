
## How it works
- Uses [Manim](https://github.com/ManimCommunity/manim)
- Uses images as starting grids
- Currently on version 3
- If you want to know exactly what's going on under the hood, you can read my attempt of using LaTeX in [Automata.pdf](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Automata.pdf)
- The main pipeline is called [Engines.py](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Code/Version_3/Engines.py)
- Manim code is called [Animations.py](https://github.com/ShiroHusin/Entropy_Simulation/blob/main/Code/Version_3/Animations.py)

https://user-images.githubusercontent.com/122879756/232184406-4249c91a-0053-4005-9a03-944d7b5fdc7a.mp4

### Cookbook Recipe 

1. Download an Image you like in Google Images and save it.

2. An image is a 2 dimensional grid stacked 3 times, take one of these stacks. 

3. To reduce computational demand, alter the range from 0-255 to 0-N where $0 \leq N \leq 32$ and the dimensions to a reasonable amount maybe 500x900 max. 

4. Apply a Cellular automata rule iteratively for K epochs. 
   - Indentify all the non zero cells and randomize their locations
   - For each non zero cell, if a uniform distribution $U \sim (0,1)$  is less than move probability $\alpha$ do something, else skip that cell
   - Now check the moore neighborhood of each non zero cell 
   - Compute the transition probabilities according to boltzmann factors and partision functions 
   - Move a quanta of energy from the cell in question to a cell that was chosen 
   - Repeat the steps above for all the non zero cells 
   - Update the entire grid configuration for 1 iteration. 
   
5.  To compute entropy, apply a convolution like technique that checks the state of a small section of the grid via a 2x2 kernel. 
    - The energy of the 2x2 kernel can range from 0 to $a+b+c+d = \phi$ where $a,b,c,d$ is each entry of the 2x2 matrix. 
    - For each of these integer energy levels, find the number of integer combinations possible from the 4 entries of the 2x2 matrix
    - In other words find integers $a, b, c, d$ such that $a + b + c + d = \phi$. Use recursion and store this in a dictionary. 
    - For each epoch $K$, use a strides function that checks the grid configuration's energy so that entropy is not double counted. 
    - Once all the energy states is identified, match it to the dictionary through its keys. 
    - Take the log of each of the mappings and sum it up, this is entropy for 1 datapoint 
    - Do this in conjuction with step 4.

6. To speed up the functions, use a MSG/spice like ingredient called numba and call @njit on functions 4 and 5. 

7. Call upon a plotting library like matplotlib animations to run it and see the results. 

8. If you like to upgrade the visualisation, call upon Manim to help. Store the grid configurations and entropy on an npy file

9. On your new environment, open the npy file and run the Manim simulation. 
   - Call upon the ImageMobject for Manim. 
   - Apply a mapping function from matplotlib to color code each cell's value to a designated RGB value. 
   - Use the Graph Mobject from manim and Dot Mobject and VGroups to add the points iteratively 
   - Call upon the self.play() method and take care to do the programming precisely to rid yourself of bugs.   
   - Within self.play() use the FadeIn, FadeOut or Transform methods on a fast run_time to switch between ImageMobjects and add points
   - Run the code and enjoy : ) 

    
