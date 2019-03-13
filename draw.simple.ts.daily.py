import matplotlib
matplotlib.use('Agg')
from numpy import *
import numpy as np
import matplotlib.pyplot as plt

lvarName  = ["Prcp","SWdown","LWdown","Tair","Qair","PSurf","Wind"]
miss  = -9999.
#****************************************
# SnowMIP
#----------------------------------------
for varName in lvarName:
    if varName in ['Prcp']:
        gswpPath1  = '/work/a01/utsumi/GSWP3/insitu_daily/Rainf/cdp/GSWP3.day.2004.npy'
        gswpPath2  = '/work/a01/utsumi/GSWP3/insitu_daily/Snowf/cdp/GSWP3.day.2004.npy'

        wfdeiPath1 = '/work/a01/utsumi/GSWP3/insitu_daily/Rainf/cdp/WFDEI.day.2004.npy'
        wfdeiPath2 = '/work/a01/utsumi/GSWP3/insitu_daily/Snowf/cdp/WFDEI.day.2004.npy'

        princePath = '/work/a01/utsumi/GSWP3/insitu_daily/Prcp/cdp/PRINCETON.day.2004.npy'

        cruPath    = '/work/a01/utsumi/GSWP3/insitu_daily/Prcp/cdp/CRUNCEP.day.2004.npy'

        obsPath1   = '/work/a01/utsumi/GSWP3/insitu_daily/Rainf/cdp/SnowMIP_gswp3c.day.2004.npy'
        obsPath2   = '/work/a01/utsumi/GSWP3/insitu_daily/Snowf/cdp/SnowMIP_gswp3c.day.2004.npy'

        a1gswp1   = ma.masked_equal(np.load(gswpPath1)   ,miss)
        a1gswp2   = ma.masked_equal(np.load(gswpPath2)   ,miss)
        a1gswp    = a1gswp1 + a1gswp2

        a1wfdei1 = ma.masked_equal(np.load(wfdeiPath1)  ,miss)
        a1wfdei2 = ma.masked_equal(np.load(wfdeiPath2)  ,miss)
        a1wfdei  = a1wfdei1 + a1wfdei2

        a1prince = ma.masked_equal(np.load(princePath) ,miss)

        a1cru    = ma.masked_equal(np.load(cruPath)    ,miss)

        a1obs1   = ma.masked_equal(np.load(obsPath1)    ,miss)
        a1obs2   = ma.masked_equal(np.load(obsPath2)    ,miss)
        a1obs    = a1obs1 + a1obs2

    else:
        gswpPath  = '/work/a01/utsumi/GSWP3/insitu_daily/%s/cdp/GSWP3.day.2004.npy'%(varName)
        wfdeiPath = '/work/a01/utsumi/GSWP3/insitu_daily/%s/cdp/WFDEI.day.2004.npy'%(varName)
        princePath= '/work/a01/utsumi/GSWP3/insitu_daily/%s/cdp/PRINCETON.day.2004.npy'%(varName)
        cruPath   = '/work/a01/utsumi/GSWP3/insitu_daily/%s/cdp/CRUNCEP.day.2004.npy'%(varName)
        obsPath   = '/work/a01/utsumi/GSWP3/insitu_daily/%s/cdp/SnowMIP_gswp3c.day.2004.npy'%(varName)

        a1gswp   = ma.masked_equal(np.load(gswpPath)   ,miss)
        a1wfdei  = ma.masked_equal(np.load(wfdeiPath)  ,miss)
        a1prince = ma.masked_equal(np.load(princePath) ,miss)
        a1cru    = ma.masked_equal(np.load(cruPath)    ,miss)
        a1obs    = ma.masked_equal(np.load(obsPath)    ,miss)

    
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
  
    if varName=='Prcp':
        print a1obs         
    
    a1gswp   = a1gswp * cgswp
    a1wfdei  = a1wfdei * cwfdei
    a1prince = a1prince * cprince
    a1cru    = a1cru * ccru
    a1obs    = a1obs * cobs

    #--- Draw Figure -----
    nstep = 365
    x = arange(nstep)
    plt.plot(x, a1gswp[:nstep],'-',color='r', label='gswp')
    plt.plot(x, a1wfdei[:nstep],'-',color='b', label='wfdei')
    plt.plot(x, a1prince[:nstep],'-',color='g',label='princeton')
    plt.plot(x, a1cru[:nstep],'-',color='orange',label='cruncep')
    plt.plot(x, a1obs[:nstep],'--',color='k', label='snowmip')
   
    plt.legend() 
    plt.title('SnowMIP '+varName)
    outPath = '/work/a01/utsumi/GSWP3/insitu/SnowMIP.day.%s.png'%(varName)
    plt.savefig(outPath)
    plt.clf()
    print outPath
    
