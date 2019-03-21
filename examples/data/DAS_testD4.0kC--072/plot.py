import numpy as np
import matplotlib.pyplot as plt

x = [4,8,16,32]
y = [ 207.938465,103.022677,103.690752,81.078052]

data = np.loadtxt('./HR/001.txt')
plt.plot(data[:,0],data[:,1],label='HRLRT');
data = np.loadtxt('./MASW/001.txt')
plt.plot(data[:,0],data[:,1],label='MASW');
plt.title("Dispersion Curves")
#plt.xlabel("Number of Cores")
#plt.ylabel("Execution time")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Phase Velocity (m/s)")
plt.legend(loc="upper right")
#plt.plot(wavenumber,S)
plt.savefig('picked.jpg')

