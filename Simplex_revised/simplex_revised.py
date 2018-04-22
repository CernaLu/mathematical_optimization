import sys
import numpy as np
from fractions import Fraction
import argparse as parse

def incrementedTableu(table, m, n):
    b = np.hsplit(table, int(n))
    b = b[int(n)-1]
    table = np.hsplit(table, np.array([int(m)-1,int(n)]) )
    table = table[0]
    identity = np.vstack( (np.zeros( (1, int(n)-1) ), np.identity( int(m)-1 )) )
    identity_b = np.hstack ( [identity, b] )
    tableu = np.hstack( (table, identity_b) ) #tableu[:] = np.hstack( [table, np.identity(int(n) ])

    return tableu
    

table = np.ndarray( (20,20) )

table = np.loadtxt("file.txt", dtype=float, comments='#', delimiter=" ")
m = table[0][0]
n = table[1][0]
table = table[2:]
tableu = incrementedTableu(table, m, n)
