#%%
import numpy as np
from itertools import chain

machines = []
price_offset = 10000000000000
with open('testinput.txt') as inp:
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
        P = [p+price_offset for p in P]
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

def is_integer(floatvalue, tol):
    res = abs(floatvalue - int(floatvalue))
    # print(f"Residual: {res:.10f}")

    if (res < tol) or (1-res < tol):
        return True
    return False
    return floatvalue.is_integer()

def solve_iter(machine):
    longest_step = (machine['T']).max()
    limit = int(price_offset/(longest_step*2))
    for n1 in chain([0], range(price_offset-, limit+101)):
        for n2 in chain([0], range(limit, limit+101)):
            N = np.array([n1, n2])
            if np.array_equal(np.dot(machine['T'], N), machine['P']):
                return N
    return None

def solve(machine):
    N = np.dot(np.linalg.inv(machine['T']), machine['P'])
    return N

total_tokens = 0
tol = 0.0001
disc_range = chain([0], range(price_offset, price_offset+101))
for machine in machines:
    steps = solve_iter(machine)

    if steps is not None:
        print(f"Steps: ({steps[0]:.10f}, {steps[1]:.10f})", is_integer(steps[0], tol), is_integer(steps[1], tol))

        # if (0 <= steps[0]) and (0 <= steps[1]) and is_integer(steps[0], tol) and is_integer(steps[1], tol):
            # tokens = 3*steps[0] + steps[1]
            # print(f"Steps: ({steps[0]:.10f}, {steps[1]:.10f})", f"Tokens: {tokens}")
            # total_tokens += tokens


    else: print("Steps is None")

print("Total tokens:", total_tokens)

#%%

