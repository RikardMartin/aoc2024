#%%
import numpy as np

#%% load input

input = []
with open('input.txt') as f:
    for line in f:
    
        row = []
        for c in line[:-1]:
            row.append(c)
        input.append(row)

input = np.array(input)
print(input)
#%% traverse map

def take_step(dir, pos):
    match dir:

        case '^':
            step = (pos[0]-1, pos[1])
            if step[0][0] < 0:
                return True, step, dir
            else:
                if input[step] == '#':
                    step = (pos[0], pos[1])
                    dir = '>'

                return False, step, dir

        case '>':
            step = (pos[0], pos[1]+1)
            if step[1][0] >= input.shape[1]:
                return True, step, dir
            
            else:
                if input[step] == '#':
                    step = (pos[0], pos[1])
                    dir = 'v'

                return False, step, dir

        case 'v':
            step = (pos[0]+1, pos[1])
            if step[0][0] >= input.shape[0]:
                return True, step, dir
            
            else:
                if input[step] == '#':
                    step = (pos[0], pos[1])
                    dir = '<'

                return False, step, dir
            
        case '<':
            step = (pos[0], pos[1]-1)
            if step[1][0] < 0:
                return True, step, dir
            
            else:
                if input[step] == '#':
                    step = (pos[0], pos[1])
                    dir = '^'

                return False, step, dir
            
        case _:
            print('error matching position to direction')


#%% sätt ut hinder
loops = []
start_pos = np.where(input=='^')
start_dir = '^'

total_n = input.shape[0]*input.shape[1]
for x in range(0, input.shape[0]):
    for y in range(0, input.shape[1]):

        # progress = int(100*(x+1)*(y+1)/total_n)
        if y % 10 == 0:
            print("progress", x, y)
        
        original = input[x,y]
        if (original == '.'):
            input[x,y] = '#'

        visited = np.zeros(input.shape, dtype='int')
        visited[start_pos] = 1
        directions = np.zeros(input.shape, dtype='str')
        directions[start_pos] = start_dir
        out = False

        position = start_pos
        dir = start_dir
        # print(dir, ' : ', position, ' : ', out)
        i = 0
        while not out:
            out, position, dir = take_step(dir, position)
            # print(dir, ' : ', position, ' : ', out)
            i += 1
            if not out:
                if (directions[position] == dir) and (visited[position] == 1):
                    loops.append((x,y))
                    break
                if i > total_n:
                    loops.append((x,y))
                    break
                    
                visited[position] = 1
                directions[position] = dir
            
        input[x,y] = original

print(loops)
print("numer of loops:", len(loops))
# print(visited.sum())
# print(visited)
# %%
