from numpy import *
from datetime import datetime, timedelta
import calendar
import myfunc.util as util
import sys, os
import numpy as np

#lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]
lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]

#lYear = range(1901,2010)
lYear = range(1901,2010)
lMon = range(1,12+1)

def ret_day_of_year(DTime):
    Year   = DTime.year
    DTime0 = datetime(Year,1,1,0)
    dDTime = DTime - DTime0
    return dDTime.days + 1

def ret_iday_eday_of_year(Year,Mon):
    ndays  = calendar.monthrange(Year,Mon)[1]
    DTime0 = datetime(Year,1,1,0)
    iDTime = datetime(Year,Mon,1,0)
    eDTime = datetime(Year,Mon,ndays,0) 
    idoy   = (iDTime - DTime0).days + 1
    edoy   = (eDTime - DTime0).days + 1
    return idoy, edoy

#-- Read APHRO_JP ------
dap = {}
for Year in lYear:
    prjName = 'APHRO_JP'
    srcDir  = '/work/a01/utsumi/GSWP3/VS_APHRO_JP/%s'%(prjName)
    srcPath = srcDir + '/prcp.daily.JPN.%s.%04d.csv'%(prjName,Year)
    f=open(srcPath,'r'); lines=f.readlines(); f.close()
    adat = map(float, lines)    

    for Mon in lMon:
        idoy,edoy = ret_iday_eday_of_year(Year,Mon)
        dap[Year,Mon] = adat[idoy-1:edoy]


#-- Read other models --
for prjName in lprjName:
    ddat = {}
    dcc  = {}
    for Year in lYear:
        srcDir  = '/work/a01/utsumi/GSWP3/VS_APHRO_JP/%s'%(prjName)
        srcPath = srcDir + '/prcp.daily.JPN.%s.%04d.csv'%(prjName,Year)
        if not os.path.exists(srcPath):
            print prjName,Year,'Skip'
            for Mon in lMon:
                dcc[Year,Mon] = None
        else:
            f=open(srcPath,'r'); lines=f.readlines(); f.close()
            adat = map(float, lines)
            
            for Mon in lMon:
                idoy,edoy = ret_iday_eday_of_year(Year,Mon)

                aap     = dap[Year,Mon]
                adatTmp = adat[idoy-1:edoy]

                if calendar.isleap(Year):
                    if (prjName=='CRUNCEP')&(Mon==2):
                        aap = aap[:-1]
                    elif (prjName=='CRUNCEP')&(Mon>2):
                        adatTmp = adat[idoy-2:edoy-1]

                print prjName,Year,Mon,len(dap[Year,Mon]),len(adatTmp)
                dcc [Year,Mon] = np.corrcoef(adatTmp, dap[Year,Mon])[0,1]

    #-- Output data --
    lout = []
    for Year in lYear:
        for Mon in lMon:
            lout.append([Year,Mon,dcc[Year,Mon]])
    sout = util.list2csv(lout) 
    #-- Save files --
    outDir  = '/work/a01/utsumi/GSWP3/VS_APHRO_JP/cc'
    util.mk_dir(outDir)
    outPath = outDir + '/cc.%s.csv'%(prjName)
    f=open(outPath,'w'); f.write(sout); f.close()
    print outPath 
 
    
