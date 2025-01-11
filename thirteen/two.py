#%%
import numpy as np
from math import isclose

machines = []
price_offset = 10000000000000
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

def solve(machine):
    N = np.dot(np.linalg.inv(machine['T']), machine['P'])
    N = np.round(N).astype(int)

    if (N[0] >= 0) and (N[1] >= 0):
        if np.array_equal(np.dot(machine['T'], N), machine['P']):
            return N.astype(int)

    return None

total_tokens = 0
tol = 0.000001
for machine in machines:
    steps = solve(machine)

    if steps is not None:
        # print(f"Steps: ({steps[0]:.10f}, {steps[1]:.10f})", is_integer(steps[0], tol), is_integer(steps[1], tol))

        # if (0 <= steps[0]) and (0 <= steps[1]) and is_integer(steps[0], tol) and is_integer(steps[1], tol):
        # if isclose(round(steps[0]), steps[0], rel_tol=0, abs_tol=1e-4) and isclose(round(steps[1]), steps[1], rel_tol=0, abs_tol=1e-4):
        tokens = 3*steps[0] + steps[1]
        print(f"Steps: ({steps[0]:.1f}, {steps[1]:.1f})", f"Tokens: {tokens}")
        total_tokens += tokens


    else: print("Steps is None")

print("Total tokens:", total_tokens)

#%%
machine = machines[0]

C = np.array([price_offset, price_offset])
N = np.dot(np.linalg.inv(machine['T']), C)

for n1 in range(N[0]):
        for n2 in range(101):
            N = np.array([n1, n2])
            C = np.array([price_offset, price_offset])
            prod = np.dot(machine['T'], N) - C
            if np.array_equal(prod, machine['P']):

# %%
