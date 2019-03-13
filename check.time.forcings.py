from numpy import *
import netCDF4
from datetime import datetime, timedelta
import gzip
##-- GSWP3 --
#'''
#<type 'netCDF4._netCDF4.Variable'>
#float64 time(time)
#    long_name: Time
#    standard_name: time
#    calendar: proleptic_gregorian
#    units: hours since 1871-01-01 00:00:00
#unlimited dimensions: time
#current shape = (2928,)
#filling on, default _FillValue of 9.96920996839e+36 used
#
#'''
#DTimeBase= datetime(1871,1,1,0,0)
#srcPath= '/data2/hjkim/GSWP3/in/EXP1/Tair/GSWP3.BC.Tair.3hrMap.1980.nc'
#nc     = netCDF4.Dataset(srcPath,'r')
#atime  = nc.variables['time'][:]
#iDTime = DTimeBase + timedelta(hours=int(atime[0]))
#
#print iDTime


##-- PRINCETON --
#'''
#        float time(time) ;
#                time:units = "hours since 1980-01-01 00:00:00" ;
#                time:time_origin = "01-JAN-1980:00:00:00" ;
#'''
#DTimeBase= datetime(1980,1,1,0,0)
#srcPath= '/work/data1/hjkim/PRINCETON/ncdf/1980/tas_3hourly_1980-1980.nc'
#nc     = netCDF4.Dataset(srcPath,'r')
#atime  = nc.variables['time'][:]
#iDTime = DTimeBase + timedelta(hours=int(atime[0]))
#
#print iDTime
#


##-- WFDEI --
#'''
#<type 'netCDF4._netCDF4.Variable'>
#int32 time(tstep)
#    title: time
#    units: seconds since 1980-01-01 00:00:00
#    long_name: time since start of month
#unlimited dimensions: tstep
#current shape = (248,)
#filling on, default _FillValue of -2147483647 used
#'''
#DTimeBase= datetime(1980,1,1,0,0)
#srcPath= '/data2/hjkim/WFDEI/Tair_WFDEI/Tair_WFDEI_198001.nc.gz'
#with gzip.open(srcPath) as gz:
#    nc = netCDF4.Dataset('dummy', mode='r', memory=gz.read())
#
#print nc.variables['time']
#atime  = nc.variables['time'][:]
#iDTime = DTimeBase + timedelta(hours=int(atime[0]))
#
#print iDTime
#


#-- CRUNCEP --
'''
OrderedDict([(u'Temperature', <type 'netCDF4._netCDF4.Variable'>
float32 Temperature(time_counter, latitude, longitude)
    title: Temperature
    units: K
unlimited dimensions: time_counter
current shape = (1460, 360, 720)
filling on, default _FillValue of 9.96920996839e+36 used
), (u'latitude', <type 'netCDF4._netCDF4.Variable'>
float32 latitude(latitude)
    units: Degrees
    title: Latitude
unlimited dimensions:
current shape = (360,)
filling on, default _FillValue of 9.96920996839e+36 used
), (u'longitude', <type 'netCDF4._netCDF4.Variable'>
float32 longitude(longitude)
    units: Degrees
    title: Longitude
unlimited dimensions:
current shape = (720,)
filling on, default _FillValue of 9.96920996839e+36 used
), (u'mask', <type 'netCDF4._netCDF4.Variable'>
int32 mask(latitude, longitude)
unlimited dimensions:
current shape = (360, 720)
filling on, default _FillValue of -2147483647 used
)])

'''
DTimeBase= datetime(1980,1,1,0,0)
srcPath= '/work/hk01/CRUNCEP/tair/cruncepv9_tair_1980.nc.gz'
with gzip.open(srcPath) as gz:
    nc = netCDF4.Dataset('dummy', mode='r', memory=gz.read())
print nc.variables
print nc.variables['Time']
atime  = nc.variables['Time'][:]
iDTime = DTimeBase + timedelta(hours=int(atime[0]))

print iDTime



