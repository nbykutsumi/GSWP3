from numpy import *
import numpy as np
import os, sys
from netCDF4 import Dataset

varName = "prcp"
Year    = 2000
baseDir = "/data1/hjkim/PRINCETON/ncdf"
srcDir  = baseDir + "/%04d"%(Year)
srcPath = srcDir + "/%s_3hourly_%s-%s.nc"%(varName, Year,Year)
nc = Dataset(srcPath, "r", format="NETCDF")
