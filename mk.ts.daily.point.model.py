from numpy import *
from datetime import datetime, timedelta
import calendar
import myfunc.util as util
import glob
import sys
import numpy as np

lprjName = ['GSWP3','PRINCETON','WFDEI','CRUNCEP']
#lprjName = ['PRINCETON']
lvarName = ["Rainf","Snowf","SWdown","LWdown","Tair","Qair","PSurf","Prcp","Wind"]
rootDir  = '/work/a01/utsumi/GSWP3/insitu'
orootDir = '/work/a01/utsumi/GSWP3/insitu_daily'
miss_out = -9999.
for varName in lvarName:
    for prjName in lprjName:
        if prjName in ['GSWP3']:
            tstp = 3  # hour
            tstpType = 'pre'
        elif prjName in ['PRINCETON']:
            tstp = 3  # hour
            tstpType = 'aft'
        elif prjName in ['WFDEI']:
            tstp = 3  # hour
            tstpType = 'pre'
        elif prjName in ['CRUNCEP']:
            tstp = 6  # hour
            tstpType = 'aft'
        else:
            print 'check prjName',prjName
            sys.exit()

        ssearch = rootDir + '/%s'%(varName)
        lbaseDir = sort(glob.glob(ssearch))
        for baseDir in lbaseDir:
            ssearch = baseDir + '/*'
            lsrcDir= glob.glob(ssearch)
            for srcDir in lsrcDir:
                siteName = srcDir.split('/')[-1]
                ssearch  = srcDir + '/%s.*.npy'%(prjName)
                lsrcPath = glob.glob(ssearch)
                for srcPath in lsrcPath:
                    print srcPath
                    Year = int(srcPath.split('.')[-2])
                    if calendar.isleap(Year):
                        nday = 366
                    else:
                        nday = 365

                    a1in = np.load(srcPath)
                    if tstpType=='pre':
                        a1inTmp = a1in[1:]
                        a1linTmp= concatenate([a1inTmp, array([miss_out])])
                    elif tstpType=='aft':
                        a1inTmp = a1in 
 
                    a1daily = ma.masked_equal(a1in, miss_out).reshape(-1,int(24/tstp)).mean(axis=1).filled(miss_out)

                        
                    if tstpType=='pre':
                        a1daily[-1] = miss_out
                   
 
                    #print a1daily
                    #print calendar.isleap(Year)
                    #print a1daily.shape


                    outDir  = orootDir + '/%s/%s'%(varName, siteName)
                    outPath = outDir + '/%s.day.%04d.npy'%(prjName, Year)
                    print outPath
                    util.mk_dir(outDir)
                    np.save(outPath, a1daily) 
                    #sys.exit()
