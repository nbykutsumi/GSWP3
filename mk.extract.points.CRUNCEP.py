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
#lvarName = ["Tair"]
lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Qair","PSurf"] # w/o Tair
#lvarName = ["Wind","Qair","PSurf"]
#lvarName = ["Wind"]
#lvarName = ["SWdown"]
baseDir = "/work/a01/utsumi/GSWP3/insitu"

tstp    = '6hr'
#iYear = 2003
#eYear = 2003
iYear = 1980
eYear = 2010

#eYear = 2014
#iYear = 1979  # common
#eYear = 2010  # common

lYear = range(iYear,eYear+1)

#-- Read sitelist --
dlatlon = {}
# SnowMIP
srcPath = '/work/a01/utsumi/GSWP3/insitu/sitelist.SnowMIP.csv'
f = open(srcPath,'r'); lines=f.readlines(); f.close()
for line in lines:
    line = line.strip().split(',')
    fileName = line[0]
    siteName = fileName.split('_')[2]
    prjType  = fileName.split('_')[1]
    lat      = float(line[1])
    lon      = float(line[2])
    if prjType != 'gswp3c':
        continue

    dlatlon[siteName] = [lat,lon]

# PALS
srcPath = '/work/a01/utsumi/GSWP3/insitu/sitelist.PASL.csv'
f = open(srcPath,'r'); lines=f.readlines(); f.close()
for line in lines:
    line = line.strip().split(',')
    siteName = line[0]
    lat      = float(line[1])
    lon      = float(line[2])
    dlatlon[siteName] = [lat,lon]
#--------------------
# Forcing
cru   = CRUNCEP.CRUNCEP()
ny    = cru.ny
nx    = cru.nx
miss_in   = cru.miss  # -9.99999979e+33
miss_out  = -9999.

a1latbnd = cru.LatBnd
a1lonbnd = cru.LonBnd
latbnd0  = a1latbnd[-1]
lonbnd0  = a1lonbnd[0]
dlat     = 0.5
dlon     = 0.5
lsiteName= dlatlon.keys()



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


        else:
            varLocal = dvarLocal[varName]
            varNC    = CRUNCEP.ret_varNC(varLocal)
            ncIn  = cru.load_nc(varName=varLocal, Year=Year, compressed=True)
            a3in  = ncIn.variables[varNC][:].reshape(-1,ny,nx)


        for siteName in lsiteName:
            lat,lon = dlatlon[siteName]
            y = ny - 1 -int((lat -latbnd0)/dlat)
            x = int((lon -lonbnd0)/dlon)

            print lat,lon
            print y, x
            a1dat = a3in[:,y,x].data

            # save
            outDir = baseDir + "/%s/%s"%(varName,siteName)
            util.mk_dir(outDir)
            outPath= outDir + "/%s.%s.%04d.npy"%(prjName, tstp, Year)
            np.save(outPath, a1dat)
            print outPath

    
