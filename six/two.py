#%%
import numpy as np

#%% load input

input = []
with open('testinput.txt') as f:
    for line in f:
        print(line)
    
        row = []
        for c in line[:-1]:
            row.append(c)
        input.append(row)

input = np.array(input)
input = input.T

#%% traverse map
def outside(pos):
    if (pos[1][0] < 0) or (pos[0][0] < 0) or (pos[0][0] >= input.shape[0]) or (pos[1][0] >= input.shape[1]):
        return True

    return False

def take_step(dir, pos):
    match dir:

        case '^':
            step = (pos[0], pos[1] - 1)
            if outside(step):
                return True, step, dir
            else:
                symbol = input[step]
                if symbol == '#':
                    step = (pos[0] + 1, pos[1])
                    dir = '>'

                return False, step, dir

        case '>':
            step = (pos[0] + 1, pos[1])
            if outside(step):
                return True, step, dir
            
            else:
                symbol = input[step]
                if symbol == '#':
                    step = (pos[0], pos[1] + 1)
                    dir = 'v'

                return False, step, dir

        case 'v':
            step = (pos[0], pos[1] + 1)
            if outside(step):
                return True, step, dir
            
            else:
                symbol = input[step]
                if symbol == '#':
                    step = (pos[0] - 1, pos[1])
                    dir = '<'

                return False, step, dir
            
        case '<':
            step = (pos[0] - 1, pos[1])
            if outside(step):
                return True, step, dir
            
            else:
                symbol = input[step]
                if symbol == '#':
                    step = (pos[0], pos[1] - 1)
                    dir = '^'

                return False, step, dir
            
        case _:
            print('error matching position to direction')


#%% sätt ut hinder
loops = []

for x in range(input.shape[0]):
    for y in range(input.shape[1]):
        original = input[x,y]
        input[x,y] = '#'

        visited = np.zeros(input.shape, dtype='int')
        directions = np.zeros(input.shape, dtype='str')
        position = np.where(input=='^')
        dir = '^'
        out = False

        print(dir, ' : ', position, ' : ', out)
        while not out:
            
            out, position, dir = take_step(dir, position)
            print(dir, ' : ', position, ' : ', out)
            if not out:
                if (directions[position] == dir) and (visited[position] == 1):
                    loops.append((x,y))
                    input[x,y] = original
                    break
                    
                visited[position] = 1
                directions[position] = dir


# %%
