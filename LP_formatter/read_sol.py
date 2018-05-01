import numpy as np
import os

def values(X):
    v = np.genfromtxt('sol.txt', str, usecols=0)
    for n in v:
        if n == 'x1':
            X[0][1] = 1
        if n == 'x2':
            X[1][1] = 1
        if n == 'x3':
            X[2][1] = 1
        if n == 'x4':
            X[3][1] = 1
        
    return

X = np.chararray( (4,2), 2, unicode=True )
i=0
for n in range(4):
    X[n][i] = 'x'+str(n+1)
    X[n][i+1] = 0

suma = 0
values(X)

with open('sol.txt',"r") as f:
    all_data=[x.split() for x in f.readlines()]
    a=array([map(float,x) for x in all_data[:N]])
    b=array([map(int,x) for x in all_data[N+1:]])

print (a)
print (b)

os.system('clear')

