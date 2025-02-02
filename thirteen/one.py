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

def is_integer(floatvalue, tol):
    return floatvalue - int(floatvalue) < tol

def solve(machine):
    for n1 in range(101):
        for n2 in range(101):
            N = np.array([n1, n2])
            if np.array_equal(np.dot(machine['T'], N), machine['P']):
                return N
    return None

total_tokens = 0
tol = 10000000000
for machine in machines:

    
    steps = solve(machine)
    if steps is not None:
        # print(steps) #, is_integer(steps[0], tol), is_integer(steps[1], tol))


        
        
        # if (-100 <= steps[0] < 1001) and (-1000 <= steps[1] < 10001) and is_integer(steps[0], tol) and is_integer(steps[1], tol):
        tokens = 3*steps[0] + steps[1]
        print("Steps:", steps, " | Tokens:", tokens)
        total_tokens += tokens

print("Total tokens:", total_tokens)

#%%

