#%%
import numpy as np

#%% read input
with open('testinput.txt') as f:
    input = f.read()

# input = input[:-1]
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

# sort disk
left_id = 1
right_id = len(disk)-1

while right_id > 1:
    print(disk)
    
    while disk[right_id]==None:
        right_id -= 1

    right_step_id = right_id
    while disk[right_step_id]==disk[right_id]:

        right_step_id -= 1

    file = disk[right_step_id+1:right_id+1]
    file_len = len(file)
    # print(file)
    
    startover=True
    while startover:       

        while (not disk[left_id]==None) and (left_id<right_step_id):
            
            left_id += 1
        
        left_step_id = left_id
        while (disk[left_step_id]==None) and (left_step_id-left_id <= file_len-1) and (left_step_id<right_step_id):
            
            left_step_id += 1

        print("gap:", left_step_id-left_id+1, "file len:", file_len)
        
        if (left_step_id+1-left_id >= file_len):
            disk[left_id:left_id+file_len] = file
            disk[right_step_id+1:right_id+1] = [None] * (right_id - right_step_id)
            startover=False
            left_id = 1

        elif (left_id>=right_step_id) or (left_step_id>=right_step_id):
            left_id = 1
            startover=False

        else:
            left_id = left_step_id
        
    
        
    
    right_id = right_step_id

disk = [x for x in disk if x is not None]
disk

#%% compute checksum
checksum = 0
for idx, num in enumerate(disk):
    checksum += idx*num

print("checksum:", checksum)

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
    
