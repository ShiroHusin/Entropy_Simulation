"""
This file is just to compile all the data so that I can plot a graph
"""
from Automata import DataCollector
import matplotlib.pyplot as plt
data_collector = DataCollector()
alphas = [0.1, 0.2, 0.4, 0.6, 0.8, 1]
length=250
n1_generations = 300
n2_generations = 600
n3_generations = 1000
data_point_per_alpha = 5

df1 = data_collector.collect_data(alphas, n1_generations, data_point_per_alpha,length)
df2=  data_collector.collect_data(alphas, n2_generations, data_point_per_alpha,length)
df3=  data_collector.collect_data(alphas, n3_generations, data_point_per_alpha,length)
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
plt.plot(df1_grouped, label='After 300 generations')
plt.plot(df2_grouped, label='After 600 iterations')
plt.plot(df3_grouped, label='After 1000 iterations')
plt.xlabel('Move probability')
plt.ylabel('Proxy entropy')
plt.title("Entropy evolution for different initial conditions")
plt.legend(loc="lower right")
plt.show()
