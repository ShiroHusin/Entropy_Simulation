
## Version 3 in the works
- Uses [Manim](https://github.com/ManimCommunity/manim)
- Uses images as starting grids
- Currently on version 2

https://user-images.githubusercontent.com/122879756/232184406-4249c91a-0053-4005-9a03-944d7b5fdc7a.mp4

## For entertainment purposes, here is a rap poem I made

```py
"""
To understand, we'll need to discern
With microstates, our foundation's firm
lets us consider a game of coins 
by employing a tree with its lines conjoined 
List the paths as shown below 
By highlighting the routes, we'd like to know 
Microstates, these routes are 
Revealing the premises that was barred 

But the sea is vast that there is more to know 
The macrostate that I've yet to show 
Bring the table back to the stage 
Classifying them by the heads they make
Take the log of the microstate 
Compute the entropy for boltzmann's sake 

The example's lame, you might say 
Just scale the game and let it play
Now you'll see what's at stake 
Billions of ways per macrostate 
Now imagine this with all your mates 
A system in motion with random states
Which is likelier you should query 
All heads or Tails or mixed uniformly 
Lets bring back the main equation 
and see the states that matches the occasion
Now you see why entropy grows 
as there is more routes for it to flow

The second law is a thing of beauty 
yet its a fate that awaits us many
For eternity the law will reign 
As in existence itself it is deeply ingrained.
"""
```

### Cookbook Recipe 

1. Download an Image you like in Google Images and save it.

2. An image is a 2 dimensional grid stacked 3 times, take one of these stacks. 

3. To reduce computational demand, alter the range from 0-255 to 0-N where $0 \leq N \leq 32$.

4. Apply a Cellular automata rule iteratively for K epochs. 
   - Indentify all the non zero cells and randomize their locations
   - For each non zero cell, if a uniform distribution $U \sim \text{Uniform}(0,1)$  is less than move probability $\alpha$ then 
     - 
