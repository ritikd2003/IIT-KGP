"""
A simple Python script for plotting a 2D random walk and analyzing its statistical properties using a Gaussian random number generator.

"""
import numpy as np
import random
import matplotlib.pyplot as plt

#initial condition
n_steps=1000
n_walks=100

#doing rando walk
x_random_walk=np.zeros((n_walks,n_steps))
y_random_walk=np.zeros((n_walks,n_steps))

for i in range(0,n_walks):
    x_lis=[]
    y_lis=[]
    for j in range(1,n_steps):
        x_random_num=random.gauss(0,1)
        x_lis.append(x_random_num)
        if x_random_num>=0:
            x_step=1
        else:
            x_step=-1
        x_random_walk[i,j]=x_random_walk[i,j-1]+x_step
        y_random_num=random.gauss(0,1)
        y_lis.append(y_random_num)
        if y_random_num>=0:
            y_step=1
        else:
            y_step=-1
        y_random_walk[i,j]=y_random_walk[i,j-1]+y_step

resultant_walk=(x_random_walk**2 + y_random_walk**2)**(1/2)




#calculation parameters

mean_disp=np.mean(resultant_walk,axis=0)
mean_squ_disp=np.mean(resultant_walk**2,axis=0)
rms_disp=np.sqrt(mean_squ_disp)
variance=np.var(resultant_walk,axis=0)

#plotting

plt.figure(figsize=(12,8))
  

plt.subplot(4,1,1)
plt.plot(mean_disp,label='mean-disp')
plt.xlabel('No. of steps')
plt.ylabel('mean displacement')
plt.title('2D random walk from gaussian random number')

plt.subplot(4,1,2)
plt.plot(mean_squ_disp,label='mean-squ-disp')
plt.xlabel('No. of steps')
plt.ylabel('mean square displacement')
plt.title('2D random walk from gaussian random number')


plt.subplot(4,1,3)
plt.plot(rms_disp,label='rms-disp')
plt.xlabel('No. of steps')
plt.ylabel('root mean square displacement')
plt.title('2D random walk from gaussian random number')


plt.subplot(4,1,4)
plt.plot(variance,label='variance')
plt.xlabel('No. of steps')
plt.ylabel('variance')
plt.title('2D random walk from gaussian random number')

plt.tight_layout()



