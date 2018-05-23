import sys
import numpy as np
import argparse as parse
import os
from sympy import nsimplify

def getconst(table, m, n):
    b = np.ndarray( [m,1] )
    for row in range(m):
        b[row][0] = table[row][n-1]

    return b

def hsplit(table, m, n):
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
    identity = np.vstack( (np.zeros( (1, m-1) ), np.identity( m-1 )) )
    identity_b = np.hstack( [identity, b] )
    tableu = hstack(table, identity_b)
    
    return tableu
    
def writeTableu(tableu, m, n, mess):
    header = mess + ' ' + (9*n) *'_' + '\n'
    footer = (12*n) * '-' + '\n'
    dst = open('output.txt', 'a')
    np.savetxt(dst, tableu, fmt='%5s', delimiter=' ', \
                newline='\n', header=header, footer=footer, \
                comments='')
    
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
    p_col = int(np.argmin(table))
    i = True
    for row in range(1, m, 1):
        buffer = tableu[row][p_col]
        b = tableu[row][n-1]
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
    etav = np.ndarray(m)
    etav = etav.astype('object')
    for row in range(m):
        if row == p_row:
            v = 1 / p
            etav[row] = nsimplify( v, rational=True) 
        else:
            a = tableu[row][p_col]
            etav[row] = ( a ) / (- p)
            etav[row] = nsimplify( etav[row], rational=True)
    
    return etav

def eta_tableu(etaV, p_row, m):
    etaM = np.identity( m )
    etaM = etaM.astype('object')
    for row in range(m):
        etaM[row][p_row] = nsimplify( etaV[row], rational=True)

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
    k = n - m
    Cts, X = np.ndarray( [k,1] ), np.ndarray( [k,1] )
    Cts, X = Cts.astype('object'), X.astype('object')
    
    for col in range(k): 
        Cts[col,0] = '0 '
        X[col,0] = '[ X_' + str(col+1) + ' ] = [ '
        ceros_count = 0
        x_row = 0
        for row in range(m):
            if tableu[row][col] == 0:
                ceros_count += 1
            if tableu[row][col] == 1:
                x_row = row
            if row == m-1:
                if ceros_count == m - 1:
                    Cts[col,0] = str(tableu[x_row][n-1]) +  ' '
                    ceros_count = 0
    
    dst.writelines('OPTIMIZATION FINISHED.\n\nValues of variables that '\
                    'optimizes our objective function:\n\n')
    string = np.c_[X, Cts]
    string = string.astype('object')
    dst.writelines( str(string) )
    dst.writelines('\n\nThe optimal value of Z is: ')
    return
    
def get_dual_vars(tableu, m, n, dst):
    k = (n-m) + 1
    #sol = tableu[0]
    sol = np.delete(tableu, np.s_[:k-1], axis=-1)
    sol = np.delete(sol, np.s_[1:], axis=0)
    sol = np.delete(sol, np.s_[k-2:], axis=-1)
    sol = np.transpose(sol)
    
    X = np.ndarray( [k-2,1] )
    X = X.astype('object')
    for row in range(k-2):
        X[row,0] = '[ X_' + str(row+1) + ' ] = [ '
    
    dst.writelines('OPTIMIZATION FINISHED.\n\nValues of variables that '\
                    'optimizes our objective function:\n\n')
    string = np.c_[X, sol]
    string = string.astype('object')
    dst.writelines( str(string) )
    dst.writelines('\n\nThe optimal value of Z is: ')    
    return sol

