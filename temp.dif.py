from numpy import *
from netCDF import *


lvarName = ["LWdown"]
baseDir1 = "/data2/hjkim/GSWP3/in/EXP1"
baseDir2 = "/data2/hjkim/GSWP3/from_tank.bin/out"

srcDir1 = baseDir1 + "/%s"%(varName)
srcDir2 = baseDir2 + "/%s"%(varName)

srcPath1 = srcDir1 + "/GSWP3.BC.%s.3hrMap.%04d.nc"%(varName, Year)
srcPath2 = srcDir2 + "/GSWP3.%s.%04d-%04d.nc"%(varName,Year,Year)

nc1 = Dataset(srcPath1, "r", format="NETCDF")
nc2 = Dataset(srcPath2, "r", format="NETCDF")



