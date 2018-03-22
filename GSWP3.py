from numpy import *
import numpy as np
import os, sys
from netCDF4 import Dataset

class GSWP3(object):
    def __init__(self):
        self.baseDir = "/data2/hjkim/GSWP3/in"
        self.Lat     = arange(-89.75,89.75+0.0001,0.5)
        self.Lon     = arange(0.25,359.75+0.0001,0.5)
        self.LatBnd  = arange(-90,90+0.001, 0.5)
        self.LonBnd  = arange(0,360+0.001,0.5)
        self.ny      = len(self.Lat)
        self.nx      = len(self.Lon)

    def __call__(self, **kwargs):
        self.expr= kwargs["expr"]


    def load_nc(self, varName, Year):
        srcDir = self.baseDir + "/%s/%s"%(self.expr, varName)
        srcPath= srcDir + "/GSWP3.BC.%s.3hrMap.%04d.nc"%(varName, Year)
        print srcPath
        nc = Dataset(srcPath, "r", format="NETCDF")
        return nc

    def load_elevation(self):
        srcPath = "/data1/hjkim/CRU/TS3.23/cru_ts3.23.1901.2014.halfdesg.elv.02^"
        a2in = fromfile(srcPath, float32).reshape(360,720)
        a2elev = concatenate([a2in[:,360:], a2in[:,:360]], axis=1)
        return a2elev
