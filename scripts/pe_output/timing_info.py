import sys
import numpy as np
import pandas as pd

hour=int(sys.argv[1])
final=int(sys.argv[2])

df = pd.read_csv('timestep_times.txt',index_col='Timestep')
df = df.drop([1,hour,final])

mean = df.mean(axis=0)
median = df.median(axis=0)
min = df.min(axis=0)
max = df.max(axis=0)

print("Mean: ", format(mean[0],".3f")) 
print("Median: ", format(median[0],".3f")) 
print("Min: ", format(min[0],".3f")) 
print("Max: ", format(max[0],".3f")) 
