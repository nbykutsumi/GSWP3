import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


from numpy import *
import GSWP3
import CRUNCEP
import PRINCETON
import WFDEI
from datetime import datetime, timedelta
import myfunc.util as util
import numpy as np
import calendar
import sys


#lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]
#lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]
#lprjName = ["CRUNCEP","WFDEI"]
#lprjName = ["GSWP3","PRINCETON"]
lprjName = ["WFDEI"]

lYear = range(1901,2014+1)

def ret_day_of_year(DTime):
    Year   = DTime.year
    DTime0 = datetime(Year,1,1,0)
    dDTime = DTime - DTime0
    return dDTime.days + 1



for prjName in lprjName:

    if prjName =='GSWP3':
        iYear,eYear = 1901,2014
        ny,nx   = 360,720
        per_day = 8
        gswp = GSWP3.GSWP3()
        gswp(expr='EXP1')
        coef  = 60*60*24.  # mm/sec --> mm/day

    elif prjName =='CRUNCEP':
        iYear,eYear = 1901,2014
        ny,nx   = 360,720
        per_day = 4
        cru   = CRUNCEP.CRUNCEP()
        coef  = 4.0   # mm/6hr --> mm/day

    elif prjName =='PRINCETON':
        iYear,eYear = 1948,2010
        ny,nx   = 180,360
        pre_day = 8
        pg    = PRINCETON.PRINCETON()
        coef  = 60*60*24.  # mm/sec --> mm/day

    elif prjName in ['WFDEI']:
        iYear,eYear = 1979,2016
        ny,nx   = 360,720
        per_day = 8
        wf    = WFDEI.WFDEI()
        coef  = 60*60*24.  # mm/sec --> mm/day

    elif prjName in ['APHRO_JP']:
        iYear,eYear = 1900,2014   


    for Year in lYear:
        if (Year<iYear)or(eYear<Year):
            print prjName,Year,'Skip'
            continue

        if prjName =='GSWP3':
            ncIn  = gswp.load_nc(varName='Rainf', Year=Year)
            a3rain  = ncIn.variables['Rainf'][:]
            ncIn  = gswp.load_nc(varName='Snowf', Year=Year)
            a3snow  = ncIn.variables['Snowf'][:]
            a3in    = (ma.masked_less(a3rain,0) + ma.masked_less(a3snow,0)).data
            a3day = ma.masked_less(a3in.reshape(-1,per_day,ny,nx),0).mean(axis=1)

        elif prjName =='CRUNCEP':
            ''' crd='np', unit=mm/6hr '''
            ncIn  = cru.load_nc(varName='rain', Year=Year, compressed=True)
            a3in  = ncIn.variables['Total_Precipitation'][:].reshape(-1,ny,nx)
            a3in  = concatenate([a3in[:,::-1,nx/2:], a3in[:,::-1,:nx/2]],axis=2)
            a3day = ma.masked_less(a3in.reshape(-1,per_day,ny,nx),0).mean(axis=1)

        elif prjName =='PRINCETON':
            ncIn  = pg.load_nc(varName='prcp', Year=Year)
            a3in  = ncIn.variables['prcp'][:].reshape(-1,ny,nx)
            a3day = ma.masked_less(a3in.reshape(-1,per_day,ny,nx),0).mean(axis=1)

        elif prjName == 'WFDEI':
            ndays = ret_day_of_year(datetime(Year,12,31))
            a3day = zeros([ndays,ny,nx], float32) 

            for Mon in range(1,12+1):
                eDay = calendar.monthrange(Year,Mon)[1]
                idtime = datetime(Year,Mon,1,0)
                edtime = datetime(Year,Mon,eDay,0)
                idoy   = ret_day_of_year(idtime)
                edoy   = ret_day_of_year(edtime)
                ik     = (idoy-1)
                ek     = (edoy-1+1)

                ncIn  = wf.load_nc(varName='Rainf_CRU', Year=Year, Mon=Mon, compressed=True)
                a3rain= ncIn.variables['Rainf'][:].reshape(-1,ny,nx)
     
                ncIn  = wf.load_nc(varName='Snowf_CRU', Year=Year, Mon=Mon, compressed=True)
                a3snow= ncIn.variables['Snowf'][:].reshape(-1,ny,nx)
                a3in  = (ma.masked_equal(a3rain,1e+20) + ma.masked_equal(a3snow,1e+20)).data

                a3day[ik:ek,:,:] = ma.masked_equal(a3in.reshape(-1,per_day,ny,nx),1e+20).mean(axis=1)
            a3day = concatenate([a3day[:,:,nx/2:], a3day[:,:,:nx/2]],axis=2)  # sp --> na

        #-- Read JP mask ---
        maskDir = '/work/a01/utsumi/GSWP3/VS_APHRO_JP/mask'
        maskPath= maskDir + '/mask_aphrojp_%s.npy'%(prjName)
        a2mask  = np.load(maskPath)



        #-- Areal mean -----
        lout = []
        for iday in range(a3day.shape[0]):
            if prjName in ['APHRO_JP',"GSWP3","PRINCETON","CRUNCEP"]:
                a2in = ma.masked_less(a3day[iday],0)
            elif prjName in ['WFDEI']:
                a2in = ma.masked_equal(a3day[iday],1e+20)

            vout = ma.masked_where(a2mask==-9999.,a2in).mean()
            vout = vout * coef  # mm/day
            lout.append(vout)

        sout = util.list2csv(lout)
        #-- Areal mean --
        outDir = '/work/a01/utsumi/GSWP3/VS_APHRO_JP/%s'%(prjName)
        util.mk_dir(outDir)
        outPath= outDir + '/prcp.daily.JPN.%s.%04d.csv'%(prjName,Year)
        f=open(outPath,'w'); f.write(sout); f.close()
        print outPath


        #-- test figure --
        plt.imshow(a3day[0], origin='lower')
        plt.colorbar()
        plt.savefig('/work/a01/utsumi/GSWP3/VS_APHRO_JP/%s/temp.png'%(prjName))
        plt.clf()




