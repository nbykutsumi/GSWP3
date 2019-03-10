from numpy import *
import netCDF4
import myfunc.util as util
import glob
from datetime import datetime, timedelta
import sys

metaPath= '/work/a01/utsumi/GSWP3/insitu/SnowMIP_Menard_Essery_2019.tab'
srcDir = '/data1/hjkim/ESM-SnowMIP/forcing.1D'
ssearch  = srcDir + '/met*.nc'
#ssearch  = srcDir + '/met_gswp3c*.nc'
#ssearch  = srcDir + '/met_insitu*.nc'
lsrcPath = glob.glob(ssearch)
DTime0 = datetime(1900,1,1,0,0,0)
#-- Open metadata table --
dlat = {}
dlon = {}

f=open(metaPath,'r'); lines = f.readlines(); f.close()
for line in lines[33:]:
    line = line.split('\t')
    fileName = line[-1].split('/')[-1].strip()
    lat = line[1]
    lon = line[2]
    dlat[fileName] = lat
    dlon[fileName] = lon

#-- Open netCDF4 ---
lout = []
for srcPath in lsrcPath:
    fileName = srcPath.split('/')[-1]
    siteName = srcPath.split('/')[-1].split('_')[2]
    nc  = netCDF4.Dataset(srcPath)
    #print nc.variables
    atime = nc.variables['time'][:]
#   
    iDTime = DTime0 + timedelta(seconds=int(atime[0]*60*60))
    eDTime = DTime0 + timedelta(seconds=int(atime[-1]*60*60))

    iYear,iMon,iDay,iHour,iMnt = iDTime.timetuple()[:5] 
    eYear,eMon,eDay,eHour,eMnt = eDTime.timetuple()[:5]

    lat  = dlat[fileName]
    lon  = dlon[fileName]
    ltmp = [fileName,lat,lon,iYear,iMon,iDay,iHour,iMnt,eYear,eMon,eDay,eHour,eMnt]
    lout.append(ltmp)

#-- Save ---

outDir  = '/work/a01/utsumi/GSWP3/insitu'
outPath = outDir + '/sitelist.SnowMIP.csv'
sout    = util.list2csv(lout)
f=open(outPath,'w'); f.write(sout); f.close()
print outPath

