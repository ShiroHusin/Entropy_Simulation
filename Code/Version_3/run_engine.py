paths=[r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\Black_hole_accretion.jpg",
r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\Galaxy_collision.jpg",
r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\Pillars_of_creation.jpg",
r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\quasar.jpg",
r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\Tarantula_Nebula_by_JWST.jpg",
       r"C:\Users\Bowen\PycharmProjects\Entropy_Game\PNGs\Andromeda_Galaxy.jpg"]

"""
SETTINGS
"""
SHOW_NON_PRIMES=True
IMAGE_INDEX=0       ## can be an integer or True
SAVE=False
SHOW_IMAGE=False
FRAMES=1600
MAX_VAL=16
MAX_VERT_SIZE=300
TEMP=0.4
PROB=1

from Engines import Automata_Simulation, Microstate_table
from Engines import collect as Collect
import numpy as np
# import matplotlib.pyplot as plt

def main(max_vert,max_val,image_index,frame,temp,prob,non_primes,save,show_image=False, collect=False):
    Simulation = Automata_Simulation(False, paths, max_vert, show_image, max_val, image_index, temp, prob)
    Simulation_grid = Simulation.grid
    Microstate = Microstate_table()
    df_microstate = Microstate.get_table(np.max(Simulation_grid), False)

    Data=Collect(False, paths, max_vert, show_image, max_val, image_index , temp, prob)
    if collect==True:
        grids, primes_grids, entropy_data = Data.collect_data(df_microstate, frame, collect)
        grids=np.array(grids)
        primes_grids=np.array(primes_grids)
        entropy_data=np.array(entropy_data)
        np.save('grids.npy', grids)
        np.save('prime_grids.npy', primes_grids)
        np.save('entropies.npy', entropy_data)

    elif collect==False:
        if not show_image:

            Animation=Simulation.run_simulation(frame, df_microstate, non_primes, save=save)
        else:
            Simulation = Automata_Simulation(False, paths, max_vert, show_image, max_val, image_index, temp, prob)
if __name__ == "__main__":
    main(MAX_VERT_SIZE, MAX_VAL, IMAGE_INDEX, FRAMES, TEMP, PROB, SHOW_NON_PRIMES, SAVE, SHOW_IMAGE,collect=True)
