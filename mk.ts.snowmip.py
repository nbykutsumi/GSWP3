from numpy import *
from datetime import datetime, timedelta
import myfunc.util as util
import calendar
import glob
import netCDF4
import sys
import numpy as np

prjName= 'SnowMIP'
srcDir = '/data1/hjkim/ESM-SnowMIP/forcing.1D'
DTimeBase = datetime(1900,1,1,0,0,0)

obststp  = 1 # hour
ssearch  = srcDir + '/*.nc'
lsrcPath = sort(glob.glob(ssearch))
#iYear = 2003
iYear = 1980
eYear = 2010
lYear = range(iYear,eYear+1)
ltstp = [3,6]  # hour
lavetype = ['pre','cnt']

#lvarName = ["Rainf","Snowf","SWdown","LWdown","Tair","Qair","PSurf","Prcp","Wind"]
lvarName = ["Rainf","Snowf","SWdown","LWdown","Tair","Qair","PSurf","Wind"]
#lvarName = ["Tair"]

for tstp in ltstp:
    for srcPath in lsrcPath:
        dattype  = srcPath.split('/')[-1].split('_')[1]
        siteName = srcPath.split('/')[-1].split('_')[2]
        obsYear0 = int(srcPath.split('/')[-1].split('_')[3])
        obsYear1 = int(srcPath.split('/')[-1].split('_')[4][:-3])
        print srcPath
        print siteName
        #print dattype
        #print obsYear0,obsYear1
        nc  = netCDF4.Dataset(srcPath)
        atime = nc.variables['time'][:]
    
        for varName in lvarName:
            adat  = nc.variables[varName][:]
            ndat  = len(adat)
    
            DTimeDat0 = DTimeBase + timedelta(hours=int(atime[0]))
            DTimeDat1 = DTimeBase + timedelta(hours=int(atime[-1]))
            #print DTimeDat0, DTimeDat1


            for avetype in lavetype:
                if avetype =='pre':
                    dhour0 = tstp
                    dhour1 = 0
                elif avetype =='cent':
                    dhour0 = tstp*0.5
                    dhour1 = tstp*0.5
      
                for Year in lYear:
                    if (Year<obsYear0)or(obsYear1<Year):
                        continue

                    iDTime = datetime(Year,1,1,0,0)        
                    eDTime = datetime(Year,12,31,24-tstp)
                    dDTime = timedelta(hours=tstp)
                    lDTime = util.ret_lDTime(iDTime,eDTime,dDTime)
            
                    aout = ones(len(lDTime),float32)*(-9999)
                    for i,DTime in enumerate(lDTime):
                        irec  = (DTime - DTimeDat0).total_seconds()/3600 / obststp
                        irec  = int(irec)
                        irec0 = irec - int(dhour0/obststp) +1
                        irec1 = irec + int(dhour1/obststp) +1
        
                        #print DTime, DTimeBase,irec
                        if (irec0>=ndat)or(irec1<=0):
                            continue
        
                        dat = adat[irec0:irec1].mean()
                        aout[i] = dat
        
                    #-- Save ---
                    outDir = '/work/a01/utsumi/GSWP3/insitu/Tair/Amplero'
                    outDir = '/work/a01/utsumi/GSWP3/insitu/%s/%s'%(varName, siteName)
                    outPath= outDir + '/%s_%s.%s.%dhr.%04d.npy'%(prjName, dattype, avetype, tstp, Year)

                    #dtime0 = DTimeBase + timedelta(hours=int(atime[irec0]))
                    #dtime1 = DTimeBase + timedelta(hours=int(atime[irec1]))
                    #print dtime0,dtime1
                    #print adat[irec0:irec1]
                    #print adat[irec0:irec1].mean()
                    #print aout[:3]
                    #print aout[-3:]
                    np.save(outPath,aout.astype(float32))
                    print outPath
                    #sys.exit()
