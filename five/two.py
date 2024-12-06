#%%
import numpy as np

#%%

with open('input.txt') as f:
    data = f.read()

data = str(data.split('\n')).split("\'\'")
data

#%% rules
rules = data[0]
rules = eval(rules[:-2]+']')

rulebook = []
for entry in rules:
    k, v = entry.split('|')
    rulebook.append((int(k), int(v)))

rulebook

#%% updates
#updates = eval('[['+data[1][2:].replace(', ', '], [').replace('\'', '')+']')
updates = eval('[['+data[1][2:].replace(', ', '], [')[:-3].replace('\'', '')+']')
updates

#%%
wrong = []

for update in updates:
    violation=False

    for rule in rulebook:
        for i in range(len(update)):
            
            if update[i]==rule[0]:
                for j in range(i):
                    if update[j]==rule[1]:
                        violation=True
                        break
            
            if violation: break
        if violation: break
    
    if violation:
        wrong.append(update)

wrong

#%% correct order
"""
for update in wrong:
    end = len(update)-1
    for element in update[:end]:
        while element is wrong wrt to next element, until end-i'th element:
            flip pair
        end -= 1
    """

def is_wrong(left, right):
    for rule in rulebook:
        if (left==rule[1]) and (right==rule[0]):
            return True


for update in wrong:
    print("---")
    print(update)

    length = len(update)-1
    end = length
    for j in range(length):
        i = 0
        while i<end:

            left, right = update[i], update[i+1]
            if is_wrong(left, right):
                tmp = left
                update[i] = right
                update[i+1] = tmp
            
            i += 1
        
        end -= 1

    print(update)


#%%
page_sum = 0
for list in wrong:
    center = int(len(list)/2)
    page_sum += list[center]

page_sum
# %%
