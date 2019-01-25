import os
import matplotlib.pyplot as plt
import numpy as np
import re
from scipy.interpolate import griddata

# same structure
# Label
# numLayer fixed - 4 here.
# misfit
# Create a class for storage
class invertedModel:
    def __init__(self):
        self.VP = []
        self.VS = []
        self.thickness = []
        self.misfit=0.0
    def append(self,vp,vs,thick):
        self.VP.append(vp)
        self.VS.append(vs)
        self.thickness.append(thick)

## when one txt file containes multiple inversion result
#filename ='editprocD_n604km_002.txt' 
#filename ='editD_merg2.txt'
filename='editmerged_3km_2.txt'
with open(filename, 'r') as myfile:
    data=myfile.readlines()
## when read from individual inversion results
# generate filelist
'''
list_dir = os.listdir('./DAS_invert/')
sorted(list_dir)
temp = list_dir.sort()
for fileName in list_dir:
    with open('./DAS_invert/'+list_dir, 'r') as myfile:
    '''
        
    
counter = len(data)
modelLen = int(counter/6)
#print("modelLen"+str(modelLen))
# Create an Empty list of object
modelList = [invertedModel() for _ in range(0,modelLen) ]
for count, line in enumerate(data):
    index = int(count/6)
    if(count%6==0):
        pass
    else:
        if(count%6==5):
# extract only number from the line - misfit
            val =float( line.split()[1])
            modelList[index].misfit = val
        else:
            tmp=line.split()
            modelList[index].append(float(tmp[0]),float(tmp[1]),float(tmp[2]))
            
# list of model obj.
#for model in modelList:
    #print("VP")
    #print(model.VP)
    #print("VS")
    #print(model.VS)
    #print("THICK")
    #print(model.thickness)
# let's generate grid
# 2.4 to increment 0.12km
'''
y = np.arange(2.4,4.4,0.12)
y = np.append(y,4.4)
print(y)
x_list = []
y_test = np.array([0.0,0.0,0.0,0.0])
y_test.fill(2.4)
y_list= []
vel_list = []
print(y_test)
# generate  x y z list
for count, model in enumerate(modelList):
    x_list.append(np.cumsum(model.thickness))
    y_list.append(np.full((1,4),2.4+count*0.12))
    vel_list.append(model.VS)
    
print("!!--------------------------------")
print(x_list)
print("!!--------------------------------")
print(y_list[10][0][1]) # this returns 1x4
print("!!--------------------------------")
print(vel_list)
X, Y, Z, = np.array([]), np.array([]), np.array([])
for i in range(len(x_list)):
    for j in range(4):
        print("index")
        print(i,j)
        X = np.append(X,x_list[i][j])
        Y = np.append(Y,2.4+i*0.12)
        Z = np.append(Z,vel_list[i][j])
# create x-y points to be used in heatmap
xi = np.linspace(X.min(), 5000, 100)
yi = np.linspace(Y.min(), Y.max(), 100)

# Z is a matrix of x-y values
zi = griddata((X, Y), Z, (xi[None,:], yi[:,None]), method='cubic')
print(zi)
# I control the range of my colorbar by removing data 
# outside of my range of interest
zmin =0 
zmax =10000
zi[(zi<zmin) | (zi>zmax)] = None

# Create the contour plot
#CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.rainbow,
#                  vmax=zmax, vmin=zmin)
plt.pcolormesh(xi, yi,zi)
plt.colorbar()  
plt.show()

'''

# Let's plot this
fig, ax = plt.subplots()
for model in modelList:
    ax.step(model.VS,np.cumsum(model.thickness),'o--')
    ax.xaxis.tick_top()

    ax.set_ylabel('depth')
    ax.set_ylim(3500, 0)
#ax.set_xlim(0, 25)
    ax.set_xlabel('vel - depth plot')

plt.show()

            
