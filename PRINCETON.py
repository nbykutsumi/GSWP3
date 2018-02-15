from numpy import *
import numpy as np
import os, sys
from netCDF4 import Dataset

class PRINCETON(object):
    def __init__(self):
        self.baseDir = "/data1/hjkim/PRINCETON/ncdf"
        self.Lat     = arange(-89.5,89.5+0.001,1.0)
        self.Lon     = arange(0.5,359.5+0.001,1.0)
        self.LatBnd  = arange(-90,90+0.01,1.0)
        self.LonBnd  = arange(0,360+0.01, 1.0)
        self.ny      = len(self.Lat)
        self.nx      = len(self.Lon)


    def load_nc(self, varName, Year):
        srcDir  = self.baseDir + "/%04d"%(Year)
        srcPath = srcDir + "/%s_3hourly_%s-%s.nc"%(varName, Year,Year)
        print srcPath
        nc = Dataset(srcPath, "r", format="NETCDF")
        return nc
        
