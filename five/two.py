#%%
import numpy as np

#%%

with open('testinput.txt') as f:
    data = f.read()

data = str(data.split('\n')).split("\'\'")
data
# %%
"""
def add_deps(basekey, rule):
    if not rule.value in all_rules[basekey]: add rule.value to values

    for new_rule in list where new_rule.key equals rule.value:
        add_deps(basekey, new_rule)


Add all rule-keys to dict as keys
For each rule in rules:
    add_deps(rule.key, rule)

"""

#%% rules
rules = data[0]
rules = eval(rules[:-2]+']')

rulebook = []
for entry in rules:
    k, v = entry.split('|')
    rulebook.append((int(k), int(v)))

rulebook

#%% updates
updates = eval('[['+data[1][2:].replace(', ', '], [').replace('\'', '')+']')
# updates = eval('[['+data[1][2:].replace(', ', '], [')[:-3].replace('\'', '')+']')
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


#%%
page_sum = 0
for list in correct:
    center = int(len(list)/2)
    page_sum += list[center]

page_sum
# %%
