import numpy as np
import os

cost_on = 1    #Costo por encender la bomba [Moneda]

def _cost(X):
    sc = (1-int(X[1][1])) * (int(X[0][1])-int(X[2][1])) +\
        (1-int(X[2][1])) * (int(X[3][1])+int(X[1][1])) +\
        int(X[1][1]) * int(X[2][1]) *\
        (int(X[0][1]) * (1-int(X[3][1])) +\
        1 - int(X[0][1]))
        
    return sc
    
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
for i in range(4):
    suma += int(X[i][1])
    
if suma == 4:
    cost = 1
else:   
    cost = _cost(X)

v = np.genfromtxt('proyecto1.lp', float, skip_header=1, usecols=(2, 5, 8, 11), max_rows=1)
z = v[0]*int(X[0][1])+ v[1]*int(X[1][1]) + v[2]*int(X[2][1]) + v[3]*int(X[3][1])
Z = z + (cost_on * cost)

os.system('clear')
print('\n\nEl valor optimo de la función es de \n\nZ =', Z)
print('\nLo que nos indica el gasto mínimo.\n\n')
print('\nDados los siguientes periodos en los cuales'\
        ' la bomba\ndebe de estar encendida o apagada:\n')

for i in range(4):
    if int(X[i][1]) == 0:
        print('periodo ',i,'->',' ','OFF')
    else:
        print('periodo ',i,'->',' ','ON')
    
print('\n\n')
