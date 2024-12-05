#%%
import numpy as np

#%%

with open('testinput.txt') as f:
    data = f.read()

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
#%%
data = str(data.split('\n')).split("\'\'")
rules = data[0]
rules = eval(rules[:-2]+']')
updates = data[1]

#%%
rulebook = []
keys = set()
for entry in rules:
    k, v = entry.split('|')
    rulebook.append({int(k): [int(v)]})
    keys.add(int(k))

all_rules = {key: [] for key in keys}
rulebook

#%%


def add_deps(basekey, rule):
    for item in rule.items():
        for value in item[1]:
            if not value in all_rules[basekey]:
                all_rules[basekey].append(value)
                
    pass


for rule in rulebook:
    for item in rule.items():
         for value in item[1]:
             print(value)
            # if not value in rulebook[basekey]:
                # rulebook[basekey].append(value) 


# %%
