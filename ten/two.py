#%%
import numpy as np

#%%
with open('input.txt') as f:
    data = f.readlines()

data = [line[:-1] for line in data]
data
# %%
len_x = len(data[0])
max_x = len_x - 1
len_y = len(data)
max_y = len_y - 1
matrix = np.empty( (len_y, len_x), dtype=int)

for idy in range(len_y):
    for idx in range(len_x):
        # print(idx,idy)
        matrix[idy, idx] = data[idy][idx]

print(matrix)
print(matrix.shape)
#%% functions
"""
def get_possible_directions((x,y)):
    check if each dir is possible, and return the possible ones
"""
def get_possible_directions(pos):
    directions = []
    
    if pos[0] > 0: directions.append((pos[0]-1, pos[1])) # up
    if pos[0] < max_y: directions.append((pos[0]+1, pos[1])) # down
    if pos[1] > 0: directions.append((pos[0], pos[1]-1)) # left
    if pos[1] < max_x: directions.append((pos[0], pos[1]+1)) # right

    return directions
   
"""
def find_paths((x,y))
    if matrix[x,y]==9:
        return 1
    
    directions = get_possible_directions(x,y)
    for dir in directions:
        if matrix[dir] - matrix[(x,y)] == 1:
            return num_paths(direction)   
"""
def find_paths(pos):
    total_paths = 0
    if matrix[pos]==9:
        if visited[pos]==0:
            # print("reached goal at", pos)
            visited[pos] = 1
            return 1
    
    else:
        directions = get_possible_directions(pos)
        # print("found", directions)
        for dir in directions:
            if matrix[dir] - matrix[pos] == 1:
                # print("going to", dir)
                # print(dir, '-', pos, '=', matrix[dir]-matrix[pos])
                total_paths += find_paths(dir)

    # print("paths so far:", total_paths)
    return total_paths

#%% algorithm
print(matrix)
"""
for each trailhead in matrix:
    num_paths += find_path(trailhead_coords)
"""
sum_of_scores = 0

y, x = np.where(matrix==0)
# y = y[[0]]
# x = x[[0]]
test = 0
for idy, idx in zip(y,x):
    print("starting at", (idy, idx))

    visited = np.zeros( (len_y, len_x), dtype=int)
    num_paths = 0
    num_paths = find_paths((idy,idx))
    print("found paths:", num_paths)

    sum_of_scores += num_paths

print("sum of scores:", sum_of_scores)


# %%
