from numpy import *
import netCDF4
import myfunc.util as util
import glob
from datetime import datetime, timedelta
srcDir = '/work/data1/hjkim/PALS/1.4_met'
ssearch  = srcDir + '/*'
lsrcPath = glob.glob(ssearch)
DTime0 = datetime(2003,1,1,0,30,0)
lout = []
for srcPath in lsrcPath:
    siteName = srcPath.split('/')[-1].split('Fluxnet')[0]
    print siteName
    nc  = netCDF4.Dataset(srcPath)
    atime = nc.variables['time'][:]
    lat   = nc.variables['latitude'][:][0][0]
    lon   = nc.variables['longitude'][:][0][0]
   
    iDTime = DTime0 + timedelta(seconds=atime[0])
    eDTime = DTime0 + timedelta(seconds=atime[-1])
    print iDTime, eDTime
    iYear,iMon,iDay,iHour,iMnt = iDTime.timetuple()[:5] 
    eYear,eMon,eDay,eHour,eMnt = eDTime.timetuple()[:5]

    ltmp = [siteName,lat,lon,iYear,iMon,iDay,iHour,iMnt,eYear,eMon,eDay,eHour,eMnt]
    lout.append(ltmp)

#-- Save ---

outDir  = '/work/a01/utsumi/GSWP3/insitu'
outPath = outDir + '/sitelist.PASL.csv'
sout    = util.list2csv(lout)
f=open(outPath,'w'); f.write(sout); f.close()
print outPath

