from numpy import *
import numpy as np
import os, sys
from netCDF4 import Dataset
import gzip

def convert_to_a2sa(a2in):
    a2in = np.flipud(a2in)
    return concatenate([a2in[:,360:],a2in[:,:360]],axis=1)


def ret_varNC(varName):
    dvar = {
            "swdown":"Incoming_Short_Wave_Radiation"
            ,"lwdown":"Incoming_Long_Wave_Radiation"
            ,"rain":"Total_Precipitation"
            ,"wind":""
            ,"uwind":"U_wind_component"
            ,"vwind":"V_wind_component"
            ,"tair":"Temperature"
            ,"qair":"Air_Specific_Humidity"
            ,"press":"Pression"
            }
    return dvar[varName]
    


class CRUNCEP(object):
    def __init__(self):
        #self.baseDir = "/data2/hjkim/CRUNCEP"
        self.baseDir = "/work/hk01/CRUNCEP"
        self.Lat     = arange(89.75,-89.75-0.001,-0.5)
        self.Lon     = arange(-179.75,179.75+0.001,0.5)
        self.LatBnd  = arange(90,-90-0.01,-0.5)
        self.LonBnd  = arange(-180,180+0.01, 0.5)

        self.ny      = len(self.Lat)
        self.nx      = len(self.Lon)
        self.miss    =  -9.99999979e+33

    def load_nc(self, varName, Year, compressed=True):
        srcDir  = self.baseDir + "/%s"%(varName)
        if compressed == True:
            ''' available for netCDF4 v1.2.8 or later'''
            srcPath = srcDir + "/cruncepv9_%s_%04d.nc.gz"%(varName, Year)
            with gzip.open(srcPath) as gz:
                nc = Dataset('dummy', mode='r', memory=gz.read())
                return nc

        else:
            srcPath = srcDir + "/cruncepv9_%s_%04d.nc"%(varName, Year)
            print srcPath
            nc = Dataset(srcPath, "r", format="NETCDF")

        return nc
        
