import matplotlib as mpl
mpl.use("Agg")
import CRUNCEP
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import calendar
from datetime import datetime, timedelta
import os, sys

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
lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Qair","PSurf"] # w/o Tair
#lvarName = ["Wind","Qair","PSurf"]
#lvarName = ["Wind"]
#lvarName = ["SWdown"]
baseDir = "/work/a01/utsumi/GSWP3"
#calFlag = False
calFlag = True
#calctype= 'mean'   # mean, sum, std
calctype = 'std'

per_day = 4 # [#/days] (6-hour-step)
#iYear = 1978
#eYear = 1984
iYear = 2009
eYear = 2014

#eYear = 2014
#iYear = 1979  # common
#eYear = 2010  # common

lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
cru   = CRUNCEP.CRUNCEP()
ny    = cru.ny
nx    = cru.nx
miss_in   = cru.miss  # -9.99999979e+33
miss_out  = -9999.


for Year in lYear:
    for varName in lvarName:
        #if (varName=="Wind")&(Year<1982):continue
        if varName=="Wind":
            varLocal1 = dvarLocal["uwind"]
            varNC1    = CRUNCEP.ret_varNC(varLocal1)
            varLocal2 = dvarLocal["vwind"]
            varNC2    = CRUNCEP.ret_varNC(varLocal2)

            ncIn1  = cru.load_nc(varName=varLocal1, Year=Year, compressed=True)
            a3in1  = ncIn1.variables[varNC1][:].reshape(-1,ny,nx)
            a3in1  = ma.masked_equal(a3in1, miss_in)

            ncIn2  = cru.load_nc(varName=varLocal2, Year=Year, compressed=True)
            a3in2  = ncIn2.variables[varNC2][:].reshape(-1,ny,nx)
            a3in2  = ma.masked_equal(a3in2, miss_in)

            a3in   = np.sqrt(np.square( a3in1 ) + np.square( a3in2 ))

            if   calctype=='mean':
                a3mon = util.nhourly2monthly(a3in, nh=6, calc=calctype, miss_in=miss_in, miss_out=miss_out)
            elif calctype=='std':
                a3mon = util.nhourly2day2monthly(a3in, nh=6, calc=calctype, miss_in=miss_in, miss_out=miss_out)
            else:
                print 'check calctype',calctype
                sys.exit()

        else:
            varLocal = dvarLocal[varName]
            varNC    = CRUNCEP.ret_varNC(varLocal)
            ncIn  = cru.load_nc(varName=varLocal, Year=Year, compressed=True)
            a3in  = ncIn.variables[varNC][:].reshape(-1,ny,nx)
            if   calctype=='mean':
                a3mon = util.nhourly2monthly(a3in, nh=6, calc=calctype, miss_in=miss_in, miss_out=miss_out)
            elif calctype=='std':
                a3mon = util.nhourly2day2monthly(a3in, nh=6, calc=calctype, miss_in=miss_in, miss_out=miss_out)
            else:
                print 'check calctype',calctype
                sys.exit()


        a3mon = a3mon[:,::-1,:]  # flipud
        a3mon = concatenate([a3mon[:,:,360:], a3mon[:,:,:360]], axis=2)

        if ma.isMaskedArray(a3mon)==True:
            a3mon = a3mon.filled(miss_out) 
        # save
        outDir = baseDir + "/Mon/%s"%(prjName)
        util.mk_dir(outDir)
        outPath= outDir + "/%s.%s.%s.MonMap.%04d.npy"%(prjName, varName, calctype, Year)
        np.save(outPath, a3mon)
        print outPath
    
