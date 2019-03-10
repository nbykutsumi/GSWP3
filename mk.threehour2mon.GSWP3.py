import matplotlib as mpl
mpl.use("Agg")
import GSWP3
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import calendar
from datetime import datetime, timedelta
import sys, os


prjName= "GSWP3"
expr = "EXP1"
gswp = GSWP3.GSWP3()
gswp(expr=expr)

#lvarName = ["SWdown","LWdown"]
#lvarName = ['SWdown']
#lvarName = ["SWdown","LWdown", "Prcp","Wind","Tair","Qair","PSurf"]
#lvarName = ["Rainf","Snowf","SWdown","LWdown","Tair","Qair","PSurf","Prcp"]
lvarName = ["Tair"]
baseDir = "/work/a01/utsumi/GSWP3"
#calFlag = False
calFlag = True
#calctype = 'mean'  # mean, sum, std
calctype = 'std'  # mean, sum, std
per_day = 8 # [#/days] (3-hour-step)
#iYear = 1901
#eYear = 2014
iYear = 1979  # common
eYear = 2010  # common
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
miss  = -9999.

for varName in lvarName:
    for Year in lYear:
        ncIn  = gswp.load_nc(varName=varName, Year=Year)
        a3in  = ncIn.variables[varName][:]

        if calctype=='mean':
            a3mon = util.nhourly2monthly(a3in, nh=3, calc=calctype, miss_in=1e+20, miss_out=miss)
        elif calctype=='std':
            a3mon = util.nhourly2day2monthly(a3in, nh=3, calc=calctype, miss_in=1e+20, miss_out=miss)
        else:
            print 'check calctype',calctype
            sys.exit()


        if ma.isMaskedArray(a3mon)==True:
            a3mon = a3mon.filled(miss) 
        # save
        #outDir = baseDir + "/TimeLat"
        outDir = baseDir + "/Mon/GSWP3"
        util.mk_dir(outDir)
        outPath= outDir + "/%s.%s.%s.MonMap.%04d.npy"%(prjName, varName, calctype, Year)
        np.save(outPath, a3mon)
        print outPath



    
