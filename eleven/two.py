#%%
import numpy as np

#%% read input
with open('testinput.txt') as f:
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


def blink(array, blinks, n_stones):
    """
    for each stone in array:
        new_arr = process_stone(stone)
        process(new_arr)
    """
    print("len(array):", len(array))
    if blinks < 6:
        blinks += 1
        for stone in array:
            new_arr = process_stone(stone)
            return blink(new_arr, blinks, len(new_arr))

    else:
        
        return blinks, len(array)

#%%% run algorithm
"""
"""
array = input.copy()
blinks, n_stones = blink(array, 0, len(array))

print("Number of blinks:", blinks, ' | n_stones:', n_stones)


# %%
