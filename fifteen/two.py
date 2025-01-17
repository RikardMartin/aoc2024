"""
def get_state(pos, action, n_steps):
    if ^: state = grid[pos[0]-n_steps, pos[1]]
    elif >: state = grid[pos[0], pos[1]+n_steps]
    ...
    return state

def set_pos(pos, action, n_steps):
    if ^: pos = (pos[0]-n_steps, pos[1])
    elif >: pos = (pos[0], pos[1]+n_steps)
    ...
    return pos
        
cur_pos = indexof(grid==@)
for all actions:
    state = get_state(cur_pos, action, 1)
    
    if state is .:
        cur_pos = set_pos(cur_pos, action, 1)
        grid[cur_pos] = @

    elif state is O:
        let new_state = state
        n = 1
        while new_state != #:
            n += 1
            let new_state = get_state(cur_pos, action, n)
            if it is .:
                new_pos = set_pos(cur_pos, action, n)
                grid[new_pos] = O
                grid[set_pos(cur_pos, action, 1)] = @
                
                break

actions: ^ > v <
outcomes: move, push, nothing

"""
#%% Imports
import numpy as np


# Load data
def read_file_to_numpy_and_string(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract the 2D box array
    box_lines = [line.strip() for line in lines if line.strip() and line.startswith('#')]
    box_array = np.array([list(line) for line in box_lines], dtype=str)

    # Extract the string of ^><v signs
    directions = ''.join(line.strip() for line in lines if set(line.strip()) <= {'^', '>', '<', 'v'})

    return box_array, directions

grid, actions = read_file_to_numpy_and_string('testinput1.txt')
print(grid)

# Helper functions
def get_state(pos, action, n_steps):
    if action=='^': state = grid[pos[0]-n_steps, pos[1]]
    elif action=='>': state = grid[pos[0], pos[1]+n_steps]
    elif action=='v': state = grid[pos[0]+n_steps, pos[1]]
    elif action=='<': state = grid[pos[0], pos[1]-n_steps]

    return state

def set_pos(pos, action, n_steps):
    if action=='^': pos = (pos[0]-n_steps, pos[1])
    elif action=='>': pos = (pos[0], pos[1]+n_steps)
    elif action=='v': pos = (pos[0]+n_steps, pos[1])
    elif action=='<': pos = (pos[0], pos[1]-n_steps)

    return pos


# Process grid
cur_pos = np.where(grid=='@')
for action in actions:
    print(action, end=' ')
    state = get_state(cur_pos, action, 1)
    
    if state=='.':
        grid[cur_pos] = '.'
        cur_pos = set_pos(cur_pos, action, 1)
        grid[cur_pos] = '@'

    elif state=='O':
        n = 1

        while state!='#':
            n += 1
            state = get_state(cur_pos, action, n)

            if state=='.':
                grid[cur_pos] = '.'
                cur_pos = set_pos(cur_pos, action, 1)
                grid[cur_pos] = '@'
                grid[set_pos(cur_pos, action, n-1)] = 'O'

                break

    # print(grid)
print('\n')


# Compute GPS
gps_sum = 0
for iy in range(grid.shape[0]):
    for ix in range(grid.shape[1]):
        if grid[iy, ix]=='O':
            gps_sum += 100 * iy + ix
print("GPS sum:", gps_sum)