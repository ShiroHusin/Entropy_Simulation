import Automata
from Automata import initialize_grid

def main():
    questions = Automata.Questions()
    length = questions.get_length()
    choice = questions.get_shape()
    alpha = questions.get_alpha()
    no_of_frames = questions.get_frames()
    grid, test_grid, alpha, no_of_frames,n = initialize_grid(length, choice, alpha, no_of_frames)
    Automata.AutomataSimulation(grid, alpha, no_of_frames,length=n)

if __name__ == "__main__":
    main()
  
