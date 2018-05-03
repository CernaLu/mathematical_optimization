import sys
import numpy as np
from fractions import Fraction
import argparse as parse
import os
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
    dst = open('output.txt', 'a')
    np.savetxt(dst, tableu, fmt='%5s', header=header, footer=footer)
    
    #np.savetxt(dst, tableu, fmt='%5s', header=header, footer=footer)
    #dst = open('output.txt', 'ab')
    #dst.writelines( [header, '\n', tableu, '\n', footer] ) #fmt='%5s'
    dst.close() 
    return

def opt_test(Z_vect):
    for test in Z_vect:
        if test < 0:
            return False
    
    return True

def pivot(tableu, m, n):
    table = tableu[0]
    table = table[:-1]
    p_col = np.argmin(table)  
    i = True
    for row in range(1, int(m), 1):
        #print('\niteration ',row, '\n')
        buffer = tableu[row][int(p_col)]
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
    
    return p, p_row, p_col
    
def eta_vect(tableu, m, n, p, p_row, p_col):
    etav = np.ndarray()
    etav = etav.astype('object')
    for row in range(int(m)):
        if row == int(p_row):
            a = int(tableu[row][int(p_col)])
            etav[row] = Fraction(1, int(p))
        else:
            a = int(tableu[row][int(p_col)])
            #etav[int(row)] = ( a ) / (- p)
            etav[row] = Fraction(a, int(-p) )

    print (etav)
    return etav

def eta_tableu(etaV, p_col, m):
    etaM = np.identity( int(m) )
    for row in range(int(m)):
        etaM[row][int(p_col)] = etaV[row]
    
    return etaM

def Simplex(tableu, m, n, etav):
    #change etav declaration to this location
    t = opt_test(tableu[0])
    if t == True:
        return 0 # MUST CHANGE THIS FOR A FINALIZATION ROUTINE
    
    p = pivot(tableu, m, n)
    etaV = eta_vect(tableu, m, n, p[0], p[1], p[2]) #gives eta as a row

    etaM = eta_tableu(etaV, p[2], m)
    #print(etaM)
    T = np.matmul(etaM, tableu)
    writeTableu(etaM, n, 'eta Tableu')
    writeTableu(T, n, 'Iteration 1')
    
    return

################################## MAIN PROGRAM
os.system('> output.txt')
table = np.ndarray( (20,20) )

table = np.loadtxt("file.txt", dtype=float, comments='#', delimiter=" ")
m = table[0][0]
n = table[1][0]
table = table[2:]
tableu = incrementedTableu(table, m, n)
etav = np.ndarray( 4 )

writeTableu(tableu, n, "\nIteration 0")

n = (n-1) + m #Now n has the incremented tableu size, not the original

Simplex(tableu, m, n, etav)

#size = np.fromfile("file.txt", dtype = float, count = 2, sep = " ")
#tableu = np.fromfile("file.txt", dtype = float, count = -1, sep = " ")
#tableu = tableu[2:]
