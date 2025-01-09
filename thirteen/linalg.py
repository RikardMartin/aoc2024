#%%
import numpy as np

machines = []
with open('input.txt') as inp:
    for line in inp:

        A = line.split(':')[1].lstrip().split(', ')
        A = [int(A[0][2:]), int(A[1][2:-1])] 
        # print(A)
        
        bline = inp.readline()
        B = bline.split(':')[1].lstrip().split(', ')
        B = [int(B[0][2:]), int(B[1][2:-1])]
        # print(B)

        pline = inp.readline()
        P = pline.split(':')[1].lstrip().split(', ')
        P = [int(P[0][2:]), int(P[1][2:-1])]
        # print(P)

        T = np.array([A,B]).T
        # print(AB)

        entry = {}
        entry['T'] = T
        # entry['A'] = A
        # entry['B'] = B
        entry['P'] = np.array(P)
        machines.append(entry)

        empty = inp.readline()

machines
#%%
"""
(t11,t12)(nA)=(X)
(t21,t22)(nB)=(Y)

(2x2)*(2x1)=(2x1)

(94,22)(nA)=8400
(34,67)(nB)=5400
"""

def is_integer(floatvalue, tol):
    return floatvalue - int(floatvalue) < tol

total_tokens = 0
tol = 0.000000000000001
for machine in machines:

    steps = np.dot(np.linalg.inv(machine['T']), machine['P'])
    # print(steps, is_integer(steps[0], tol), is_integer(steps[1], tol))

    
    
    if (0 <= steps[0] < 101) and (0 <= steps[1] < 101) and is_integer(steps[0], tol) and is_integer(steps[1], tol):
        tokens = 3*steps[0] + steps[1]
        print("Steps:", steps, " | Tokens:", tokens)
        total_tokens += tokens

print("Total tokens:", total_tokens)

#%%

