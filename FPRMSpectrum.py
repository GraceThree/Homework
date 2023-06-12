# Analyzes a truth table and decomposes it into the least costly FPRM
# for a function f: {0,1}^n -> {0,1}
# Brute force recursive algorithm
# Author: Grace Unger
# Modified: 6-11-23

import numpy as np
import math
import scipy as sp


#0 -> negative polarity
#1 -> positive polarity
# output in order that comes from truth Karnaugh map
def getSpec(code, table, nums):
    newVec = [0] * len(table)
    newCosts = [0] * len(table)
    half = len(table)//2
    if code[0] == "0":
        for i in range(0, half):
            newVec[i] = table[i] ^ table[i+half]
            newVec[i+half] = table[i+half]
            newCosts[i] = nums[i+half]# ^ costs[i+half] #How to combine these lol
            newCosts[i+half] = nums[i]
    else:
        for i in range(0, half):
            newVec[i] = table[i]
            newVec[i+half] = table[i+half] ^ table[i]
            newCosts[i] = nums[i]
            newCosts[i+half] = nums[i+half] #costs[i++half] ^ costs[i]
    if len(code) == 1:
        return (newVec, newCosts)
    top = getSpec(code[1:], newVec[:half], newCosts[:half]) 
    bottom = getSpec(code[1:], newVec[half:], newCosts[half:])
    return (top[0]+bottom[0], top[1] + bottom[1])

#Manually builds a table vector for boolean function f of n bits
def buildTableVec(f, n):
    tableVec = [0] * 2 ** n
    for i in range(0, 2 ** n):
        s =f'{i:0{n}b}'.format(12)
        if f(s):
            tableVec[i] = 1
    return tableVec
            
def majN(x, n):
    if n%2 == 0: raise Exception("n must be odd for majority function, not {n}.")
    return x.count("1")>=n//2

def prob4B(x):
    [a,b,c,d,e,f] = [int(i) for i in x]
    return a*b*c ^ d*(1^e)*(1^f) ^ (1^a)*(1^b)*c ^ (1^d)*e*f

# truth table built from karnaugh map traversal

#tableVec = [0, 1, 1, 0, 1, 1, 1, 1]
# Sample function this was designed for from Merek's notes

#tableVec = [0, 0, 0, 1, 0, 1, 1, 1]
# Majority function 3x3

#tableVec = buildTableVec(lambda x: majN(x, 5), 5)
# Majority function 5x5

#tableVec = [0, 1, 0, 1, 0, 0, 1, 1]
# ab + a'c

tableVec = buildTableVec(lambda x: prob4B(x), 6)

k = math.log(len(tableVec), 2)
if not k.is_integer():
    raise Exception("vector is not of size 2^n") #only handles boolean ops

k = int(k)
spec = []
code = ""
mincost = 2**k

specRM = []
for i in range(0, 2 ** k):
    RMTerms = range(0,2 ** k)
    s = f'{i:0{k}b}'.format(12)
    [specS, RMTerms] = getSpec(s,tableVec, RMTerms)
    numTerms = list(map(lambda x: f'{x:0{k}b}'.count("1"), RMTerms))
    numTerms = list(map(lambda x: max(2 ** x - 3, 1 ), numTerms))
    cost = np.dot(numTerms, specS) + s.count("0") #Cost based on 2^n-3 for an n x n toffoli gate, so NOT and CNOT are identical! Neat!
    if cost<mincost or (cost == mincost and specS.count(1)<spec.count(1)):
        mincost = cost
        spec = specS
        code = s 
        specRM = RMTerms

print(f"Spectrum: {spec}\nHas minimal cost: {mincost}\nAnd comes from polarity: {code}")

temp = np.multiply(spec, specRM)
temp = list(filter(lambda x: x>0, temp))
temp = list(map(lambda x: f'{x:0{k}b}'.format(12), temp))
print(f"The FPRM expression is given by:\n{' + '.join(temp)}")
print("\n")

funcVec = []
for i in temp:
    s = ""
    curChr = 97
    for j in range(0, k):
        if i[j] == "1":
            if code[j] == "1":
                s += chr(curChr)
            else:
                s += chr(curChr) + "'"
        curChr+=1
    funcVec += [s]

print("This translates to:")
print(f'{chr(0x2295)} '.join(funcVec))
print()

