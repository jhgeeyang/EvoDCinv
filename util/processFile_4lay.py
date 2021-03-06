import os
import matplotlib.pyplot as plt
import numpy as np
import re
from scipy.interpolate import griddata
from scipy.stats import gaussian_kde
from matplotlib.lines import Line2D

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
#filename='editmerged_3km_2.txt'
#filename = 'editsynth5.txt'
filename = 'editinv5temp_.txt'
#filename = 'editinvResult_0315_DAS.txt'
filename = 'editinvResult_0318_DAS.txt'
#filename='edit5lay_3.0_.txt'
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
# Create an Empty list of object - to make an Input Form
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
            # append each list  VP VS THICK
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
misfit_list = []
print(y_test)
# generate  x y z list
for count, model in enumerate(modelList):
    x_list.append(np.cumsum(model.thickness))
    y_list.append(np.full((1,4),2.4+count*0.12))
    vel_list.append(model.VS)
    misfit_list.append(model.misfit)

print("max min misfit val")
print(max(misfit_list),min(misfit_list))
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

# CODE run
misfit_list = []
# Let's plot this

### RED LINES
## NEED TO PLOT INVERSION BOUNDARIES.(LOWEST - HIGHEST)
par_beta = np.array([ [ 600., 2300. ], [ 700., 2400. ], [ 750., 4000. ],[ 1000., 4000. ]])#,[1200.,4200. ]])
low_beta = par_beta[:,0]
high_beta = par_beta[:,1]

# - NOTE: final layer 
par_thick = np.array([ [ 100., 500. ], [ 250., 800. ] ,[500.,1200],[ 99999., 99999. ] ])
low_thick = par_thick[:,0]
high_thick = par_thick[:,1]

fig, ax = plt.subplots()
print(low_beta)
print(high_beta)
print(np.concatenate( ([0],low_thick) )[0:-1])
print(np.concatenate( ([0],high_thick) )[0:-1])
print(np.concatenate( ([0],np.cumsum(high_thick)) )[0:-1])

# PLOT LOW / HIGH BOUND
#val=low_beta[-1]
#fixModel = model.VS+[val]
# TRUE - 2 Data
DataIn = np.loadtxt('../examples/data/trueVS/mid.txt')
#ax.step(DataIn[:,1],DataIn[:,0],'*')
DataIn = np.loadtxt('../examples/data/trueVS/stack.txt')
#ax.step(DataIn[:,1],DataIn[:,0],'*')
exitCount =0
print("modelLEN")
print(len(modelList))
avgMode = invertedModel(); # Create an Empty Model to collect all model values
avgMode.thickness =np.zeros(5)
avgMode.VS=np.zeros(5)

# variable to collect the stair points in plot
x_collect=[]
y_collect=[]

## Plot and Binning
for model in modelList:
    misfit_list.append(model.misfit)
# shape of cumsum (3,)
# model.VS is a list variable
    if(exitCount>=0):
        #print(np.concatenate( ([0],np.cumsum(model.thickness)) )[:-1] ) 
        #print(model.VS)
        val=model.VS[-1]
        fixModel = model.VS+[val]
        #print(fixModel)

        avgMode.VS = np.asarray(avgMode.VS) + np.asarray(fixModel)
# First empty matching shape ndarray is need for calc
        avgMode.thickness =np.add(avgMode.thickness, np.concatenate( ([0],np.cumsum(model.thickness)) ))

        #ax.step(model.VS,np.concatenate( ([0],np.cumsum(model.thickness)) )[:-1] ,'o--')
# PLOT
  #      ax.step(fixModel,np.concatenate( ([0],np.cumsum(model.thickness)) ),'o--',alpha=0.1,color="0.4")
#        print(model.VS,np.concatenate( ([0],np.cumsum(model.thickness)[0:-1])) )

        x_collect.append(model.VS[:-1])
        y_collect.append(np.concatenate( ([0],np.cumsum(model.thickness)[0:-2]) ))

        #ax.step(model.VS,newThick[:-1],'o--')
        #ax.step(model.VS,np.cumsum(model.thickness),'o--')
        ax.xaxis.tick_top()

        ax.set_ylabel('Depth (m)')
        ax.set_ylim(700, 0)
        exitCount = exitCount +1
