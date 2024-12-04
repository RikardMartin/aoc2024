#%%
import numpy as np

#%%

with open('input.txt') as f:
    data = f.readlines()

data
# %%
data = [line[:-1] for line in data]
data
# %%
len_x = len(data[0])
len_y = len(data)
matrix = np.empty( (len_y, len_x), dtype='str')

for idy in range(len_y):
    for idx in range(len_x):
        # print(idx,idy)
        matrix[idy, idx] = data[idy][idx]

print(matrix)
print(matrix.shape)

#%% along rows
xmas_count = 0

for idy in range(len_y):
    for idx in range(len_x-3):
        # print(matrix[idx][idy:idy+4])
        word = ''.join(c for c in matrix[idy][idx:idx+4])
        if word in ['SAMX', 'XMAS']:
            print(idy, idx, word)
            xmas_count += 1

#%% along diagonal /
max_len = len_y + len_x - 4
x, y = np.meshgrid(np.arange(0,len_y,1), np.arange(0,len_x,1))

for idag in range(3, max_len):
    diag = matrix[x + y == idag]
    # print('diag:', diag)

    for idx in range(len(diag)-3):
        # print(diag[idx:idx+4])
        word = ''.join(c for c in diag[idx:idx+4])
        # print(word)
        if word in ['SAMX', 'XMAS']:
            print(idx, word)
            xmas_count += 1

#%% along diagonal \

for idag in range(4-len_y, len_x-4):
    diag = matrix[x - y == idag]
    # print('diag:', diag)

    for idx in range(len(diag)-3):
        # print(diag[idx:idx+4])
        word = ''.join(c for c in diag[idx:idx+4])
        # print(word)
        if word in ['SAMX', 'XMAS']:
            print(idx, word)
            xmas_count += 1

#%% along columns
matrix = matrix.T
len_x = len(data)
len_y = len(data[0])

for idy in range(len_y):
    for idx in range(len_x-3):
        # print(matrix[idx][idy:idy+4])
        word = ''.join(c for c in matrix[idy][idx:idx+4])
        if word in ['SAMX', 'XMAS']:
            print(idy, idx, word)
            xmas_count += 1





# %%
xmas_count