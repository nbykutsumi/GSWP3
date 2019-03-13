import matplotlib
matplotlib.use('Agg')
from numpy import *
import numpy as np
import matplotlib.pyplot as plt

lvarName  = ["Rainf","Snowf","SWdown","LWdown","Tair","Qair","PSurf","Wind"]
gswpPath  = '/work/a01/utsumi/GSWP3/insitu_daily/SWdown/cdp/GSWP3.day.1980.npy'

wfdeiPath = '/work/a01/utsumi/GSWP3/insitu_daily/SWdown/cdp/WFDEI.day.1980.npy'
princePath= '/work/a01/utsumi/GSWP3/insitu_daily/SWdown/cdp/PRINCETON.day.1980.npy'
cruPath   = '/work/a01/utsumi/GSWP3/insitu_daily/SWdown/cdp/CRUNCEP.day.1980.npy'

a1gswp   = np.load(gswpPath)
a1wfdei  = np.load(wfdeiPath)
a1prince = np.load(princePath)
a1cru    = np.load(cruPath)*0.0001
#--- WFDEI & PRINCETON ----
nstep = 8*4
x1  = arange(0,3*nstep,3)      # pre 3hr
x2  = arange(0,3*nstep,3) + 3  # post 3hr
plt.plot(x1, a1gswp[:nstep],'--',color='k')
plt.plot(x1, a1wfdei[:nstep],'-',color='r')
plt.plot(x2, a1prince[:nstep],'-',color='b')

outPath = '/work/a01/utsumi/GSWP3/insitu/diurnal1.png'
plt.savefig(outPath)
plt.clf()
print outPath

#--- CRUNCEP ----
nstep = 8*4
x1  = arange(0,3*nstep,3)
x2  = arange(0,3*nstep,6) +6
plt.plot(x1,a1gswp[:nstep],'--',color='k')
plt.plot(x2,a1cru[:int(nstep/2)],'-',color='r')

outPath = '/work/a01/utsumi/GSWP3/insitu/diurnal2.png'
plt.savefig(outPath)
plt.clf()
print outPath


#--- CRUNCEP @6h comparizon----
nstep = 8*4
x1  = arange(0,3*nstep,6) 
x2  = arange(0,3*nstep,6) 

y1  = a1gswp[1:-1].reshape(-1,2).mean(axis=1)   # GSWP pre-3h --> after 6hr
plt.plot(x1,y1[:int(nstep/2)],'--',color='k')
plt.plot(x2,a1cru[:int(nstep/2)],'-',color='r')

outPath = '/work/a01/utsumi/GSWP3/insitu/diurnal3.png'
plt.savefig(outPath)
plt.clf()
print outPath

