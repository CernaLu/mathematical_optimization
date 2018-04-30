import numpy as np

print("\nSelect option:\n\n  1) Maximize\n\n  2) Minimize\n\n")
obj = input()

print("\nNumber of variables?\n\n")
nvars = input()

print("\nEnter obj equation's coefficients in order\n")
Oequ = input()

print("\nNumber of restrictions?\n\n")
nequ = input()

print("\nSelc option:\n\n   1) Xi > 0\n   2) Insert bounds\n\n")
bounds = input()

dst = open("src.lp", "w")

if int(obj) == 1:
    dst.write('Maximize\n')
elif int(obj) == 2:
    dst.write('Minimize\n')
else:
    exit()

dst = open("src.lp", "a")
i = 0
dst.writelines(' obj: ')
for x in range(int(nvars)):
    if i == 0:
        dst.writelines( [str(Oequ[2*x]), 'x', str(i+1)] )
    else:
        dst.writelines( [' + ', str(Oequ[2*x]), 'x', str(i+1)] )
    i += 1


#for i in range(nvars):
#    X.extend()
#for i in range(nequ):
#    if int(i) == 1:
#        dst.writelines( 'c', i, ': ', for j in )
 
print('\n\n')
dst.close()
