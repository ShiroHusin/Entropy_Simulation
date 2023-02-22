The goal of the problem is to model a random process.

In version 1 rules of the problem are:
1. A cell within the 2D grid can only take 2 discrete values 1 or 0.

2. The number of 1s within the grid cannot change. This is an analogue of the 1st law of thermodynamics. 

3. An occupied cell (1) can move in a random direction to an empty cell (0) that is 1 unit away. 
   - This means that a 1 surrounded by empty cells has 8 possible outcomes or microstates either it can go up, down, left, right or any of the 4 diagonals.
   - If the 1 is completely surrounded by other 1s it can only stay in its place. 
 
Additional information:
The parameter "move probability" determines the likelyhood that the code responsible for movement will execute for each 1s. 
 - A move probability of 100% means that if it can move it will move. 
 - A move probability of 0% means there is absolutely no movement between each cell. The only choice for the 1 cell is to stay in its place over n iterations. 
 - A move probability of 50% means that half of the time if it can move it will move. Likewise, each of the 1s will stay in place 50% of the time. 

In version 2 the rules of the problem are: 
1. A cell within the 2D grid can take any integer values ranging from 0 to 8.

2. The number of 1s within the grid cannot change. This is an analogue of the 1st law of thermodynamics. 

3. An occupied cell (1-8) transfer its energy to an any cell that is not an 8 within 1 square distance away. 
   - This means that cells containing energy surrounded cells that are not 8s has 8 possible outcomes or 8 ways it can transfer its energy. 
   - - Either it can go up, down, left, right or any of the 4 diagonals.
   - If an 8 cell is completely surrounded by other 8s it can only stay in its place. 
 
Additional information:
The parameter "move probability" determines the likelyhood that the code responsible for movement will execute for each 1s. 
 - A move probability of 100% means that if it can move it will move. 
 - A move probability of 0% means there is absolutely no movement between each cell. The only choice for the 1 cell is to stay in its place over n iterations. 
 - A move probability of 50% means that half of the time if it can move it will move. Likewise, each of the 1s will stay in place 50% of the time. 
