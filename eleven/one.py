#%%
import numpy as np

#%% read input
with open('input.txt') as f:
    input = f.read()

input = input[:-1]
input = np.array(input.split(' '), dtype='int')
input

#%% functions
def process_stone(stone):
    """
    go through conditions and apply appropriate rule
    return array of new stone(s)
    """
    if stone == 0:
        return [1]
     
    elif len(str(stone)) % 2 == 0:
        strstone = str(stone)
        left = strstone[:int(len(strstone)/2)]
        right = strstone[int(len(strstone)/2):]
        # print(int(left), int(right))
        return [int(left), int(right)]

    else:
        return [stone*2024]
    
#%%
def process_array(array):
    """ define new array
        for stone in array:
            call process_stone() and append to new array
        return new array
    """
    new_arr = []
    for stone in array:
        # print("stone:", stone)
        new_arr += process_stone(stone)

    return new_arr
    


#%%% run algorithm
"""
array = input    
for i in range(26): # "blink 25 times"
    array = process_array(array)
print(len(array))
"""
array = input.copy()
for i in range(25):
    array = process_array(array)
    print("array:", array)

print("Number of stones:", len(array))


# %%
