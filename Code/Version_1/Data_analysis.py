"""
This file is just to compile all the data so that I can plot a graph
Note: This script takes quite a while to run. Its meant to be that way.
"""
from Automata import DataCollector
import numpy as np
import matplotlib.pyplot as plt
data_collector = DataCollector()
alphas=np.arange(0.05,1.05,0.05)
n1_generations = 300
n2_generations = 600
n3_generations = 1000
data_point_per_alpha = 5

df1 = data_collector.collect_data(alphas, n1_generations, data_point_per_alpha,length=250)
df2=  data_collector.collect_data(alphas, n2_generations, data_point_per_alpha,length=250)
df3=  data_collector.collect_data(alphas, n3_generations, data_point_per_alpha,length=250)
#
# ## Group the dataframe find the averages and the standard deviation for the final plot
df1_grouped = df1.groupby('alpha')['xor_result'].mean()
df1_std = df1.groupby('alpha')['xor_result'].std()

## Group the 2nd dataframe
df2_grouped = df2.groupby('alpha')['xor_result'].mean()
df2_std = df2.groupby('alpha')['xor_result'].std()

## Group the 3rd dataframe
df3_grouped = df3.groupby('alpha')['xor_result'].mean()
df3_std = df3.groupby('alpha')['xor_result'].std()

## Plot the graphs
plt.plot(df1_grouped, label='After 300 iterations')
plt.plot(df2_grouped, label='After 600 iterations')
plt.plot(df3_grouped, label='After 1000 iterations')
plt.xlabel('Move probability')
plt.ylabel('Proxy entropy')
plt.title("Entropy evolution for different initial conditions")
plt.legend(loc="lower right")
plt.show()
