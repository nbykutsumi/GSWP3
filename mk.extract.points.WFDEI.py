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
#lvarName = ["Rainf"]
#lvarName = ["Tair"]
lvarName = ["SWdown","LWdown","Rainf","Snowf","Wind","Tair","Qair","PSurf"]
#lvarName = ["Qair","PSurf"]
baseDir = "/work/a01/utsumi/GSWP3/insitu"
tstp   = '3hr'
#iYear = 1956
#iYear = 1979
#eYear = 2016

iYear = 1980 # common
eYear = 2010 # common

#iYear = 2003 # common
#eYear = 2003 # common

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

#-------------------
# Forcing ----------
miss_in   = 1.00000002e+20
miss_out  = -9999.
wf    = WFDEI.WFDEI()
ny    = wf.ny
nx    = wf.nx

a1latbnd = wf.LatBnd
a1lonbnd = wf.LonBnd
latbnd0  = a1latbnd[0]
lonbnd0  = a1lonbnd[0]
dlat     = 0.5
dlon     = 0.5
lsiteName= dlatlon.keys()

#-------------------
for varName in lvarName:
    for Year in lYear:
        #if (varName=="Qair")&(Year<2007):continue
        varLocal = dvarLocal[varName]

        if calendar.isleap(Year):
            nDay = 366
        else:
            nDay = 365
        a3in = empty([nDay*8,ny,nx])

        for iMon,Mon in enumerate(range(1,12+1)):
            eDay   = calendar.monthrange(Year,Mon)[1]
            dtime0 = datetime(Year,Mon,1)
            dtime1 = datetime(Year,Mon,eDay)
            doy0  = util.ret_day_of_year(dtime0)
            doy1  = util.ret_day_of_year(dtime1)

            ncIn  = wf.load_nc(varName=varLocal, Year=Year, Mon=Mon, compressed=True)
            a3in[(doy0-1)*8:(doy1-1)*8+8,:,:] = ncIn.variables[varName][:].reshape(-1,ny,nx).data



        for siteName in lsiteName:
            lat,lon = dlatlon[siteName]
            y = int((lat -latbnd0)/dlat)
            x = int((lon -lonbnd0)/dlon)

            a1dat = a3in[:,y,x]

            # save
            outDir = baseDir + "/%s/%s"%(varName,siteName)
            util.mk_dir(outDir)
            outPath= outDir + "/%s.%s.%04d.npy"%(prjName, tstp, Year)
            np.save(outPath, a1dat)
            print outPath

    
