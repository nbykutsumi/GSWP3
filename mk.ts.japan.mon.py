from numpy import *
import myfunc.util as util
import numpy as np
import myfunc.regrid.Regrid as Regrid
import calendar

lYear = range(1901,2011+1)
#lYear = range(2010,2011+1)

LatOrg = arange(24.025,  24.025+0.05*440, 0.05)
LonOrg = arange(123.025, 123.025+0.05*460, 0.05)
LatUp  = arange(-89.75,89.75+0.001, 0.5)
LonUp  = arange(0.25, 359.75+0.0001, 0.5)

us = Regrid.UpScale()
us(LatOrg, LonOrg, LatUp, LonUp, globflag=False)

def total_days_year(Year):
    if calendar.isleap(Year):
        return 366
    else:
        return 365



loutMon = []
loutYear= []

for Year in lYear:
    print Year
    #-- Load Aphro_jp --
    apDir  = '/work/a01/utsumi/GSWP3/Mon/APHRO_JP'
    apPath = apDir + '/APHRO_JP.Prcp.mean.MonMap.%04d.npy'%(Year)
    a3apOrg= np.load(apPath)

    gsDir  = '/work/a01/utsumi/GSWP3/Mon/GSWP3'
    gsRainPath   = gsDir + '/GSWP3.Rainf.mean.MonMap.%04d.npy'%(Year)
    gsSnowPath   = gsDir + '/GSWP3.Snowf.mean.MonMap.%04d.npy'%(Year)

    a3gsSnow = np.load(gsSnowPath)
    a3gsRain = np.load(gsRainPath)
    a3gs     = ( ma.masked_less(a3gsSnow,0) + ma.masked_less(a3gsRain,0) ).data
    a3gs     = ma.masked_less(a3gs,0)*60*60*24 # mm/sec -->mm/day

    lMon   = range(1,12+1)

    a3apMask= zeros([12,360,720],float32)
    a3gsMask= zeros([12,360,720],float32)

    for iMon,Mon in enumerate(lMon):
        a2apOrg= a3apOrg[iMon]
        a2ap   = us.upscale(a2apOrg, pergrid=False, miss_in=-9999., miss_out=-9999.)
        a2mask = ma.masked_less(a2ap, 0).mask

        a2gs   = a3gs[iMon]
        a2gs   = ma.masked_where(a2mask, a2gs).filled(-9999.)

        a3apMask[iMon] = a2ap
        a3gsMask[iMon] = a2gs

        #- Calc monthly precip (mm/month) --
        ndays = calendar.monthrange(Year,Mon)[1]
        ap = ma.masked_less(a2ap, 0).mean() * ndays  # mm/day-->mm/month
        gs = ma.masked_less(a2gs, 0).mean() * ndays  # mm/day-->mm/month
        loutMon.append([Year,Mon,ap, gs])

    a3apMask = ma.masked_less(a3apMask, 0)
    a3gsMask = ma.masked_less(a3gsMask, 0)

    #- Calc annual precip (mm/yr)
    ndays = total_days_year(Year)
    ap = a3apMask.mean() * ndays  # mm/day --> mm/yr
    gs = a3gsMask.mean() * ndays  # mm/day --> mm/yr
    loutYear.append([Year,ap,gs])

#-- Save monthly --
loutMon = [['Year','Mon','APHRO_JP','GSWP3']] + loutMon
sout   = util.list2csv(loutMon)

outDir = '/work/a01/utsumi/GSWP3/ts_jp'
outPath= outDir + '/ts_jp.mon.csv'
f=open(outPath,'w'); f.write(sout); f.close()
print outPath


#-- Save annual --
loutYear = [['Year','APHRO_JP','GSWP3']] + loutYear
sout   = util.list2csv(loutYear)

outDir = '/work/a01/utsumi/GSWP3/ts_jp'
outPath= outDir + '/ts_jp.year.csv'
f=open(outPath,'w'); f.write(sout); f.close()
print outPath
