from datetime import datetime, timedelta
import netCDF4

srcPath = '/work/data1/hjkim/PALS/1.4_met/TumbaFluxnet.1.4_met.nc'
nc = netCDF4.Dataset(srcPath)
DTime0 = datetime(2003,1,1,0,30,0)

atime = nc.variables['time'][:]