def Simplex(tableu, m, n, it, type_of_prob):
    p = pivot(tableu, m, n)
    etaV = eta_vect(tableu, m, n, p[0], p[1], p[2]) 
    etaM = eta_tableu(etaV, p[1], m)
    mess = 'Iteration ' + str(it) + '\n\nPivot = ' + str(p[0]) \
            + '\nRow: ' + str(p[1]) + '\nCol: ' + str(p[2]) \
            + '\n\neta matrix'
    writeTableu(etaM, m, n, mess)
    tableu = matmul(etaM, tableu)
    
    writeTableu(tableu, m, n, ' (eta matrix) x (tableu) ')
    it += 1
    
    t = opt_test(tableu[0])
    if t == False:
        Simplex(tableu, m, n, it, type_of_prob)
    else:
        dst = open('output.txt', 'a')
        if type_of_prob == 'normal':
            get_vars(tableu, m, n, dst)
        elif type_of_prob == 'dual':
            get_dual_vars(tableu, m, n, dst)
        Z = tableu[0][n-1]
        dst.writelines( ('Zopt = ', str(Z)) )
        dst.close()
        return 
    
def take_simbols(table, m, n):
    simbols = ['' for i in range(m)]
    col = n-2
    for row in range(m-1):
        simbols[row] = str(table[row+1][col])

    return simbols
    
def check_simbols(simbols, m, n):
    count = 0
    for i in range(m-1):
        if simbols[i] == '<=':
            count += 1
    
    if count == m-1:
        return True
    else:
        return False
        
def check_min(table, simbols, m):
    ones = np.ones([m])
    count = 0
    for i in range(m-1):
        if simbols[i] == '<=':
            count += 1
            if count == m-1:
                return table
        else:
            ones[i+1] = ones[i+1]*(-1)
    
    ones = np.diag(ones)
    C = np.matmul(ones, table.astype('float'))
    return C

def remove_simbols(table, n):
    tableu = np.delete(table, n-2, 1)

    return tableu

def dual_method(table, m, n):
    constants = np.transpose( getconst(table, m, n) )
    constants = np.delete(constants, 0)
    Z_dual = np.negative(constants)
    b_dual = np.delete(table, np.s_[1:], axis=0)
    b_dual = np.delete(b_dual, n-1, axis=1)
    b_dual = np.insert(b_dual, 0, 0, axis=1)
    b_dual = np.transpose(b_dual)
    b_dual = b_dual.astype('float')
    b_dual = np.negative(b_dual)
    buffer_table = np.delete(table, 0, axis=0)
    buffer_table = np.delete(buffer_table, n-1, axis=1)
    transposed_buff = np.transpose(buffer_table)
    tableu = np.vstack((Z_dual,transposed_buff))
    tableu = np.hstack((tableu,b_dual))
    return tableu

def manage_input(optimization, table, shape):
    m = int(shape[0])
    n = int(shape[1]) #this n contains also the simbols
    simbols = take_simbols(table,m,n)
    check = check_simbols(simbols,m,n)
    if check == True:
        if optimization == 'Max':
            tableu = remove_simbols(table,n)
            return 'normal', tableu
        if optimization == 'Min':
            tablu = remove_simbols(table,n)
            tablu = check_min(tablu, simbols, m)
            dual_tableu = dual_method(tablu, m, n-1)
            return 'dual', dual_tableu
    else:
        tablu = remove_simbols(table,n)
        tablu = check_min(tablu, simbols, m)
        dual_tableu = dual_method(tablu, m, n-1)
        return 'dual', dual_tableu

################################## MAIN PROGRAM
os.system('> output.txt')
srcfile = sys.argv[1]
optimization_type = np.genfromtxt(srcfile, dtype=str, max_rows=1, comments='#', delimiter=' ') 
input_ = np.genfromtxt(srcfile, dtype=str, skip_header=1, comments='#', delimiter=' ')

str_shape = input_.shape
type_of_prob, table = manage_input(optimization_type, input_, str_shape)

shape = table.shape
m = shape[0]
k = shape[1]
tableu = incrementedTableu(table, m, k)

n = (k-1) + m       #incremented tableu size columns
writeTableu(tableu, m, n, "\nIteration 0")
Simplex(tableu, m, n, 1, type_of_prob)

