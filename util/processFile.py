import matplotlib.pyplot as plt
import numpy as np
import re

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

with open('newfile2.txt', 'r') as myfile:
    data=myfile.readlines()
    
counter = len(data)
modelLen = int(counter/6)
print("modelLen"+str(modelLen))
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
            

for model in modelList:
    print("VP")
    print(model.VP)
    print("VS")
    print(model.VS)
    print("THICK")
    print(model.thickness)
    
# Let's plot this
fig, ax = plt.subplots()
for model in modelList:
    ax.plot(model.VP,np.cumsum(model.thickness),'o--')
    ax.xaxis.tick_top()

    ax.set_ylabel('depth')
    ax.set_ylim(4000, 0)
#ax.set_xlim(0, 25)
    ax.set_xlabel('vel - depth plot')

plt.show()

            
