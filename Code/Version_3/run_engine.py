paths=[r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\Black_hole_accretion.jpg",
r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\Galaxy_collision.jpg",
r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\Pillars_of_creation.jpg",
r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\quasar.jpg",
r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\Tarantula_Nebula_by_JWST.jpg",
       r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\Andromeda_Galaxy.jpg"]

"""
SETTINGS
"""
SHOW_NON_PRIMES=False ## Show an image of prime numbers
IMAGE_INDEX=0       ## can be an integer or True
SAVE=False         ## Save as a gif file ?
SHOW_IMAGE=False    ## Show the pre-processed image ?
COLLECT=True       ## Collect the data ?
FRAMES=1600
MAX_VAL=16          ## Don't set this too high
MAX_VERT_SIZE=200   ## This is the vertical size of the image
TEMP=0.3
PROB=1              ## The probability that each non zero cell actually transfers energy

from Engines import Automata_Simulation, Microstate_table
from Engines import collect as Collect
import numpy as np

def main(max_vert,max_val,image_index,frame,temp,prob,non_primes,save,show_image=False, collect=False):

    Simulation = Automata_Simulation(False, paths, max_vert, show_image, max_val, image_index, temp, prob)

    if not(show_image):
        Simulation_grid = Simulation.grid
        Microstate = Microstate_table()
        df_microstate = Microstate.get_table(np.max(Simulation_grid))

        Data=Collect(False, paths, max_vert, show_image, max_val, image_index , temp, prob)
        if collect==True:
            grids, primes_grids, entropy_data, density_states = Data.collect_data(df_microstate, frame, collect)
            grids=np.array(grids)
            primes_grids=np.array(primes_grids)
            entropy_data=np.array(entropy_data)
            density_states = np.array(density_states)
            np.save('grids.npy', grids)
            np.save('entropies.npy', entropy_data)
            np.save('density_of_states.npy', density_states)

        elif collect==False:
            if not show_image:
                Animation=Simulation.run_simulation(frame, df_microstate, non_primes, save=save)
            else:
                Simulation = Automata_Simulation(False, paths, max_vert, show_image, max_val, image_index, temp, prob)


if __name__ == "__main__":
    main(MAX_VERT_SIZE, MAX_VAL, IMAGE_INDEX, FRAMES, TEMP, PROB, SHOW_NON_PRIMES, SAVE, show_image=SHOW_IMAGE, collect=COLLECT)

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def check_npy_files():
    # Load the data
    grids = np.load('grids.npy')
    prime_grids = np.load('prime_grids.npy')
    entropies = np.load('entropies.npy')
    density_of_states = np.load('density_of_states.npy')

    # Set up the figure, the axis, and the plot elements we want to animate
    fig, axarr = plt.subplots(2, 2, figsize=(10, 10))
    fig.tight_layout(pad=3.0)

    # Set up the colormaps
    cmap1 = 'plasma'
    cmap2 = 'binary'

    def update(num):
        axarr[0, 0].imshow(grids[num], cmap=cmap1)
        axarr[0, 0].set_title('Grids')

        axarr[0, 1].imshow(prime_grids[num], cmap=cmap2)
        axarr[0, 1].set_title('Prime Grids')

        axarr[1, 0].clear()
        axarr[1, 0].plot(entropies[:num])
        axarr[1, 0].set_title('Entropies')
        axarr[1, 0].set_xlim(0, 100)
        axarr[1, 0].set_ylim(np.min(entropies), np.max(entropies))

        axarr[1, 1].imshow(density_of_states[num], cmap='viridis')
        axarr[1, 1].set_title('Density of States')

    # Call the animator.
    # We're only animating over the range [0, 100] as you specified
    ani = FuncAnimation(fig, update, frames=range(0, 100), blit=False, repeat=False)

    plt.show()

# check_npy_files()
