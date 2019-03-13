import matplotlib
matplotlib.use('Agg')
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import calendar
import sys, os
import myfunc.util as util

lobsName = ['SnowMIP_gswp3c','PALS']
#lobsName = ['SnowMIP_gswp3c']
lprjName  = ['GSWP3','WFDEI','PRINCETON','CRUNCEP']
lvarName  = ["Prcp","SWdown","LWdown","Tair","Qair","PSurf","Wind"]
#lvarName  = ["Prcp"]
miss  = -9999.
#****************************************
def load_data(prjName, varName, siteName):
    if varName in ['Prcp']:
        if prjName =='GSWP3':
            srcPath1  = '/work/a01/utsumi/GSWP3/insitu_daily/Rainf/%s/GSWP3.day.%04d.npy'%(siteName,Year)
            srcPath2  = '/work/a01/utsumi/GSWP3/insitu_daily/Snowf/%s/GSWP3.day.%04d.npy'%(siteName,Year)
            a1dat1   = ma.masked_equal(np.load(srcPath1)   ,miss)
            a1dat2   = ma.masked_equal(np.load(srcPath2)   ,miss)
            a1dat    = a1dat1 + a1dat2

        elif prjName=='WFDEI':
            srcPath1 = '/work/a01/utsumi/GSWP3/insitu_daily/Rainf/%s/WFDEI.day.%04d.npy'%(siteName,Year)
            srcPath2 = '/work/a01/utsumi/GSWP3/insitu_daily/Snowf/%s/WFDEI.day.%04d.npy'%(siteName,Year)
            a1dat1   = ma.masked_equal(np.load(srcPath1)   ,miss)
            a1dat2   = ma.masked_equal(np.load(srcPath2)   ,miss)
            a1dat    = a1dat1 + a1dat2


        elif prjName=='PRINCETON':
            srcPath  = '/work/a01/utsumi/GSWP3/insitu_daily/Prcp/%s/PRINCETON.day.%04d.npy'%(siteName,Year)
            a1dat    = ma.masked_equal(np.load(srcPath)   ,miss)

        elif prjName=='CRUNCEP':
            srcPath    = '/work/a01/utsumi/GSWP3/insitu_daily/Prcp/%s/CRUNCEP.day.%04d.npy'%(siteName,Year)
            a1dat    = ma.masked_equal(np.load(srcPath)   ,miss)

        elif prjName=='SnowMIP_gswp3c':
            srcPath1   = '/work/a01/utsumi/GSWP3/insitu_daily/Rainf/%s/%s.day.%04d.npy'%(siteName,prjName,Year)
            srcPath2   = '/work/a01/utsumi/GSWP3/insitu_daily/Snowf/%s/%s.day.%04d.npy'%(siteName,prjName,Year)
            a1dat1   = ma.masked_equal(np.load(srcPath1)   ,miss)
            a1dat2   = ma.masked_equal(np.load(srcPath2)   ,miss)
            a1dat    = a1dat1 + a1dat2

        elif prjName=='PALS':
            srcPath    = '/work/a01/utsumi/GSWP3/insitu_daily/Rainf/%s/%s.day.%04d.npy'%(siteName,prjName,Year)
            a1dat    = ma.masked_equal(np.load(srcPath)   ,miss)
        else:
            print 'check prjName',prjName


    else:
        srcPath  = '/work/a01/utsumi/GSWP3/insitu_daily/%s/%s/%s.day.%04d.npy'%(varName, siteName, prjName, Year)
        a1dat    = ma.masked_equal(np.load(srcPath)   ,miss)

    
    if varName in ['Prcp','Rainf','Snowf']:   
        cgswp= cwfdei =cprince = 60*60*24  # mm/s --> mm/day
        ccru = 4  # mm/6hr -->mm/day
        cobs = 60*60*24  # mm/s -->mm/day
    elif varName in ['PSurf']:
        cgswp= cwfdei =cprince = 1.0
        ccru = 1.0
        cobs = 1.0
    elif varName in ['SWdown']:
        cgswp= cwfdei =cprince = 1.0
        ccru = 1./(60*60*6)
        cobs = 1.0


    else:
        cgswp= cwfdei =cprince = 1.0
        ccru = 1.0
        cobs = 1.0
  
  
    if   prjName =='GSWP3':
        c = cgswp
    elif prjName =='WFDEI':
        c = cwfdei
    elif prjName =='PRINCETON':
        c = cprince
    elif prjName =='CRUNCEP':
        c = ccru
    else:
        c = cobs
    a1dat = a1dat * c
    return a1dat
