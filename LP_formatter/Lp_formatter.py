import numpy as np
import os

dst = open("src.lp", "w")

print("\nSelect option:\n\n  1) Maximize\n\n  2) Minimize\n\n")
obj = input()
print("\nNumber of variables?\n\n")
nvars = input()
print("\nEnter obj equation's coefficients in order\n")
Oequ = input()
print("\nNumber of restrictions?\n\n")
nequ = input()
Requ = ['' for x in range(int(nequ))]
print("\nEnter restriction's coefficients\n")
for n in range(int(nequ)):
    Requ[n] = input()

print("\nSelc option:\n\n   1) Xi >= 0\n   2) Insert bounds\n\n")
bounds = input()

if int(obj) == 1:
    dst.write('Maximize\n')
elif int(obj) == 2:
    dst.write('Minimize\n')
else:
    exit()

dst = open("src.lp", "a")
dst.write(' obj: ')
for x in range(int(nvars)):
    if x == 0:
        dst.writelines( [str(Oequ[2*x]), ' x', str(x+1)] )
    else:
        dst.writelines( [' + ', str(Oequ[2*x]), ' x', str(x+1)] )

dst.write('\nSubject To')
for c in range(int(nequ)):
    dst.writelines( ['\n c',str(c+1),': '] )
    for x in range(int(nvars)):
        if x == 0:
            dst.writelines( [str(Requ[c][2*x]), ' x', str(x+1)] )
        else:
            dst.writelines( [' + ', str(Requ[c][2*x]), ' x', str(x+1)] )

dst.write('\nBounds')
if int(bounds) == 1:
    for r in range(int(nvars)):
        dst.writelines( ['\n0 <= ', 'x', str(r+1)] )
elif int(bounds) == 2:
    print('\nHow many boundaries?')
    nb = input()
    for c in range(int(nb)):
        boundaries[c] = input()
else:
    exit()

dst.write('\nEND')
dst.close()
print('\n\n')