#****************************************
# SnowMIP
#----------------------------------------
for varName in lvarName:
    if varName in ['Prcp']:
        gswpPath1  = '/work/a01/utsumi/GSWP3/insitu_daily/Rainf/Amplero/GSWP3.day.2004.npy'
        gswpPath2  = '/work/a01/utsumi/GSWP3/insitu_daily/Snowf/Amplero/GSWP3.day.2004.npy'

        wfdeiPath1 = '/work/a01/utsumi/GSWP3/insitu_daily/Rainf/Amplero/WFDEI.day.2004.npy'
        wfdeiPath2 = '/work/a01/utsumi/GSWP3/insitu_daily/Snowf/Amplero/WFDEI.day.2004.npy'

        princePath = '/work/a01/utsumi/GSWP3/insitu_daily/Prcp/Amplero/PRINCETON.day.2004.npy'

        cruPath    = '/work/a01/utsumi/GSWP3/insitu_daily/Prcp/Amplero/CRUNCEP.day.2004.npy'

        obsPath    = '/work/a01/utsumi/GSWP3/insitu_daily/Rainf/Amplero/PALS.day.2004.npy'

        a1gswp1   = ma.masked_equal(np.load(gswpPath1)   ,miss)
        a1gswp2   = ma.masked_equal(np.load(gswpPath2)   ,miss)
        a1gswp    = a1gswp1 + a1gswp2

        a1wfdei1 = ma.masked_equal(np.load(wfdeiPath1)  ,miss)
        a1wfdei2 = ma.masked_equal(np.load(wfdeiPath2)  ,miss)
        a1wfdei  = a1wfdei1 + a1wfdei2

        a1prince = ma.masked_equal(np.load(princePath) ,miss)

        a1cru    = ma.masked_equal(np.load(cruPath)    ,miss)

        a1obs1   = ma.masked_equal(np.load(obsPath1)    ,miss)
        a1obs2   = ma.masked_equal(np.load(obsPath2)    ,miss)
        a1obs    = a1obs1 + a1obs2

    else:
        gswpPath  = '/work/a01/utsumi/GSWP3/insitu_daily/%s/Amplero/GSWP3.day.2004.npy'%(varName)
        wfdeiPath = '/work/a01/utsumi/GSWP3/insitu_daily/%s/Amplero/WFDEI.day.2004.npy'%(varName)
        princePath= '/work/a01/utsumi/GSWP3/insitu_daily/%s/Amplero/PRINCETON.day.2004.npy'%(varName)
        cruPath   = '/work/a01/utsumi/GSWP3/insitu_daily/%s/Amplero/CRUNCEP.day.2004.npy'%(varName)
        obsPath   = '/work/a01/utsumi/GSWP3/insitu_daily/%s/Amplero/PALS.day.2004.npy'%(varName)

        a1gswp   = ma.masked_equal(np.load(gswpPath)   ,miss)
        a1wfdei  = ma.masked_equal(np.load(wfdeiPath)  ,miss)
        a1prince = ma.masked_equal(np.load(princePath) ,miss)
        a1cru    = ma.masked_equal(np.load(cruPath)    ,miss)
        a1obs    = ma.masked_equal(np.load(obsPath)    ,miss)

    
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
  
    if varName=='Prcp':
        print a1obs         
    
    a1gswp   = a1gswp * cgswp
    a1wfdei  = a1wfdei * cwfdei
    a1prince = a1prince * cprince
    a1cru    = a1cru * ccru
    a1obs    = a1obs * cobs

    #--- Draw Figure -----
    nstep = 365
    x = arange(nstep)
    plt.plot(x, a1gswp[:nstep],'-',color='r', label='gswp')
    plt.plot(x, a1wfdei[:nstep],'-',color='b', label='wfdei')
    plt.plot(x, a1prince[:nstep],'-',color='g',label='princeton')
    plt.plot(x, a1cru[:nstep],'-',color='orange',label='cruncep')
    plt.plot(x, a1obs[:nstep],'--',color='k', label='pals')
   
    plt.legend() 
    plt.title('PALS '+varName)
    outPath = '/work/a01/utsumi/GSWP3/insitu/PALS.day.%s.png'%(varName)
    plt.savefig(outPath)
    plt.clf()
    print outPath
    

