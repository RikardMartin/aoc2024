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

# sort disk
left_id = 1
right_id = len(disk)-1

while right_id > 1:
    print(right_id)
    
    while disk[right_id]==None:
        right_id -= 1

    right_step_id = right_id
    while disk[right_step_id]==disk[right_id]:

        right_step_id -= 1

    file = disk[right_step_id+1:right_id+1]
    file_len = len(file)
    # print("File:", file)
    
    startover=True
    while startover:
        # print("startover at left_id:", left_id)   

        while (not disk[left_id]==None) and (left_id<=right_step_id):
            
            left_id += 1
        
        left_step_id = left_id
        while (disk[left_step_id]==None) and (left_step_id<=right_step_id):
            
            left_step_id += 1

        # print("gap:", left_step_id-left_id, "file len:", file_len, "disk content:", disk[left_id:left_id+file_len])
        
        if (left_step_id-left_id >= file_len):
            disk[left_id:left_id+file_len] = file
            disk[right_step_id+1:right_id+1] = [None] * (right_id - right_step_id)
            startover=False
            left_id = 1
            # print("File written:", file)

        elif (left_id>=right_step_id) or (left_step_id>=right_step_id):
            left_id = 1
            startover=False
            # print("Reached right_step_id:", right_step_id)

        else:
            left_id = left_step_id
            # print("continue search for left_id")
        
    
        
    
    right_id = right_step_id
    # print("step right_id to:", right_id)

# disk = [x for x in disk if x is not None]
disk

# compute checksum
checksum = 0
for idx, num in enumerate(disk):
    if num:
        checksum += idx*num

print("checksum:", checksum)

