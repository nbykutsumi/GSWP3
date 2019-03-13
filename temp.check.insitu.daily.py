from numpy import *
from datetime import datetime, timedelta
import netCDF4
import numpy as np

'''
#-- SnowMip ---
DTimeBase = datetime(1900,1,1,0,0,0)
obststp   = 1 # hour
orgPath = '/data1/hjkim/ESM-SnowMIP/forcing.1D/met_gswp3c_obs_1980_2010.nc'

dayPath = '/work/a01/utsumi/GSWP3/insitu_daily/SWdown/obs/SnowMIP_gswp3c.day.1990.npy'

ncorg = netCDF4.Dataset(orgPath)
a1org = ncorg.variables['SWdown'][:]
a1time= ncorg.variables['time'][:]

a1day = np.load(dayPath)

iDTimeOrg = DTimeBase + timedelta(hours=int(a1time[0]))

irecOrg = int((datetime(1990,1,1,0)-iDTimeOrg).total_seconds() / (3600)/obststp)
print a1org[irecOrg:irecOrg+24]
print a1org[irecOrg:irecOrg+24].mean()
print a1day[0]
'''


#-- PALS ---
DTimeBase = datetime(2003,1,1,0,30,0)
obststp   = 0.5 # hour
orgPath = '/work/data1/hjkim/PALS/1.4_met/AmpleroFluxnet.1.4_met.nc'

dayPath = '/work/a01/utsumi/GSWP3/insitu_daily/SWdown/Amplero/PALS.day.2003.npy'

ncorg = netCDF4.Dataset(orgPath)
a1org = ncorg.variables['SWdown'][:]
a1time= ncorg.variables['time'][:]

a1day = np.load(dayPath)

iDTimeOrg = DTimeBase + timedelta(seconds=int(a1time[0]))

irecOrg = int((datetime(2003,1,1,0)-iDTimeOrg).total_seconds() / (3600)/obststp)


#print a1org[irecOrg:irecOrg+int(24/obststp)]
#print a1org[irecOrg:irecOrg+int(24/obststp)].mean()
#print a1day[0]

#print a1org[:48]
print a1org[:48].mean()
print a1day[0]
print a1day[:5]
