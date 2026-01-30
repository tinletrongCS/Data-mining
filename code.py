import pandas as pd 
import numpy as np 
path = "jewelry.csv"
dataset = pd.read_csv(path)
print(dataset.shape)
print(dataset.head(5))