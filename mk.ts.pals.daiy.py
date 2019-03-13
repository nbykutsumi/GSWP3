from numpy import *
from datetime import datetime, timedelta
import myfunc.util as util
import calendar
import glob
import netCDF4
import sys
import numpy as np

prjName= 'PALS'
srcDir = '/work/data1/hjkim/PALS/1.4_met'
DTimeBase = datetime(2003,1,1,0,30,0)
obststp  = 0.5 # hour
ssearch  = srcDir + '/*'
lsrcPath = glob.glob(ssearch)
#iYear = 2003
#eYear = 2010
#iYear = 2004
#eYear = 2004

lYear = range(iYear,eYear+1)
avetstp = 24  # output time step [hour]

#lvarName = ["Rainf","Snowf","SWdown","LWdown","Tair","Qair","PSurf","Prcp","Wind"]
lvarName = ["Rainf","SWdown","LWdown","Tair","Qair","PSurf","Wind"]

for srcPath in lsrcPath:
    siteName = srcPath.split('/')[-1].split('Fluxnet')[0]
    print srcPath
    print siteName
    nc  = netCDF4.Dataset(srcPath)
    atime = nc.variables['time'][:]

    for varName in lvarName:
        adat  = nc.variables[varName][:]
        try:
            aqc   = nc.variables[varName+'_qc'][:]
        except KeyError:
            aqc   = ones(len(adat),float32)*(-9999.)

        ndat  = len(adat)

        DTimeDat0 = DTimeBase + timedelta(seconds=atime[0])
        DTimeDat1 = DTimeBase + timedelta(seconds=atime[-1])

        for Year in lYear:
            iDTime = datetime(Year,1,1,0,0)        
            eDTime = datetime(Year,12,31,24-avetstp)
            dDTime = timedelta(hours=avetstp)
            lDTime = util.ret_lDTime(iDTime,eDTime,dDTime)
            aout    = ones(len(lDTime),float32)*(-9999.)
            aout_qc = ones(len(lDTime),float32)*(-9999.)
            for i,DTime in enumerate(lDTime):
                irec0  = (DTime - (DTimeDat0 -timedelta(seconds=1800))).total_seconds()/3600 / obststp
                irec0  = int(irec0)
                irec1  = irec0 + int(avetstp/obststp)
    
                #print DTime 
                if (irec0>=ndat)or(irec1<=0):
                    continue
    
                dat = adat[irec0:irec1].mean()
                qc  = aqc [irec0:irec1].mean()
                if qc==1:
                    aout[i] = dat
                else:
                    aout[i] = -9999.

                #print irec0,irec1
                #print adat[irec0:irec1]
                #print dat
                #sys.exit()   
            print Year, len(aout) 
            #-- Save ---
            #outDir = '/work/a01/utsumi/GSWP3/insitu_daily/Tair/Amplero'
            outDir = '/work/a01/utsumi/GSWP3/insitu_daily/%s/%s'%(varName, siteName)
            outPath= outDir + '/%s.day.%04d.npy'%(prjName, Year)
            #dtime0 = DTimeBase + timedelta(seconds=atime[irec0])
            #dtime1 = DTimeBase + timedelta(seconds=atime[irec1])
            #print dtime0,dtime1
            #print adat[irec0:irec1]
            #print adat[irec0:irec1].mean()
            #print aout[:3]
            #print aout[-3:]
            np.save(outPath,aout.astype(float32))
            print outPath
