import sys
import numpy as np
import argparse as parse
import os
from sympy import *
from decimal import Decimal

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
    header = mess + ' ' + int(9*n)*'_' + '\n'
    footer = int(12*n) * '-' + '\n'
    dst = open('output.txt', 'a')
    np.savetxt(dst, tableu, fmt='%5s', delimiter=' ', newline='\n', header=header, footer=footer)
    
    dst.close() 
    return


def opt_test(Z_vect): #Stop when all coff in Z are > 0
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
        buffer = tableu[row][int(p_col)]
        b = tableu[row][int(n)-1]
        if (buffer > 0):
            buff_test = b / buffer
            if i == True:
                p = buffer
                test = buff_test
                p_row = row
            elif buff_test < test:
                p = buffer
                test = buff_test
                p_row = row
            i = False
    
    return p, p_row, p_col
    
def eta_vect(tableu, m, n, p, p_row, p_col):
    etav = np.ndarray(int(m))
    etav = etav.astype('object')
    for row in range(int(m)):
        if row == int(p_row):
            v = 1 / p
            etav[row] = nsimplify( (v), rational=True) 
        else:
            a = tableu[row][int(p_col)]
            etav[row] = ( a ) / (- p)
            etav[row] = nsimplify( (etav[row]), rational=True)
    
    return etav

def eta_tableu(etaV, p_row, m):
    etaM = np.identity( int(m) )
    etaM = etaM.astype('object')
    for row in range(int(m)):
        etaM[row][int(p_row)] = Rational(etaV[row])

    return etaM

def matmul(A, B):
    a, b = A.shape, B.shape
    m, r, n = a[0], a[1], b[1]
    c = np.ndarray( [m,n] )
    c = c.astype('object')
    
    for i in range(m):
        for j in range(n):
            c[i][j] = 0
            for k in range(r):
                c[i][j] += A[i][k] * B[k][j]
                c[i][j] = nsimplify( (c[i][j]), rational=True )
    
    return c

def get_vars(tableu, m, n, dst):
    k = int(int(n)-int(m))
    K = np.ndarray( [k,1] )
    X = np.ndarray( [k,1] )
    K = K.astype('object')
    X = X.astype('object')
    for j in range(k):
        K[j,0] = '0 '
        X[j,0] = '[ X_' + str(j+1) + ' ] = [ '
        n_ceros = 0
        for i in range(int(m)):
            if tableu[i][j] == 0:
                n_ceros +=1
            if n_ceros == int(m-1):
                K[j,0] = str(tableu[i][int(n)-1]) +  ' '
                n_ceros = 0
    
    dst.writelines('OPTIMIZATION FINISHED.\n\nValues of variables that '\
                    'optimizes our objective function:\n\n')
    string = np.c_[X, K]
    string = string.astype('object')
    dst.writelines( str(string) )
    dst.writelines('\n\nThe optimal value of Z is: ')
    return

def Simplex(tableu, m, n, it):
    p = pivot(tableu, m, n)
    etaV = eta_vect(tableu, m, n, p[0], p[1], p[2]) #gives eta as a row
    etaM = eta_tableu(etaV, p[1], m)
    #writeprod(etaM, tableu)
    mess = 'Iteration ' + str(it) + '\n\nPivot = ' + str(p[0]) \
            + '\nRow: ' + str(p[1]) + '\nCol: ' + str(p[2]) \
            + '\n\neta matrix'
    writeTableu(etaM, m, n, mess)
    etaM = etaM.astype('float')
    tableu = matmul(etaM, tableu)
    
    writeTableu(tableu, m, n, ' (eta matrix) x (tableu) ')
    it += 1

    t = opt_test(tableu[0])
    if t == False:
        Simplex(tableu, m, n, it)
    else:
        dst = open('output.txt', 'a')
        get_vars(tableu, m, n, dst)
        Z = tableu[0][int(n)-1]
        dst.writelines( ('Zopt = ', str(Z)) )
        dst.close()
        return 

################################## MAIN PROGRAM
os.system('> output.txt')
table = np.ndarray( (20,20) ) 

table = np.genfromtxt("input.txt", dtype=float, comments='#',\
                        skip_header=2 ,delimiter=' ') 
shape = np.genfromtxt("input.txt", dtype=float, comments='#',\
                        usecols=(0) , max_rows=2 ) 
m = shape[0]
n = shape[1]
tableu = incrementedTableu(table, m, n)

n = (n-1) + m #Now n has the incremented tableu size, not the original
writeTableu(tableu, m, n, "\nIteration 0")
Simplex(tableu, m, n, 1)

