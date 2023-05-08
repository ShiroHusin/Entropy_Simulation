"""
This is a standardized method to collect data the grid is of length=100 and uses the circle method.
"""
## Multiple ways to collect datas using classes.
## If you want to collect 2D data use either data_entropy_2D_C or data_entropy_2D_T
## If u want a 2D plot use plot_entropy_2D to within Data_collector class to plot
"""
For data_entropy_2D_C. Input your temperatures as a numpy array and choose how many data points you want and how many 
iterations of the grid you need. Obviously be reasonable with these numbers and don't go crazy as they will take forever. 
"""
"""
For data_entropy_2D_T. Input your conductivities as a numpy array and again choose the data points you want, iterations. 
The plot will be a 2D plot where Temperatures are the X axis, entropy the Y axis for different set Conductivities. 
"""
from Engine import DataCollector
import numpy as np

## Placeholder values
T_arr=np.array([0.1, 0.5, 1, 2, 4, 6])
C_arr=np.array([10, 50, 100, 500, 2000, 6000])

## Change the input values here
conductivities=6
temps=6
iterations=20
data_points=5

datas=DataCollector(conductivities,temps,iterations,data_points)
Conductivities,Temperatures,Entropies=datas.data_entropy_3D()

## If you want a 3D plot call the method plot_entropy_3D
figure=datas.plot_entropy_3D(Conductivities,Temperatures,Entropies)

