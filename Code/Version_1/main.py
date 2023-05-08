"""
This file is to run Automata.py; the file that houses the entire script
"""

import Automata
from Automata import initialize_grid

def main():
    ## Prompts the questions
    questions = Automata.Questions()
    length = questions.get_length()
    choice = questions.get_shape()
    alpha = questions.get_alpha()
    no_of_frames = questions.get_frames()
    ## Initialise all the necessary initial conditions
    grid, test_grid, alpha, no_of_frames,n = initialize_grid(length, choice, alpha, no_of_frames)
    ## Runs the simulation
    animation = Automata.AutomataSimulation(grid, alpha, no_of_frames, length=n)
    # Uncomment this line if you want to save this animation.
    # animation.save_animation("Entropy.gif")

## Runs Automata.py
if __name__ == "__main__":
    main()