#ax.set_xlim(0, 25)
        ax.set_xlabel('S-Wave velocity (m/s)')
    else:
        break
# Plot Best Model
bestIndex = misfit_list.index(min(misfit_list))
print("lowest misfit: " + str(min(misfit_list)))
#print(sorted(range(len(misfit_list)), key=lambda i : misfit_list[i])[0:2])
print("highest misfit: " + str(max(misfit_list)))
# Draw the top models
# Top10
for goodIndex in sorted(range(len(misfit_list)), key=lambda i : misfit_list[i])[1:10]:
    val=modelList[goodIndex].VS[-1]
    print(misfit_list[goodIndex])
    fixModel = modelList[goodIndex].VS+[val]
    ax.step(fixModel,np.concatenate( ([0],np.cumsum(modelList[goodIndex].thickness)) ),'*',color='green')
#ax.step(modelList[63].VS,modelList[63].thickness,'X')
    
##BEST
val=modelList[bestIndex].VS[-1]
fixModel = modelList[bestIndex].VS+[val]
ax.step(fixModel,np.concatenate( ([0],np.cumsum(modelList[bestIndex].thickness)) ),'X',color='blue',linewidth=3)

# Plot Avg Model
print(max(misfit_list),min(misfit_list))
print(misfit_list.index(max(misfit_list)),misfit_list.index(min(misfit_list)))
print(avgMode.thickness)
print(avgMode.VS)
avgMode.thickness = avgMode.thickness/len(modelList)
avgMode.VS= np.asarray(avgMode.VS)/len(modelList)
#ax.step(avgMode.VS,avgMode.thickness,'D',color='orange')

#LASTLY the red DASH
##ax.legend(['result','bound']) NG

                #Line2D([0], [0], color='orange', lw=2),
## Create custom legend with Line2D
custom_lines = [Line2D([0], [0], color='red',linestyle='dashed', lw=2),
                Line2D([0], [0], color='green', lw=2),
                Line2D([0], [0], color='blue', lw=2)]

#fig, ax = plt.subplots()
#lines = ax.plot(data)
ax.legend(custom_lines, ['Bounds',  'top 10','best fit'])

##
ax.plot(np.append(low_beta,low_beta[-1]),np.concatenate( ([0],np.cumsum(low_thick)) ),linestyle='--',drawstyle='steps',color='red')
ax.plot(np.append(high_beta,high_beta[-1]),np.concatenate( ([0],np.cumsum(low_thick)) ),linestyle='--',drawstyle='steps',color='red')
plt.savefig('1DInv.png',transparent='true')
#plt.savefig('inv.png')
#plt.show()


x_ravel =np.asarray(x_collect).ravel()
y_ravel =np.asarray(y_collect).ravel()
print(x_ravel.shape)
print(y_ravel.shape)

##########################33
# hist2D was UGLY
# for new window
plt.figure()

#BLUES OR
plt.hist2d(x_ravel,y_ravel,bins=[16,40],cmap='viridis')
#plt.hist2d(np.asarray(x_collect).ravel(),np.asarray(y_collect).ravel(),bins=100,cmap='Blues')
cb = plt.colorbar()
cb.set_label('count in Bin')
plt.xlim(left=min(x_ravel),right=max(x_ravel))
plt.ylim(bottom=min(y_ravel),top=max(y_ravel))
#plt.ylim(ymin=0,ymax=2000)
plt.show()

# TRY KDE
'''
plt.figure()

kde_data = np.vstack([x_ravel,y_ravel])
kde = gaussian_kde(kde_data)            
xgrid = np.linspace(0,max(x_ravel),200)
ygrid = np.linspace(min(y_ravel),max(y_ravel),200)
Xgrid, Ygrid = np.meshgrid(xgrid,ygrid)
Z = kde.evaluate(np.vstack([Xgrid.ravel(),Ygrid.ravel()]))
#extent=[0,4000,0,1000]
# Blues or
plt.imshow(Z.reshape(Xgrid.shape).T,origin='lower',aspect='auto',cmap='Blues')
cb = plt.colorbar()
cb.set_label("density")
plt.show()
'''
