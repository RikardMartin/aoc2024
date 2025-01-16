#%%
import numpy as np
import pandas as pd
"""
Load all positions and velocities to a list.

For each robot:
    Get the starting position.
    Add to its position its velocity multiplied by the number of seconds and save as destination.
    Divide the x-destination by the length of the grid and save the remainder.
    Set its x-endpoint as the remainder.
    Do the same but for the y-axis.

Find the median in x and y on the "grid".
For all endpoints:
    If y is less than med-y:
        If x is less than med-x:
            count +1 in first quadrant.
        elif x is more than med-x:
            count +1 in second quadrant.
    elif Y is more than med-y:
        If x is less than med-x:
            count +1 in third quadrant.
        elif x is more than med-x:
            count +1 in fourth quadrant.

multiply the four quadrant numbers together.
"""
#%% Parameters
len_x = 101
len_y = 103
path = 'input.txt'

#%% Load data
robots = []
with open(path) as f:
    for line in f:
        line = line.split(' ')
        print(line)

        pos = line[0].split('=')[1].split(',')
        pos[0] = int(pos[0])
        pos[1] = int(pos[1])

        vel = line[1].split('=')[1].split(',')
        vel[0] = int(vel[0])
        vel[1] = int(vel[1])

        # print(vel)

        robots.append({'pos': np.array(pos), 'vel': np.array(vel)})

robots

#%% functions
def connected_component_lengths(matrix):
    """
    Finds the lengths of connected components (loops) in a binary matrix.
    Components can include horizontal, vertical, and diagonal connections.
    
    Parameters:
        matrix (np.ndarray): A 2D binary matrix (containing only 0s and 1s).
    
    Returns:
        list: A list of lengths of all connected components (loops) in the matrix.
    """
    # Define directions for horizontal, vertical, and diagonal movements
    directions = [
        (-1, 0), (1, 0),  # Vertical
        (0, -1), (0, 1),  # Horizontal
        (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
    ]
    
    def is_valid(x, y):
        """Check if the position (x, y) is valid and contains a 1."""
        return 0 <= x < rows and 0 <= y < cols and not visited[x, y] and matrix[x, y] == 1
    
    def dfs(x, y):
        """Perform Depth First Search to find all connected cells."""
        stack = [(x, y)]
        length = 0
        while stack:
            cx, cy = stack.pop()
            if visited[cx, cy]:
                continue
            visited[cx, cy] = True
            length += 1
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if is_valid(nx, ny):
                    stack.append((nx, ny))
        return length

    # Initialize visited matrix
    rows, cols = matrix.shape
    visited = np.zeros_like(matrix, dtype=bool)
    
    # Find all connected components
    component_lengths = []
    for i in range(rows):
        for j in range(cols):
            if matrix[i, j] == 1 and not visited[i, j]:
                # Start a new connected component search
                component_length = dfs(i, j)
                component_lengths.append(component_length)
    
    return component_lengths
#%% Find christmas tree

lengths = []
max_length = 1
for sec in range(100, 10000):
    grid = np.zeros((len_y, len_x))
    for robot in robots:
        end = robot['pos'] + robot['vel']*sec
        end = [end[0]%len_x, end[1]%len_y]
        grid[end[1], end[0]] = 1

    length = max(connected_component_lengths(grid))
    if length > max_length: max_length = length
    lengths.append([sec, length])

print("max length:", max_length)

#%% print(lengths)
for length in lengths:
    if length[1] > max_length*0.9:

        grid = np.zeros((len_y, len_x))
        for robot in robots:
            end = robot['pos'] + robot['vel']*length[0]
            end = [end[0]%len_x, end[1]%len_y]
            grid[end[1], end[0]] = 1
        
        print("sec:", length[0])
        df = pd.DataFrame(grid)
        print(df.to_string(index=False, header=False))
        print('---------------------')


#%%

    

    

#%% Compute safety factor
med_x = int(len_x/2)
med_y = int(len_y/2)
print("medians:", med_x, med_y)

nw, ne, se, sw = 0, 0, 0, 0
for robot in robots:
    x, y =robot['end'][0], robot['end'][1]
    # print(x,y)

    if y < med_y:
        if x < med_x:
            nw += 1
        elif x > med_x:
            ne += 1
    elif y > med_y:
        if x < med_x:
            sw += 1
        elif x > med_x:
            se += 1

result = nw*ne*sw*se
print("safety factor:", result)

