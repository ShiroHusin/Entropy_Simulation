In version 2 the rules of the problem are: 
1. A cell within the 2D grid can take any integer values ranging from 0 to 8.

2. The summation of numbers within the grid cannot change. This is an analogue of the 1st law of thermodynamics. 

3. An occupied cell (1-8) transfer its energy to an any cell that is not an 8 within 1 square distance away. 
   - This means that cells containing energy surrounded cells that are not 8s has 8 possible outcomes or 8 ways it can transfer its energy. It can go up, down, left, right or any of the 4 diagonals.
   - If an 8 cell is completely surrounded by other 8s it can only stay in its place. 
 
Additional information:
The parameter "move probability" determines the likelyhood that the code responsible for movement will execute for each 1s. 
 - A move probability of 100% means that if it can transfer energy it will. 
 - A move probability of 0% means there is absolutely no chance of cells transferring its energy to its neighbours.  
 - A move probability of 50% means that half of the time the code responsible for executing energy movement is executed. 
 - In version 2, conductivity is related to "move probability" through a function. If the grid is highly conductive, there is a near 100% chance that the code responsible for moving energy is executed. 

There is also a new parameter called Temperature. In this simulation, the grid is extremely sensitive to temperature changes as I removed the boltzmann constant. 
 - The probability and direction in which it transfers energy in the 8 neighbours depends on each of the cells' energy state. 
 - For example, if the cell in question is a 7 surrounded by cells of value {1,4,2,3,5,7,6,0}, energy from the 7 cell will overwhelmingly transfer itself to a 0 cell, followed by the 1 cell and the 2 cell.   
 - Each of the direction vector's associated probability are altered and calculated trough the use of the boltzmann factor where temperature plays a huge role in altering the probabilities. 
 - If temperature is very high, the simulation becomes insensitive towards differences between energy levels and all the direction vectors are approximately equal.
