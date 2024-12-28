#%%
import numpy as np

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
    global area, perimeter
    """
    """
    # print("checking node", (iy, ix), "for symbol", symbol, "with area as", area)
    if pruned_garden[iy, ix]==symbol:
        area += 1
        pruned_garden[iy, ix] = ''
        perimeter += find_perimeter(iy, ix, symbol, direction=direction)
        
        # print("found plant", symbol, "at", (iy, ix), "with area", area, "and perimeter", perimeter)

        find_region(iy, ix+1, symbol, pruned_garden, direction='right')
        find_region(iy+1, ix, symbol, pruned_garden, direction='down')
        find_region(iy, ix-1, symbol, pruned_garden, direction='left')
        find_region(iy-1, ix, symbol, pruned_garden, direction='up')

def find_perimeter(iy, ix, symbol, direction=None):
    perimeter = 0

    if direction=='down':
        if matrix[iy+1, ix]!=symbol: perimeter += 1
    elif direction=='up':
        if matrix[iy-1, ix]!=symbol: perimeter += 1
    elif direction=='right':
        if matrix[iy, ix+1]!=symbol: perimeter += 1
    elif direction=='left':
        if matrix[iy, ix-1]!=symbol: perimeter += 1
    
    else:
        if matrix[iy+1, ix]!=symbol: perimeter += 1
        if matrix[iy-1, ix]!=symbol: perimeter += 1
        if matrix[iy, ix+1]!=symbol: perimeter += 1
        if matrix[iy, ix-1]!=symbol: perimeter += 1
    

    return perimeter


pruned_garden = matrix.copy()
total_price = 0

for idy in range(1,len_y-1):
    for idx in range(1,len_x-1):

        area = 0
        perimeter = 0
        symbol = pruned_garden[idy, idx]
        if symbol!='':
            find_region(idy, idx, symbol, pruned_garden)

            total_price += area*perimeter
            print("plant:", symbol, ", area:", area, ", perimeter:", perimeter)


print("total price:", total_price)
# %%
