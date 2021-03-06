from numpy import *
import numpy as np
import os, sys
from netCDF4 import Dataset


# load sample file
varName = "Rainf"
Year    = 1999
srcDir  = "/data2/hjkim/GSWP3/in/EXP1/%s"%(varName)
srcPath = srcDir + "/GSWP3.BC.%s.3hrMap.%04d.nc"%(varName, Year)

ncIn = Dataset(srcPath, "r", format="NETCDF")

Dat  = ncIn[varName]
Lat  = ncIn["lat"]
Lon  = ncIn["lon"]
Time = ncIn["time"]

TypeDat  = Dat.dtype
TypeLat  = Lat.dtype
TypeLon  = Lon.dtype
TypeTime = Time.dtype

# get attributes
Attr = {}
for attr in ncIn.ncattrs():
    Attr[attr] = ncIn.getncattr(attr)


# load output file
print Attr
outPath = "./temp.nc"
ncOut= Dataset(outPath, "w", format="NETCDF4")




#print ncIn.dimensions
## Create file
#outPath = "./temp.nc"
#ncOut= Dataset(outPath, "w", format="NETCDF4")

## Dimension
#ncOut.createDimension("lat", len(Lat))
#ncOut.createDimension("lon", len(Lon))
#ncOut.createDimension("time", len(Time))
#
#
## Variables
#lat  = ncOut.createVariable("lat",  TypeLat,  ("lat",))
#lon  = ncOut.createVariable("lon",  TypeLon,  ("lon",))
#time = ncOut.createVariable("time", TypeTime, ("time",))
#dat  = ncOut.createVariable(varName,  TypeDat,  ("time", "lat", "lon"))


# Attributes
for attr in Attr.keys():
    ncOut.setncattr(attr, Attr[attr])

# close and write file
ncOut.close()
print outPath


print ncOut["lat"] == ncIn["lat"]
print ncOut["lon"] == ncIn["lon"]
print ncOut["time"] == ncIn["time"]
print ncOut[varName] == ncIn[varName]


