import matplotlib
matplotlib.use('Agg')
from numpy import *
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

obsPath = '/work/data1/hjkim/PALS/1.4_met/AmpleroFluxnet.1.4_met.nc'
#fcgPath= '/work/a01/utsumi/GSWP3/insitu/Tair/Amplero/GSWP3.3hr.2003.npy'
#fcgPath= '/work/a01/utsumi/GSWP3/insitu/Tair/Amplero/PRINCETON.3hr.2003.npy'
fcgPath= '/work/a01/utsumi/GSWP3/Tair/swa/PRINCETON.3hr.2003.npy'
nc = Dataset(obsPath)
a1time = nc.variables['time'][::6]
a1obs = nc.variables['Tair'][::6]

print a1time[:4]
a1fcg = np.load(fcgPath)

nrec = len(a1fcg)
print nrec

#eDTime = datetime(2003,1,1,0,30) + timedelta(seconds=a1time[nrec*2*3])
#print eDTime

plt.scatter(a1fcg, a1obs[:nrec])
figPath = '/work/a01/utsumi/GSWP3/insitu/temp.png'
plt.savefig(figPath)
print figPath


