import sys
import numpy as np
from fractions import Fraction
import argparse as parse

def incrementedTableu(table, m, n):
    b = np.hsplit(table, int(n))
    b = b[int(n)-1]
    table = np.hsplit(table, np.array( [int(m)-1,int(n)]) )
    table = table[0]
    identity = np.vstack( (np.zeros( (1, int(n)-1) ), np.identity( int(m)-1 )) )
    identity_b = np.hstack ( [identity, b] )
    tableu = np.hstack( (table, identity_b) ) #tableu[:] = np.hstack( [table, np.identity(int(n) ])

    return tableu
    
def writeTableu(tableu, n, mess):
    header = mess + ' ' + int(9*n)*'_' + '\n'
    footer = int(12*n) * '-' + '\n'
    for row in tableu:
            np.savetxt('output.txt', tableu, fmt='%5s',\
            header=header, footer=footer)

    return

def opt_test(Z_vect):
    for test in Z_vect:
        if test < 0:
            return False
    
    return True

def eta_vect(tableu, eta_col, m, n):
       eta = np.stack( for row in tableu: tableu[row][int(eta_col)] )
        

def find_pivot(tableu, m, n):
    t = opt_test(tableu[0])
    if t == True:
        return 0 # MUST CHANGE THIS FOR A FINALIZATION ROUTINE
    
    table = tableu[0]
    table = table[:-1]
    col = np.argmin(table)  
    i = True
    for row in range(1, int(m), 1):
        #print('\niteration ',row, '\n')
        buffer = tableu[row][int(col)]
        #print('buff = ', buffer)
        b = tableu[row][int(n)-1]
        #print('b = ',b)
        if (buffer > 0):
            buff_test = b / buffer
            #print('buffer test = ', buff_test)
            if i == True:
                p = buffer
                #print('p =', p)
                test = buff_test
                #print('test = ', test)
            elif buff_test < test:
                #print(buff_test, '<', test)
                p = buffer
                #print('Now:\np = ',p)
                test = buff_test
                #print('test = ', test)
            i = False              
    
    eta_vect(tableu, col, m, n)
    return p

table = np.ndarray( (20,20) )

table = np.loadtxt("file.txt", dtype=float, comments='#', delimiter=" ")
m = table[0][0]
n = table[1][0]
table = table[2:]
tableu = incrementedTableu(table, m, n)

writeTableu(tableu, n, "\nIteration 0")

n = (n-1) + m #Now m has the incremented tableu size, not the original
pivot = find_pivot(tableu, m, n)
if pivot == 0:
    sys.exit('Z is optimal')

while pivot =! 0:
#size = np.fromfile("file.txt", dtype = float, count = 2, sep = " ")
#tableu = np.fromfile("file.txt", dtype = float, count = -1, sep = " ")
#tableu = tableu[2:]
