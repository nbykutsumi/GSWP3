import matplotlib as mpl
mpl.use("Agg")
import CRUNCEP
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import calendar
from datetime import datetime, timedelta

dvarLocal = {"SWdown":"swdown"
            ,"LWdown":"lwdown"
            ,"Prcp":"rain"
            ,"uwind":"uwind"
            ,"vwind":"vwind"
            ,"Tair":"tair"
            ,"Qair":"qair"
            ,"PSurf":"press"
            }


prjName   = "CRUNCEP"
#lvarName = ["Wind"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
lvarName = ["SWdown","LWdown","Prcp","Wind","Qair","PSurf"]
#lvarName = ["PSurf"]
#lvarName = ["SWdown"]
baseDir = "/work/a01/utsumi/GSWP3"
#calFlag = False
calFlag = True
per_day = 4 # [#/days] (6-hour-step)
#iYear = 1956
#iYear = 1984
#iYear = 2010
#eYear = 2014
#iYear = 1901
iYear = 1901
eYear = 2014
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
miss  = -9999.
cru   = CRUNCEP.CRUNCEP()
ny    = cru.ny
nx    = cru.nx


for varName in lvarName:
    for Year in lYear:
        if varName=="Wind":
            varLocal1 = dvarLocal["uwind"]
            varNC1    = CRUNCEP.ret_varNC(varLocal1)
            varLocal2 = dvarLocal["vwind"]
            varNC2    = CRUNCEP.ret_varNC(varLocal2)

            ncIn1  = cru.load_nc(varName=varLocal1, Year=Year)
            a3in1  = ncIn1.variables[varNC1][:].reshape(-1,ny,nx)

            ncIn2  = cru.load_nc(varName=varLocal2, Year=Year)
            a3in2  = ncIn2.variables[varNC2][:].reshape(-1,ny,nx)

            a3in   = np.sqrt(np.square( a3in1 ) + np.square( a3in2 ))

            a3mon = util.nhourly2monthly(a3in, nh=6, calc="mean", miss=miss)


        else:
            varLocal = dvarLocal[varName]
            varNC    = CRUNCEP.ret_varNC(varLocal)
            ncIn  = cru.load_nc(varName=varLocal, Year=Year)
            a3in  = ncIn.variables[varNC][:].reshape(-1,ny,nx)
            a3mon = util.nhourly2monthly(a3in, nh=6, calc="mean", miss=miss)

        a3mon = a3mon[:,::-1,:]  # flipud
        a3mon = concatenate([a3mon[:,:,360:], a3mon[:,:,:360]], axis=2)

        if ma.isMaskedArray(a3mon)==True:
            a3mon = a3mon.filled(miss) 
        # save
        #outDir = baseDir + "/TimeLat"
        outDir = baseDir + "/Mon/%s"%(prjName)
        util.mk_dir(outDir)
        outPath= outDir + "/%s.%s.MonMap.%04d.npy"%(prjName, varName, Year)
        np.save(outPath, a3mon)
        print outPath
    
