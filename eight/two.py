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
matrix = np.empty( (len_y, len_x), dtype='str')

for idy in range(len_y):
    for idx in range(len_x):
        # print(idx,idy)
        matrix[idy, idx] = data[idy][idx]

print(matrix)
print(matrix.shape)
#%% find antinodes
"""
let dx and dy be the number of steps, in each direction, between the two nodes
if the first node coords - (dy, dx) are positive:
    place an antinode and add this tuple to list of returnvalues
if the second node coorde + (dy, dx) are within matrix limits:
    place an antinode and add this tuple to list of returnvalues
"""
def get_antinode_coords(first, second):
    result = []
    dy = second[0] - first[0]
    dx = second[1] - first[1]
    
    node1 = (first[0], first[1])
    while (node1[0] >= 0) and (node1[1] >= 0) and (node1[1] < len_x):
        result.append(node1)
        node1 = (node1[0]-dy, node1[1]-dx)
    
    node2 = (second[0], second[1])
    while (node2[0] < len_y) and (node2[1] >= 0) and (node2[1] < len_x):
        result.append(node2)
        node2 = (node2[0]+dy, node2[1]+dx)
    
    return result

def insert_antinodes(antimap, nodes):
    for node in nodes:
        # print("new node at:", node)
        antimap[node] = 1



# %% go through pussle
"""
define empty matrix for antinodes

for each column:
    for each row:
        if current cell is not a '.':
            record symbol
            for each column starting from current:
                for each row starting from current:
                    if cell matches symbol:
                        compute antinodes and store in antinode-matrix

"""
antimap = np.zeros( (len_y, len_x), dtype='int')

for y in range(len_y):
    for x in range(len_x):

        symbol = matrix[y,x]
        if symbol != '.':
            print("current symbol:", symbol, 'at: (', y,x,')')
            first_row = True
            for i in range(y,len_y):
                
                if first_row:
                    start_x = x+1
                    first_row = False
                else:
                    start_x = 0
                for j in range(start_x,len_x):
        
                    if matrix[i,j]==symbol:
                        # print("match at: (", i,j,')')
                        antinodes = get_antinode_coords((y,x), (i,j))
                        insert_antinodes(antimap, antinodes)

# %% compute result
print("Number of antinode locations:", antimap.sum())
antimap

# %%
