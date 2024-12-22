#%%
import numpy as np
from multiprocessing import Manager, Process

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
    if stone in stonemap:
        return stonemap[stone]
    else:
        if stone == 0:
            stonemap[stone] = [1]
            return stonemap[stone]
        
        elif len(str(stone)) % 2 == 0:
            strstone = str(stone)
            left = strstone[:int(len(strstone)/2)]
            right = strstone[int(len(strstone)/2):]
            stonemap[stone] = [int(left), int(right)]
            return stonemap[stone]

        else:
            stonemap[stone] = [int(stone*2024)]
            return stonemap[stone]

from functools import lru_cache
import json

@lru_cache(maxsize=None)  # Cache unlimited results
def memoized_blink(array_json, blinks):
    array = json.loads(array_json)  # Convert back to Python list
    if blinks == 75:
        return len(array)

    blinks += 1
    total_stones = 0
    for stone in array:
        new_arr = process_stone(stone)
        total_stones += memoized_blink(json.dumps(new_arr), blinks)  # Convert to JSON for hashable input

    return total_stones


def blink(array, blinks, return_dict, process_id):
    if blinks == 75:
        return_dict[process_id] = len(array)
        return

    blinks += 1
    total_stones = 0
    for stone in array:
        new_arr = process_stone(stone)
        total_stones += memoized_blink(json.dumps(new_arr), blinks)
    
    return_dict[process_id] = total_stones


# Main function to parallelize
def parallel_blink(input_array):
    manager = Manager()
    return_dict = manager.dict()

    processes = []
    for i, stone in enumerate(input_array):
        process = Process(target=blink, args=([stone], 0, return_dict, i))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    # Aggregate results from all processes
    return sum(return_dict.values())


# run algorithm
"""
"""
stonemap = {}
progress = 0
# n_stones = 0
blinks = 0
stones = parallel_blink(input)

print("\nNumber of stones:", stones)
