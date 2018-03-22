from numpy import *
import numpy as np
import os, sys
from netCDF4 import Dataset


lvarName = ["Rainf"]
lYear    = [2014]

for varName in lvarName:
    for Year in lYear:
        # read attributes from sample file
        YearTmp    = 1995
        srcDir  = "/data2/hjkim/GSWP3/in/EXP1/%s"%(varName)
        srcPath = srcDir + "/GSWP3.BC.%s.3hrMap.%04d.nc"%(varName, YearTmp)
        
        ncIn = Dataset(srcPath, "r", format="NETCDF4")
       
        # open output file
        outPath = "./temp.%s.%04d.nc"%(varName,Year)
        ncOut= Dataset(outPath, "r+", format="NETCDF4")


        # copy variable attributes 
        '''
        SKIP "_FillValue" for varName
        '''
        for v_name, varin in ncIn.variables.iteritems():
            for attr in varin.ncattrs():
                if ((v_name==varName)&(attr=="_FillValue")):continue

                #print v_name, attr
                ncOut.variables[v_name].setncattr(attr, varin.getncattr(attr))


        #ncOut.variables[varName].setncattr("_FillValue", varin.getncattr("_FillValue"))
        #ncOut.variables[varName].setncattr("FillValue",np.float32(1.0) )


 
        # get global attributes
        Attr = {}
        for attr in ncIn.ncattrs():
            Attr[attr] = ncIn.getncattr(attr)
        
        # change contributors
        Attr["contributors"] = "Satoshi Watanabe, Eun-Chul Chang, Nobuyuki Utsumi, Kei Yoshimura, David Lawrence, Gilbert Compo, Hirabayashi Yukiko, James Famiglietti, and Taikan Oki"
        
        # set global attributes
        for attr in ncIn.ncattrs():
            #print attr
            ncOut.setncattr(attr, Attr[attr])
         
        # close and write file
        ncOut.close()
        print outPath
        
        
