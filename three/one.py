# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
input = np.array([[7, 6, 4, 2, 1],
[1, 2, 7, 8, 9],
[9, 7, 6, 2, 1],
[1, 3, 2, 4, 5],
[8, 6, 4, 4, 1],
[1, 3, 6, 7, 9]])

# %%
with open('input.txt') as f:
    lines = f.readlines()

array_of_lines = [np.array(list(map(int, line.split()))) for line in lines]
input = np.array(array_of_lines, dtype=object)

# %%
input[0]

# %%