#****************************************
# SnowMip
#----------------------------------------

ltmp = ['variable','Network','site','lat','lon','iYear','eYear','mean_obs']
ltmp = ltmp + ['mean_%s'%(prjName) for prjName in lprjName]
ltmp = ltmp + ['rbias_%s'%(prjName) for prjName in lprjName]
ltmp = ltmp + ['cc_%s'%(prjName) for prjName in lprjName]
ltmp = ltmp + ['rmse_%s'%(prjName) for prjName in lprjName]
lout = [ltmp]
for varName in lvarName:
    for obsName in lobsName:
        if obsName == 'SnowMIP_gswp3c':
            listPath = '/work/a01/utsumi/GSWP3/insitu/sitelist.%s.csv'%('SnowMIP')
        elif obsName=='PALS':
            listPath = '/work/a01/utsumi/GSWP3/insitu/sitelist.%s.csv'%('PALS')

        else:
            print 'check obsName',obsName
            sys.exit()

        f=open(listPath,'r'); lines=f.readlines(); f.close()
    
        for line in lines:
            line = line.split(',')
            if obsName == 'SnowMIP_gswp3c':
                fileName = line[0]
                siteName = fileName.split('_')[2]
            elif obsName =='PALS':
                siteName = line[0]
            else:
                print 'check obsName',obsName
                sys.exit()

            lat  = float(line[1])
            lon  = float(line[2])
            iYear= int(line[3])
            eYear= int(line[8])
            if eYear > 2010:
                eYear = 2010
        
            if siteName[:10]=='met_insitu':
                continue
    
            dmean = {}
            dcc   = {}
            drmse = {}
            drbias= {}
            #-- Read Observation --- 
            a1obs = []
            for Year in range(iYear,eYear+1):
                a1tmp = load_data(obsName,varName,siteName)
                a1obs = concatenate([a1obs, a1tmp])
            a1obs = ma.masked_equal(a1obs, miss)
    
            dmean[obsName] = a1obs.mean() 
    
            for prjName in lprjName:
                a1dat = []
                for Year in range(iYear,eYear+1):
                    leapFlag=calendar.isleap(Year)
                    a1tmp = load_data(prjName,varName,siteName)
    
                    #-- Insert Feb. 29 ---
                    if (prjName=='CRUNCEP')&(leapFlag):
                        a1tmp = concatenate([a1tmp[:31+28],[miss],a1tmp[31+28:]])
                    #---------------------
                    a1dat = concatenate([a1dat, a1tmp])
                a1dat = ma.masked_equal(a1dat,miss)
   
                print varName, obsName, siteName,prjName,len(a1obs),len(a1dat)
                #-- Metrics -- 
                mean  = a1dat.mean()
                cc    = np.ma.corrcoef(a1obs,a1dat, allow_masked=True)[0,1]
                rmse  = np.sqrt( ((a1dat - a1obs)**2).mean() )
                rbias = (a1dat.mean() - a1obs.mean())/a1obs.mean()

                dmean [prjName] = mean
                dcc   [prjName] = cc
                drmse [prjName] = rmse
                drbias[prjName] = rbias 
   
            #-- Make string line --
            ltmp = [varName,obsName,siteName,lat,lon,iYear,eYear]
            ltmp = ltmp + [dmean[obsName]]
            ltmp = ltmp + [dmean [prjName] for prjName in lprjName]
            ltmp = ltmp + [drbias[prjName] for prjName in lprjName]
            ltmp = ltmp + [dcc   [prjName] for prjName in lprjName]
            ltmp = ltmp + [drmse [prjName] for prjName in lprjName]


            lout.append(ltmp)

#-- Save ---
sout = util.list2csv(lout)
outPath = '/work/a01/utsumi/GSWP3/insitu/metric.point.csv'
f = open(outPath,'w'); f.write(sout); f.close()
print outPath
