# Draws Concat Velocity model
import os
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
import numpy as np
import re
from scipy import interpolate,ndimage
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
filename = 'editmerge_3km_3lay_4.txt'
#filename = 'editsynth.txt'
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
modelLen = int(counter/5)
#print("modelLen"+str(modelLen))
# Create an Empty list of object
modelList = [invertedModel() for _ in range(0,modelLen) ]
for count, line in enumerate(data):
    index = int(count/5)
    if(count%5==0):
        pass
    else:
        if(count%5==4):
# extract only number from the line - misfit
            val =float( line.split()[1])
            modelList[index].misfit = val
        else:
            tmp=line.split()
            print(tmp)
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
## generate new array by mod(4) val
x_1=np.array([])
y_1=np.array([])
z_1=np.array([])

x_2=np.array([])
y_2=np.array([])
z_2=np.array([])

x_3=np.array([])
y_3=np.array([])
z_3=np.array([])

x_4=np.array([])
y_4=np.array([])
z_4=np.array([])

# generate  x y z list
x_list = []
y_test = np.array([0.0,0.0,0.0,0.0])
y_test.fill(2.4)
y_list= []
vel_list = []
for count, model in enumerate(modelList):
    x_list.append(np.cumsum(model.thickness))
    y_list.append(np.full((1,4),2.4+count*0.12))
    vel_list.append(model.VS)
X, Y, Z, = np.array([]), np.array([]), np.array([])
for i in range(len(x_list)):
    for j in range(3):
        print("index")
        print(i,j)
        X = np.append(X,x_list[i][j])
        Y = np.append(Y,2.4+i*0.12)
        Z = np.append(Z,vel_list[i][j])
        if(j==0):
            x_1 = np.append(x_1,x_list[i][j])
            y_1 = np.append(y_1,2.4+i*0.12)
            z_1 = np.append(z_1,vel_list[i][j])
        elif(j==1):
            x_2 = np.append(x_2,x_list[i][j])
            y_2 = np.append(y_2,2.4+i*0.12)
            z_2 = np.append(z_2,vel_list[i][j])
        elif(j==2):
            x_3 = np.append(x_3,x_list[i][j])
            y_3 = np.append(y_3,2.4+i*0.12)
            z_3 = np.append(z_3,vel_list[i][j])
'''
fig = plt.figure()
ax1 = fig.add_subplot(411)#,projection='3d')
ax1.set_xlim([0,3000])
#ax1.set_zlim([0,8000])
#ax1.xaxis.tick_top()
ax1.scatter(x_1,y_1,z_1,c='r')

ax1.scatter(x_2,y_2,z_2,c='b')

ax1.scatter(x_3,y_3,z_3,c='g')

ax1.scatter(x_4,y_4,z_4,c='y')
ax1.set_xlabel('X Label')
ax1.set_ylabel('Y Label')
'''
#ax1.set_zlabel('Z Label')
# size X Y Z : 19*4 = 76
print(len(X))
print("\n"*10)
print(len(Y))
print("\n"*10)
print(len(Z))
# zMat does not have depth val
zMat = np.reshape(Z,(19,3))
xMat = np.reshape(X,(19,3))
zMatT = np.transpose(zMat)
xMatT = np.transpose(xMat)
# add extra data - 0km 450m/s
extraX = np.hstack((np.zeros((xMat.shape[0],1),dtype=xMat.dtype),xMat))
extraZ = np.hstack((np.full((zMat.shape[0],1),450.0),zMat))
for k in range(extraZ.shape[0]):
    if extraX[k][3]>4500:
        extraX[k][3]=4500.0
print("xmatT")
print(xMat[1])
print(zMat[1])
print(extraX[1])
print(extraZ[1])

nXlist=[]
nYlist=[]
nZlist=[]
for k in range(extraZ.shape[0]):
    f = interpolate.interp1d(extraX[k],extraZ[k])
    nYlist.append(np.full((45),2.4+0.12*k))

# 1D 0~4500
    xnew= np.arange(extraX[k].min(),extraX[k].max(),100)
    znew = f(xnew)
    nXlist.append(xnew)
    nZlist.append(znew)
#print(nXlist)# 19*45
print(np.asarray(nXlist).shape)# 19*45
print(np.asarray(nYlist).shape)# 19*45
#plt.plot(extraX[1],extraZ[1],'o',xnew,znew,'-')
CS =plt.contourf(np.asarray(nYlist),np.asarray(nXlist),np.asarray(nZlist),20,cmap=plt.cm.rainbow,
        vmax=5000,vmin=0)
# Rotate this!
plt.colorbar()
# for downward y 
plt.gca().invert_yaxis()
## ugly scatter dots.(NG)
#plt.scatter(nYlist[1],nXlist[1],nZlist[1])
print(nYlist[1],nXlist[1],nZlist[1])
plt.savefig('vel.png',bbox_inches='tight')
#plt.show()
fig = plt.figure()
#plt.matshow(np.transpose(zMat))
ax1 =fig.add_subplot(111)
#cax = ax1.matshow(np.transpose(zMat), interpolation='nearest')
#fig.colorbar(cax)


#ax1.scatter(X,Y,Z)
#ax4.scatter(X,Y,Z)
#plt.contourf(X,Y,Z)

#plt.show()

            
