"""
A simple Python script for plotting a 1D random walk and analyzing its statistical properties using a Gaussian random number generator.

"""

import matplotlib.pyplot as plt
import numpy as np
import random

#initial conditions
n_steps=10000
n_walks=100

#doing random walk
random_walk = np.zeros((n_walks,n_steps))
for i in range(0,n_walks):
    lis1=[]
    for j in range(1,n_steps):
        random_num = random.gauss(0,1)
        lis1.append(random_num)
        if random_num>=0:
            random_step = 1
            random_walk[i,j]=random_walk[i,j-1]+random_step
        else:
            random_step = -1
            random_walk[i,j]=random_walk[i,j-1]+random_step




#calculations

mean_disp=np.sum(random_walk,axis=0)/n_walks
mean_squ_disp=np.sum(random_walk**2,axis=0)/n_walks   
rms_disp=(mean_squ_disp)**(1/2)
var=np.var(random_walk,axis=0)


#plotting of random walks

for i in range(n_walks):
    plt.plot(random_walk[i])
plt.xlabel('No. of steps')
plt.ylabel('Displacement')
plt.title('1D random walk from gaussian random number')



#plotting of parameters
plt.figure(figsize=(12,8))


plt.subplot(4,1,1)
plt.plot(mean_disp,label='mean-disp')
plt.xlabel('No. of steps')
plt.ylabel('mean displacement')
plt.title('1D random walk from gaussian random number')

plt.subplot(4,1,2)
plt.plot(mean_squ_disp,label='MSD')
plt.xlabel('No. of steps')
plt.ylabel('mean square displacement')
plt.title('1D random walk from gaussian random number')

plt.subplot(4,1,3)
plt.plot(rms_disp,label='rms-disp')
plt.xlabel('No. of steps')
plt.ylabel('rms displacemet')
plt.title('1D random walk from gaussian random number')

plt.subplot(4,1,4)
plt.plot(var,label='variance')
plt.xlabel('No. of steps')
plt.ylabel('variance')
plt.title('1D random walk from gaussian random number')

plt.tight_layout()
plt.legend()















