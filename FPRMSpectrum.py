# Analyzes a truth table and decomposes it into the least costly FPRM
# Tracks the cost table as well
# Brute force recursive algorithm
# Author: Grace Unger
# Modifier: 6-11-23

import numpy as np
import math
import scipy as sp


#0 -> negative polarity
#1 -> positive polarity
# output in order that comes from truth Karnaugh map
def getSpec(code, table, costs):
    newVec = [0] * len(table)
    newCosts = [0] * len(table)
    half = len(table)//2
    if code[0] == "0":
        for i in range(0, half):
            newVec[i] = table[i] ^ table[i+half]
            newVec[i+half] = table[i+half]
            newCosts[i] = costs[i+half]# ^ costs[i+half] #How to combine these lol
            newCosts[i+half] = costs[i]
    else:
        for i in range(0, half):
            newVec[i] = table[i]
            newVec[i+half] = table[i+half] ^ table[i]
            newCosts[i] = costs[i]
            newCosts[i+half] = costs[i+half] #costs[i++half] ^ costs[i]
    if len(code) == 1:
        return (newVec, newCosts)
    top = getSpec(code[1:], newVec[:half], newCosts[:half]) 
    bottom = getSpec(code[1:], newVec[half:], newCosts[half:])
    return (top[0]+bottom[0], top[1] + bottom[1])

# truth table built from karnaugh map traversal
#Future addition: add way to input an arbitrary K-map and generate this vector

# tableVec = [0, 1, 1, 0, 1, 1, 1, 1
# Sample function this was designed for from Merek's notes

tableVec = [0, 0, 0, 1, 0, 1, 1, 1]
# Majority function

k = math.log(len(tableVec), 2)
if not k.is_integer():
    raise Exception("vector is not of size 2^n") #only handles boolean ops

k = int(k)
spec = []
code = ""
mincost = 2**k

for i in range(0, 2 ** k):
    costs = [0, 1, 1, 2, 1, 2, 2, 3] #For now, hardcoded to only work with 3 variables, but will extend :)
    s = f'{i:0{k}b}'.format(12)
    [specS, costs] = getSpec(s,tableVec, costs)
    cost = np.dot(costs, specS)
    print()
    print(s)
    print(specS)
    print(costs)
    print(f"cost is {cost}")
    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print()
    if cost<mincost or (cost == mincost and specS.count(1)<spec.count(1)):
        mincost = cost
        spec = specS
        code = s 

print(f"Spectrum: {spec}\nHas minimal cost: {mincost}\nAnd comes from polarity: {code}")