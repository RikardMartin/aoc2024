#%%
import numpy as np
"""
Load all positions and velocities to a list.

For each robot:
    Get the starting position.
    Add to its position its velocity multiplied by the number of seconds and save as destination.
    Divide the x-destination by the length of the grid and save the remainder.
    Set its x-endpoint as the remainder.
    Do the same but for the y-axis.

Find the median in x and y on the "grid".
For all endpoints:
    If y is less than med-y:
        If x is less than med-x:
            count +1 in first quadrant.
        elif x is more than med-x:
            count +1 in second quadrant.
    elif Y is more than med-y:
        If x is less than med-x:
            count +1 in third quadrant.
        elif x is more than med-x:
            count +1 in fourth quadrant.

multiply the four quadrant numbers together.
"""
#%% Parameters
len_x = 101 #101
len_y = 103 #103
path = 'input.txt'
n_sec = 100

#%% Load data
robots = []
with open(path) as f:
    for line in f:
        line = line.split(' ')
        print(line)

        pos = line[0].split('=')[1].split(',')
        pos[0] = int(pos[0])
        pos[1] = int(pos[1])

        vel = line[1].split('=')[1].split(',')
        vel[0] = int(vel[0])
        vel[1] = int(vel[1])

        print(vel)

        robots.append({'pos': np.array(pos), 'vel': np.array(vel)})

robots

#%% Compute final positions
for robot in robots:
    # print("pos:", robot['pos'])
    end = robot['pos']+robot['vel']*n_sec
    # print("end:", end)

    robot['end'] = [end[0]%len_x, end[1]%len_y]
    print("dest:", robot['end'])

#%% Compute safety factor
med_x = int(len_x/2)
med_y = int(len_y/2)
print("medians:", med_x, med_y)

nw, ne, se, sw = 0, 0, 0, 0
for robot in robots:
    x, y =robot['end'][0], robot['end'][1]
    # print(x,y)

    if y < med_y:
        if x < med_x:
            nw += 1
        elif x > med_x:
            ne += 1
    elif y > med_y:
        if x < med_x:
            sw += 1
        elif x > med_x:
            se += 1

result = nw*ne*sw*se
print("safety factor:", result)


# %%
