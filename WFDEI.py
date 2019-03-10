from numpy import *
import numpy as np
import os, sys
from netCDF4 import Dataset
import subprocess
import gzip

class WFDEI(object):
    def __init__(self):
        self.baseDir = "/data2/hjkim/WFDEI"
        self.Lat     = arange(-89.75, 89.75+0.01, 0.5)
        self.Lon     = arange(-179.75, 179.75+0.01, 0.5)
        self.LatBnd  = arange(-90, 90+0.01, 0.5)
        self.LonBnd  = arange(-180, 180+0.01, 0.5)
        self.ny      = len(self.Lat)
        self.nx      = len(self.Lon)
        self.tempDir = "/home/utsumi/temp"
        self.miss    = 1e+20

    def load_nc(self, varName, Year, Mon, compressed=True):
        if varName[:5] in ["Rainf","Snowf"]:
            srcDir = self.baseDir + "/%s_WFDEI_%s"%(varName[:5], varName[6:])
            srcPath = srcDir + "/%s_WFDEI_%s_%04d%02d.nc"%(varName[:5], varName[6:], Year, Mon)
        else:
            srcDir = self.baseDir + "/%s_WFDEI"%(varName)
            srcPath = srcDir + "/%s_WFDEI_%04d%02d.nc"%(varName,Year,Mon)

        #if compressed==True:
        #    srcPath = srcPath + ".gz"
        #    tmpPath = self.tempDir + "/%s_%04d%02d.nc"%(varName,Year,Mon)
        #    cmd = "gunzip -c %s > %s"%(srcPath, tmpPath)
        #    subprocess.call(cmd, shell=True)
        #    nc  = Dataset(tmpPath, "r", format="NETCDF")
        #    os.remove(tmpPath)

        if compressed==True:
            ''' available for netCDF4 v1.2.8 or later'''
            srcPath = srcPath + ".gz"
            with gzip.open(srcPath) as gz:
                nc = Dataset('dummy', mode='r', memory=gz.read())
                return nc


        else:
            nc  = Dataset(srcPath, "r", format="NETCDF")

        return nc 

