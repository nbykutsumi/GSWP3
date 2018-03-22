import matplotlib as mpl
mpl.use("Agg")
import WFDEI
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import calendar
from datetime import datetime, timedelta
import sys, os

dvarLocal = {"SWdown":"SWdown"
            ,"LWdown":"LWdown"
            ,"Rainf":"Rainf_CRU"
            ,"Snowf":"Snowf_CRU"
            ,"Wind":"Wind"
            ,"Tair":"Tair"
            ,"Qair":"Qair"
            ,"PSurf":"PSurf"
            }

prjName   = "WFDEI"
#lvarName = ["SWdown"]
#lvarName = ["LWdown"]
#lvarName = ["SWdown","LWdown","Rainf","Snowf","Wind","Tair","Qair","PSurf"]
lvarName = ["Rainf","Snowf","Wind","Tair","Qair","PSurf"]
baseDir = "/work/a01/utsumi/GSWP3"
#calFlag = False
calFlag = True
per_day = 8 # [#/days] (3-hour-step)
#iYear = 1956
iYear = 1979
#iYear = 2000
eYear = 2016
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
miss_in   = 1.00000002e+20
miss_out  = -9999.
wf    = WFDEI.WFDEI()
ny    = wf.ny
nx    = wf.nx


for varName in lvarName:
    for Year in lYear:
        varLocal = dvarLocal[varName]

        a3mon = empty([12,ny,nx])
        for iMon,Mon in enumerate(range(1,12+1)):
            ncIn  = wf.load_nc(varName=varLocal, Year=Year, Mon=Mon, compressed=True)
            a3in  = ncIn.variables[varName][:].reshape(-1,ny,nx)
            a3mon[iMon] = ma.masked_equal(a3in, miss_in).mean(axis=0)
    
        a3mon = concatenate([a3mon[:,:,nx/2:], a3mon[:,:,:nx/2]], axis=2)

        if ma.isMaskedArray(a3mon)==True:
            a3mon = a3mon.filled(miss_out) 

        # save
        #outDir = baseDir + "/TimeLat"
        outDir = baseDir + "/Mon/%s"%(prjName)
        util.mk_dir(outDir)
        outPath= outDir + "/%s.%s.MonMap.%04d.npy"%(prjName, varName, Year)
        np.save(outPath, a3mon)
        print outPath
    
