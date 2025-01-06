#%%
import numpy as np
# from collections import defaultdict


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
    global area, coords
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

def get_next_outer_boundary_node(node, dir):
    """
    start at first region node
    walk left if it is inside region
    else walk forward if it is inside region
    else walk right if it is inside region
    else walk back
    record node as outside boundary node
    record direction we walked at
    use direction to take next step acording to left,straight,right,back-rule
    break when we arrive at first node
    """
    if dir=='right':
        if (node[0]-1, node[1]) in coords:
            node = (node[0]-1, node[1])
            dir = 'up'
        elif (node[0], node[1]+1) in coords:
            node = (node[0], node[1]+1)
            dir = 'right'
        elif (node[0]+1, node[1]) in coords:
            node = (node[0]+1, node[1])
            dir = 'down'
        elif (node[0], node[1]-1) in coords:
            node = (node[0], node[1]-1)
            dir = 'left'
        else:
            dir = None
    
    elif dir=='up':
        if (node[0], node[1]-1) in coords:
            node = (node[0], node[1]-1)
            dir = 'left'
        elif (node[0]-1, node[1]) in coords:
            node = (node[0]-1, node[1])
            dir = 'up'
        elif (node[0], node[1]+1) in coords:
            node = (node[0], node[1]+1)
            dir = 'right'
        elif (node[0]+1, node[1]) in coords:
            node = (node[0]+1, node[1])
            dir = 'down'    
        else:
            dir = None
        
    elif dir=='down':
        if (node[0], node[1]+1) in coords:
            node = (node[0], node[1]+1)
            dir = 'right'
        elif (node[0]+1, node[1]) in coords:
            node = (node[0]+1, node[1])
            dir = 'down'
        elif (node[0], node[1]-1) in coords:
            node = (node[0], node[1]-1)
            dir = 'left'
        elif (node[0]-1, node[1]) in coords:
            node = (node[0]-1, node[1])
            dir = 'up'
        else:
            dir = None
    
    elif dir=='left':
        if (node[0]+1, node[1]) in coords:
            node = (node[0]+1, node[1])
            dir = 'down'
        elif (node[0], node[1]-1) in coords:
            node = (node[0], node[1]-1)
            dir = 'left'
        elif (node[0]-1, node[1]) in coords:
            node = (node[0]-1, node[1])
            dir = 'up'
        elif (node[0], node[1]+1) in coords:
            node = (node[0], node[1]+1)
            dir = 'right'
        else:
            dir = None
    
    return node, dir

def find_outer_boundary(list_of_coords):
    node = list_of_coords[0]
    dir = 'right'
    outer_boundary = []
    
    while True:
        outer_boundary.append(node)
        node, dir = get_next_outer_boundary_node(node, dir)
        if node==list_of_coords[0]:
            break
    
    return outer_boundary

def find_perimeter(list_of_coords):
    # This handles inside boundary edges
    """
    walk through region matrix. row by row from left to right
        if current node is not symbol, continue.
        at current point, for each direction that doesnt have symbol in it.
            if right or left:
                if up is symbol, mark direction as perimeter
            if up or down:
                if left is symbol, mark that direction as perimeter.
        else continue.
    """
    inner_perimeter = 0

    # This handles outside boundary edges
    """
    get all boundary nodes.
    for each boundary node.
        increment perimeter if we change direction, e.g. we now increase or decrease y, but last node decreased x.
    """
    outer_boundary = find_outer_boundary(list_of_coords)
    outer_perimeter = 0
    print(outer_boundary)
    
    if len(outer_boundary) > 1:
        first = outer_boundary[0]
        second = outer_boundary[1]
        if first[0] != second[0]: direction = 'y'
        elif first[1] != second[1]: direction = 'x'
        outer_perimeter += 1
        outer_boundary.append(outer_boundary[0])

        for ix in range(len(outer_boundary)-1):
            this = outer_boundary[ix]
            next = outer_boundary[ix+1]
            # print('direction', direction)
            # print(this, '->', next)

            if (direction == 'x') and (next[0] != this[0]):
                    outer_perimeter += 1
                    direction = 'y'
                    # print("going y")
            elif (direction == 'y') and (next[1] != this[1]):
                    outer_perimeter += 1
                    direction = 'x'
                    # print("going x")

    else:
        outer_perimeter = 4


    return inner_perimeter + outer_perimeter


# Main algorithm
pruned_garden = matrix.copy()
total_price = 0

for idy in range(1,len_y-1):
    for idx in range(1,len_x-1):

        area = 0
        coords = set()
        symbol = pruned_garden[idy, idx]
        if symbol!='':
            find_region(idy, idx, symbol, pruned_garden)
            perimeter = find_perimeter(list(coords))

            total_price += area*perimeter
            print("plant:", symbol, ", area:", area, ", perimeter:", perimeter)


print("total price:", total_price)
# %%
