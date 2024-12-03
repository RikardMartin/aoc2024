# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# %%
with open('input.txt') as f:
    input = f.read()

input

# %%
pattern = r'mul\(\d{1,3},\d{1,3}\)'

matches = re.findall(pattern, input)
print(matches)

#%%
def multiply(task):
    nums = task[4:-1].split(',')
    res = int(nums[0])*int(nums[1])
    return res


#%%
sum = 0
for task in matches:
    prod = multiply(task)
    sum += prod
    print(task, multiply(task))

print(sum)

# %%
