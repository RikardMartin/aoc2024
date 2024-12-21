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


def blink(array, blinks):
    if blinks == 75:
        # n_stones = len(array)
        # print("nblinks:", blinks)
        return len(array)

    blinks += 1
    total_stones = 0
    for stone in array:
        new_arr = process_stone(stone)
        n_stone = blink(new_arr, blinks)
        total_stones += n_stone
        # print("len(arr):", len(new_arr), " | n_stone:", n_stone, " | total_stones:", total_stones)

    return total_stones

# run algorithm
"""
"""
array = input.copy()
# n_stones = 0
blinks = 0
stones = blink(array, blinks)

print("Number of stones:", stones)


# %%
