#%%
from itertools import permutations, product

#%%
calibration_result = 0

def mul(test, i):
    test[i+1] = test[i] * test[i+1]
    # print(test[i+1], '=', test[i], '*', test[i+1])
    return test

def add(test, i):
    test[i+1] = test[i] + test[i+1]
    # print(test[i+1], '=', test[i], '+', test[i+1])
    return test

def evaluate(answer, test):
    repeats = len(test)-1
    perms = [p for p in product([add, mul], repeat=repeats)]
    # print(perms)  
    for perm in perms:
        result = [n for n in test]
        for i in range(repeats):
            result = perm[i](result, i)
            # print('result:', result[-1])
        if result[-1]==answer:
            return True
        
with open('input.txt') as f:
    for line in f:
        
        answer, test = line.split(':')
        answer = int(answer)
        
        test = test.strip().split(' ')
        test = [int(x) for x in test]
        # print(test)

        result = evaluate(answer, test)
        print('final:', result, answer)
        if result:
            calibration_result += answer


print(calibration_result)



    