import numpy as np
#DataIn = np.loadtxt('ewe_mode0.txt')
filename = 'test2.5kDm--060.txt'
DataIn = np.loadtxt(filename)
#print(DataIn)
print(DataIn[:,0])
print(DataIn[:,1])
print(DataIn[:,1]/DataIn[:,0])
