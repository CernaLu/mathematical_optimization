import sys
import numpy as np
import argparse as parse
import os
from sympy import *
from decimal import Decimal

# CHECK ITERATION 1, IT'S WRONG

    # It's important not to stay in an infinit cycle that could
    # happen if there are repeated pivots. Code should be
    # able to identify and pick the next pivot, even if it
    # has the same value

def getconst(table, i, j):
    m = int(i)
    n = int(j)
    b = np.ndarray( [m,1] )
    for row in range(m):
        b[row][0] = table[row][n-1]

    return b

def hsplit(table, i, j):
    m = int(i)
    n = int(j)
    tableu = np.ndarray( [m,n-1] )
    for row in range(m):
        for col in range(n-1):
            tableu[row][col] = table[row][col]

    return tableu

def hstack(A, B):
    a, b = A.shape, B.shape
    m, n = a[0], a[1]+b[1]
    C = np.ndarray( [m,n] )
    for i in range(m):
        l, k = -1, -1
        for j in range(n):
            if j < a[1]:
                l += 1
                C[i][j] = A[i][l]
            elif j >= a[1]:
                k += 1
                C[i][j] = B[i][k]

    return C

def incrementedTableu(table, m, n):
    b = getconst(table, m, n)
    table = hsplit(table, m, n)
    identity = np.vstack( (np.zeros( (1, int(m)-1) ), np.identity( int(m)-1 )) )
    identity_b = np.hstack( [identity, b] )
    tableu = hstack(table, identity_b)
    
    return tableu
    
def writeTableu(tableu, m, n, mess):
    size = tableu.shape
    tableu = tableu.astype('object')
    for i in range(int(size[0])):
        for j in range(int(size[1])):
            tableu[i][j] = tableu[i][j]
    
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
    print (tableu)
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
    etav = np.ndarray(int(m))
    etav = etav.astype('object')
    for row in range(int(m)):
        if row == int(p_row):
            a = int(tableu[row][int(p_col)])
            etav[row] = Rational(1, int(p))
        else:
            a = int(tableu[row][int(p_col)])
            #etav[int(row)] = ( a ) / (- p)
            etav[row] = Rational(a, int(-p) )

    return etav

def eta_tableu(etaV, p_row, m):
    print('m =', m)
    etaM = np.identity( int(m) )
    etaM = etaM.astype('object')
    for row in range(int(m)):
        etaM[row][int(p_row)] = Rational(etaV[row])

    return etaM

def matmul(A, B):
    a, b = A.shape, B.shape
    m, r, n = a[0], a[1], b[1]
    c = np.ndarray( [m,n] )
    
    for i in range(m):
        for j in range(n):
            for k in range(r):
                c[i][j] += A[i][k] * B[k][j]
                c[i][j] = round(c[i][j], 2)
                c[i][j] = Rational(c[i][j])
    
    return c

def Simplex(tableu, m, n, etav):
    #change etav declaration to this location
    t = opt_test(tableu[0])
    if t == True:
        return 0 # MUST CHANGE THIS FOR A FINALIZATION ROUTINE
    
    p = pivot(tableu, m, n)
    etaV = eta_vect(tableu, m, n, p[0], p[1], p[2]) #gives eta as a row

    etaM = eta_tableu(etaV, p[1], m)
    writeTableu(etaM, m, n, 'eta Tableu')
    etaM = etaM.astype('float')
    T = matmul(etaM, tableu)
    writeTableu(T, m, n, 'Iteration 1')
    
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

n = (n-1) + m #Now n has the incremented tableu size, not the original
writeTableu(tableu, m, n, "\nIteration 0")
Simplex(tableu, m, n, etav)

#size = np.fromfile("file.txt", dtype = float, count = 2, sep = " ")
#tableu = np.fromfile("file.txt", dtype = float, count = -1, sep = " ")
#tableu = tableu[2:]
