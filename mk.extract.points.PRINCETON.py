import PRINCETON
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import calendar
from datetime import datetime, timedelta
import sys

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
baseDir = "/work/a01/utsumi/GSWP3/insitu"
#calFlag = False
calFlag = True
#calctype= 'mean'  # mean, sum, std
calctype= 'std'  # mean, sum, std

per_day = 8 # [#/days] (3-hour-step)
#iYear = 1956
iYear = 2003
eYear = 2003

#iYear = 1980 # common
#eYear = 2010 # common
lYear = range(iYear,eYear+1)
miss  = -9999.

tstp  = '3hr'

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
pg    = PRINCETON.PRINCETON()
ny    = pg.ny
nx    = pg.nx

a1latbnd = pg.LatBnd
a1lonbnd = pg.LonBnd
latbnd0  = a1latbnd[0]
lonbnd0  = a1lonbnd[0]
dlat     = 1.0
dlon     = 1.0
lsiteName= dlatlon.keys()

print ny,nx
#-------------------
for Year in lYear:
    for varName in lvarName:
        varLocal = dvarLocal[varName]
        ncIn  = pg.load_nc(varName=varLocal, Year=Year)
        a3in  = ncIn.variables[varLocal][:].reshape(-1,ny,nx).data

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


