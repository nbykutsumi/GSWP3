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
lvarName = ["Rainf","Snowf","SWdown","LWdown","Tair","Qair","PSurf","Prcp","Wind"]
#lvarName = ["Wind"]
baseDir = "/work/a01/utsumi/GSWP3/insitu"
#calFlag = False
calFlag = True
#calctype = 'mean'  # mean, sum, std
calctype = 'std'  # mean, sum, std
per_day = 8 # [#/days] (3-hour-step)
tstp    = '3hr'
#iYear = 1901
#eYear = 2014
#iYear = 2003
#eYear = 2003
#iYear = 1981
iYear = 1980  # common
#eYear = 2010  # common
eYear = 1980  # common
lYear = range(iYear,eYear+1)
miss  = -9999.

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


# Forcing 
a1latbnd = gswp.LatBnd
a1lonbnd = gswp.LonBnd
latbnd0  = a1latbnd[0]
lonbnd0  = a1lonbnd[0]
dlat     = 0.5
dlon     = 0.5
lsiteName= dlatlon.keys()

for Year in lYear:
    for varName in lvarName:
        ncIn  = gswp.load_nc(varName=varName, Year=Year)
        a3in  = ncIn.variables[varName][:]

        for siteName in lsiteName:
            lat,lon = dlatlon[siteName]
            y = int((lat -latbnd0)/dlat)
            x = int((lon -lonbnd0)/dlon)

            a1dat = a3in[:,y,x].data

            # save
            outDir = baseDir + "/%s/%s"%(varName,siteName)
            util.mk_dir(outDir)
            outPath= outDir + "/%s.%s.%04d.npy"%(prjName, tstp, Year)
            np.save(outPath, a1dat)
            print outPath
        


    
