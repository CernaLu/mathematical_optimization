import sys
import numpy as np
from fractions import Fraction
import argparse as parse

# It's important not to stay in an infinit cycle that could
    # happen if there are repeated pivots. Code should be
    # able to identify and pick the next pivot, even if it
    # has the same value

# Also, it is of importance 

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
    #for row in tableu:
    np.savetxt('output.txt', tableu, fmt='%5s',\
    header=header, footer=footer)

    return

def opt_test(Z_vect):
    for test in Z_vect:
        if test < 0:
            return False
    
    return True

def pivot(tableu, m, n, col, p_row):
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
                p_row = row
            elif buff_test < test:
                #print(buff_test, '<', test)
                p = buffer
                #print('Now:\np = ',p)
                test = buff_test
                #print('test = ', test)
                p_row = row
            i = False

    return p
    
def eta_vect(tableu, m, n, p_row, col, p):
    eta_.ndarray( (4,1) )
    for row in range(int(m))
        if row == int(p_row):
            a = int(tableu[row][int(col)])
            eta_[int(row)] = p**(-1)
        else:
            a = int(tableu[row][int(col)])
            eta_[int(row)] = ( a ) / (- p)

    return
    
def Simplex(tableu, m, n):
    t = opt_test(tableu[0])
    if t == True:
        return 0 # MUST CHANGE THIS FOR A FINALIZATION ROUTINE
    
    p_row = 0 # If it stays a 0, then no pivot was found
    col = 0
    p_value = pivot(tableu, m, n, p_row, col)
    eta_vect(tableu, m, n, p_row, col, p_value)
    
    
    
    return

################################## MAIN PROGRAM
table = np.ndarray( (20,20) )

table = np.loadtxt("file.txt", dtype=float, comments='#', delimiter=" ")
m = table[0][0]
n = table[1][0]
table = table[2:]
tableu = incrementedTableu(table, m, n)

writeTableu(tableu, n, "\nIteration 0")

n = (n-1) + m #Now n has the incremented tableu size, not the original

Simplex(tableu, m, n)

#size = np.fromfile("file.txt", dtype = float, count = 2, sep = " ")
#tableu = np.fromfile("file.txt", dtype = float, count = -1, sep = " ")
#tableu = tableu[2:]
