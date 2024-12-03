# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# %%
with open('input.txt') as f:
    input = f.read()

input
#%%
"""
Find the indices of each do and don't
For each dont-index:
    find the distance to the next do-index
    cut those indices out of the string
Run the original algorithm on the new string
"""
def find_matches(input, pattern):
    matches = re.finditer(pattern, input)
    matches = [(match.group(), match.start(), match.end()) for match in matches]
    return matches
   
# hej_input = "hej sa ja te daj, ja hej hEj precis så hejdå 1s"
# hej_pattern = r'hej'
# hejs = find_matches(hej_input, hej_pattern)
# hejs

dos = find_matches(input, r'do\(\)')
donts = find_matches(input, r"don't\(\)")

#%%
new_input = input
last_do_idx = 0
for dont_match in donts:
    print("--- New dont ---")
    current_dont_idx = dont_match[1]
    # print(current_dont_idx)

    for do_match in dos:
        current_do_idx = do_match[2]
        # print(current_do_idx)

        if current_do_idx > current_dont_idx:
            # print(input)

            to_remove = input[current_dont_idx:current_do_idx]
            print(len(to_remove))

            new_input = new_input.replace(to_remove, "")
            last_do_idx += 1
            # print(new_input)

            print("------------ end --------------", len(new_input))
            break
            






# %%
pattern = r'mul\(\d{1,3},\d{1,3}\)'

matches = re.findall(pattern, new_input)
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
