#%%
import numpy as np
from collections import defaultdict


#%%
with open('testinput.txt') as f:
    data = f.readlines()

data = [line[:-1] for line in data]
data

len_x = len(data[0])+2
max_x = len_x - 1
len_y = len(data)+2
max_y = len_y - 1
matrix = np.empty( (len_y, len_x), dtype='str')
# plants = set()

for idy in range(1,len_y-1):
    for idx in range(1,len_x-1):
        # print(idx,idy)
        matrix[idy, idx] = data[idy-1][idx-1]
        # plants.add(data[idy-1][idx-1])
# matrix[1:-1,1:-1] = data

print(matrix)
print(matrix.shape)
# print(plants)
#%%
def find_region(iy, ix, symbol, pruned_garden, direction=None):
    global area, perimeter, coords
    """
    """
    # print("checking node", (iy, ix), "for symbol", symbol, "with area as", area)
    if pruned_garden[iy, ix]==symbol:
        area += 1
        pruned_garden[iy, ix] = ''
        coords.add((iy, ix))
        
        # print("found plant", symbol, "at", (iy, ix), "with area", area, "and perimeter", perimeter)

        find_region(iy, ix+1, symbol, pruned_garden, direction='right')
        find_region(iy+1, ix, symbol, pruned_garden, direction='down')
        find_region(iy, ix-1, symbol, pruned_garden, direction='left')
        find_region(iy-1, ix, symbol, pruned_garden, direction='up')


def get_boundary_nodes(coords):
    """
    Takes in a list of coordinate pairs (y, x) and returns the boundary nodes.

    Args:
        coords (list of tuples): List of coordinate pairs representing the area.

    Returns:
        list of tuples: Boundary nodes of the area.
    """
    # Convert the list of coordinates to a set for O(1) lookups
    # coord_set = set(coords)

    # Define possible neighbors (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    boundary_nodes = []

    for y, x in coords:
        # Check if the current node has all neighbors in the set
        for dy, dx in directions:
            neighbor = (y + dy, x + dx)
            if neighbor not in coords:
                boundary_nodes.append((y, x))
                break  # No need to check further if it's a boundary node
    
    boundary_nodes.sort()

    return boundary_nodes


def find_perimeter():
    """
    # This handles inside boundary edges
    walk through region matrix. row by row from left to right
        if current node is not symbol, continue.
        at current point, for each direction that doesnt have symbol in it.
            if right or left:
                if up is symbol, mark direction as perimeter
            if up or down:
                if left is symbol, mark that direction as perimeter.
        else continue.

    # This handles outside boundary edges
    start at first region node
    walk left if it is inside region
    else walk forward if it is inside region
    else walk right if it is inside region
    else walk back
    record node as outside boundary node
    record direction we walked at
    use direction to take next step acording to left,straight,right,back-rule
    break when we arrive at first node

    for each boundary node.
        increment perimeter if we change direction, e.g. we now increase or decrease y, but last node decreased x.
    """
    pass


pruned_garden = matrix.copy()
total_price = 0

for idy in range(1,len_y-1):
    for idx in range(1,len_x-1):

        area = 0
        coords = set()
        symbol = pruned_garden[idy, idx]
        if symbol!='':
            find_region(idy, idx, symbol, pruned_garden)
            perimeter = find_perimeter(coords)

            total_price += area*perimeter
            print("plant:", symbol, ", area:", area, ", perimeter:", perimeter)


print("total price:", total_price)
# %%
