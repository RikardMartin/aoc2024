#%%
import numpy as np

#%%
with open('input.txt') as f:
    data = f.readlines()

data = [line[:-1] for line in data]
data
# %%
len_x = len(data[0])
len_y = len(data)
matrix = np.empty( (len_y, len_x), dtype=int)

for idy in range(len_y):
    for idx in range(len_x):
        # print(idx,idy)
        matrix[idy, idx] = data[idy][idx]

print(matrix)
print(matrix.shape)

#%% algorithm
"""
for each trailhead in matrix:
    num_paths += find_path(trailhead_coords)

    
def get_possible_directions((x,y)):
    check if each dir is possible, and return the possible ones

def find_paths((x,y))
    if matrix[x,y]==9:
        return 1
    
    directions = get_possible_directions(x,y):
    for dir in directions:
        if matrix[dir] - matrix[(x,y)] == 1:
            return num_paths(direction)    

"""
