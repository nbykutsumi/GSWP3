import matplotlib as mpl
mpl.use("Agg")
import PRINCETON
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import calendar
from datetime import datetime, timedelta

dvarLocal = {"SWdown":"dswrf"
            ,"LWdown":"dlwrf"
            ,"Prcp":"prcp"
            ,"Wind":"wind"
            ,"Tair":"tas"
            ,"Qair":"shum"
            ,"PSurf":"pres"
            }

prjName   = "PRINCETON"
#lvarName = ["SWdown","LWdown"]
lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
#lvarName = ["PSurf"]
#lvarName = ["SWdown"]
baseDir = "/work/a01/utsumi/GSWP3"
#calFlag = False
calFlag = True
#calctype= 'mean'  # mean, sum, std
calctype= 'std'  # mean, sum, std

per_day = 8 # [#/days] (3-hour-step)
#iYear = 1956
#iYear = 1948
#eYear = 2014

iYear = 1979
eYear = 2010

lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
miss  = -9999.
pg    = PRINCETON.PRINCETON()
ny    = pg.ny
nx    = pg.nx


for varName in lvarName:
    for Year in lYear:
        varLocal = dvarLocal[varName]
        ncIn  = pg.load_nc(varName=varLocal, Year=Year)
        a3in  = ncIn.variables[varLocal][:].reshape(-1,ny,nx)

        if calctype=='mean':
            a3mon = util.nhourly2monthly(a3in, nh=3, calc=calctype, miss_in=2e+20, miss_out=miss)
        elif calctype == 'std':
            a3mon = util.nhourly2day2monthly(a3in, nh=3, calc=calctype, miss_in=2e+20, miss_out=miss)
        else:
            print 'check calctype',calctype
            sys.exit()


        if ma.isMaskedArray(a3mon)==True:
            a3mon = a3mon.filled(miss) 
        # save
        #outDir = baseDir + "/TimeLat"
        outDir = baseDir + "/Mon/PRINCETON"
        util.mk_dir(outDir)
        outPath= outDir + "/%s.%s.%s.MonMap.%04d.npy"%(prjName, varName, calctype, Year)
        np.save(outPath, a3mon)
        print outPath
         
