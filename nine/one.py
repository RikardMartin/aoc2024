#%%
import numpy as np

#%% read input
with open('input.txt') as f:
    input = f.read()

input = input[:-1]
input
    
#%% build disk
disk = []
id = 0
for idx in range(0, len(input)-1, 2):
    # print("id:", id, "idx:", idx)
    disk.extend([id]*int(input[idx]))
    disk.extend([None]*int(input[idx+1]))
    id += 1

if len(input)%2:
    disk.extend([id]*int(input[-1]))

disk

#%% sort disk
left_id = 0
right_id = len(disk)-1
while left_id <= right_id:

    left = disk[left_id]
    while left!=None:
        left_id += 1
        left = disk[left_id]

    right = disk[right_id]
    while right==None:
        right_id -= 1
        right = disk[right_id]

    disk[left_id] = right
    disk[right_id] = None

disk = [x for x in disk if x is not None]
disk
    
#%% compute checksum
checksum = 0
for idx, num in enumerate(disk):
    checksum += idx*num

print("checksum:", checksum)
