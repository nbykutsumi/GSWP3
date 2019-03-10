import matplotlib as mpl
mpl.use("Agg")
import GSWP3, PRINCETON, CRUNCEP
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import calendar
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
import gswp_func
from myfunc.regrid import Regrid

lprjName = ["GSWP3","PRINCETON","WFDEI","CRUNCEP"]
#lprjName = ["GSWP3","CRUNCEP"]

#lvarName = ["SWdown","LWdown"]
#lvarName = ["Prcp"]
#lvarName = ["SWdown","LWdown","Rainf","Snowf","Wind","Tair","Qair","PSurf"]
lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Qair","PSurf"]
#lvarName = ["Qair","PSurf"]
#lvarName = ["Tair"]
#lvarName = ["SWdown"]
#lseason  = ["ALL","DJF","MAM","JJA","SON"]
lseason = ["ALL"]
baseDir = "/work/a01/utsumi/GSWP3"
#iYear = 1901   # GSWP3
#iYear = 1956   # PRINCETON
#eYear = 2014

iYear = 1979   # all
eYear = 2010   # all

#iYear  = 1979
#eYear  = 1979

lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
nYear = len(lYear)
miss  = -9999.

lcalctype = ['mean','std']
#lcalctype = ['std']
#lcalctype = ['mean']


us = Regrid.UpScale()


for calctype in lcalctype:
    if calctype =='mean':
        vminmax = {"SWdown":[100,300], "LWdown":[100,400], "Prcp":[0,10], "Rainf":[0,10],"Snowf":[0,10],"Wind":[0,10], "Tair":[230,310], "Qair":[0.002, 0.02], "PSurf":[800,1020]}
    
        vminmax_dif = {"SWdown":[-20,20], "LWdown":[-20,20], "Prcp":[-1,1], "Rainf":[-1,1],"Snowf":[-1,1],"Wind":[-2,2], "Tair":[-3,3], "Qair":[-0.005, 0.005], "PSurf":[-100,100]}
    
    elif calctype=='std':
        vminmax = {"SWdown":[0,100], "LWdown":[0,50], "Prcp":[0,10], "Rainf":[0,10],"Snowf":[0,10],"Wind":[0,5], "Tair":[0,10], "Qair":[0, 0.004], "PSurf":[0,10]}
    
        vminmax_dif = {"SWdown":[-40,40], "LWdown":[-20,20], "Prcp":[-4,4], "Rainf":[-1,1],"Snowf":[-1,1],"Wind":[-2,2], "Tair":[-2,2], "Qair":[-0.002, 0.002], "PSurf":[-5,5]}
    
    
    for varName in lvarName:
    
        da2dat = {}
    
        for prjName in lprjName:
            if prjName in ["GSWP3","CRUNCEP","WFDEI"]:
                ny,nx   = 360,720
                Lat     = arange(-89.75,89.75+0.0001,0.5)
                Lon     = arange(0.25,359.75+0.0001,0.5)
                res     = "hlf"
            elif prjName in ["PRINCETON"]:
                ny,nx   = 180,360
                Lat     = arange(-89.5,89.5+0.0001,1.0)
                Lon     = arange(0.5,359.5+0.0001,1.0)
                res     = "one"
    
            # coeficients
            if (prjName=="CRUNCEP")&(varName in ["SWdown"]):
                coef = 1./(60*60*6)
    
            else:
                coef = 1.0
    
            a2orog= gswp_func.load_orog(res="one")
     
            a2all = zeros([ny,nx],float32)
            a2djf = zeros([ny,nx],float32)
            a2mam = zeros([ny,nx],float32)
            a2jja = zeros([ny,nx],float32)
            a2son = zeros([ny,nx],float32)
        
            for Year in lYear:
                print varName, prjName, Year
           
                if (varName=="Prcp")&(prjName in ["GSWP3","WFDEI"]):
                    srcDir  = baseDir + "/Mon/%s"%(prjName) 
                    srcPath1 = srcDir + "/%s.%s.%s.MonMap.%04d.npy"%(prjName, "Rainf", calctype, Year)
                    a3in1    = np.load(srcPath1)
                    a3in1    = ma.masked_equal(a3in1,miss)
    
    
                    srcPath2 = srcDir + "/%s.%s.%s.MonMap.%04d.npy"%(prjName, "Snowf", calctype, Year)
                    a3in2    = np.load(srcPath2)
                    a3in2    = ma.masked_equal(a3in2,miss)
    
                    a3in     = a3in1 + a3in2
    
                else: 
                    srcDir  = baseDir + "/Mon/%s"%(prjName) 
                    srcPath = srcDir + "/%s.%s.%s.MonMap.%04d.npy"%(prjName, varName, calctype, Year)
                    a3in    = np.load(srcPath)
                    a3in    = ma.masked_equal(a3in,miss)
    
    
                a2all   = a2all + a3in.mean(axis=0)
                a2djf   = a2djf + a3in[[0,1,11],:,:].mean(axis=0)
                a2mam   = a2mam + a3in[[2,3,4], :,:].mean(axis=0)
                a2jja   = a2jja + a3in[[5,6,7], :,:].mean(axis=0)
                a2son   = a2son + a3in[[8,9,10],:,:].mean(axis=0)
        
            a2all = a2all/nYear *coef
            a2djf = a2djf/nYear *coef    
            a2mam = a2mam/nYear *coef    
            a2jja = a2jja/nYear *coef    
            a2son = a2son/nYear *coef    
    
    
    
            #************************
            #for season in lseason:
            for season in ['ALL','DJF','MAM','JJA','SON']:
                if   season=="ALL":
                    a2dat = a2all
                elif season=="DJF":
                    a2dat = a2djf
                elif season=="MAM":
                    a2dat = a2mam
                elif season=="JJA":
                    a2dat = a2jja
                elif season=="SON":
                    a2dat = a2son
        
                if varName in ["Prcp","Rainf","Snowf"]:
                    if prjName =="CRUNCEP":
                        a2dat = a2dat * 4  # mm/6hr --> mm/day
                    else:
                        a2dat = a2dat *60*60*24   # mm/day
                elif varName=="PSurf":
                    a2dat = a2dat * 0.01
    
    
                # regrid to 1.0 degree
                if res=="hlf":
                    LatOrg = arange(-89.75,89.75+0.001, 0.5)
                    LonOrg = arange(0.25,359.75+0.001, 0.5)
                    LatUp  = arange(-89.5,89.5+0.001, 1.0)
                    LonUp  = arange(0.5,359.5+0.001, 1.0)
                    us(LatOrg, LonOrg, LatUp, LonUp, globflag=True)
                    a2dat = us.upscale(a2dat, pergrid=False, miss_in = -9999., miss_out=-9999.)
    
                # mask sea
                a2dat = ma.masked_where(a2orog==-999., a2dat)
    
                da2dat[prjName,season] = a2dat
    
        #""" 
        # Figure simple mean
        for season in lseason:
            for prjName in lprjName:
                for figtype in ["ref","dif"]:
                    if (prjName=="GSWP3")&(figtype=="dif"):
                        continue
    
                    if (prjName !="GSWP3")&(figtype=="ref"):
                        continue
    
                    if figtype =="ref":
                        a2dat = da2dat[prjName,season]
                        a2all = da2dat[prjName,'ALL']
                        a2djf = da2dat[prjName,'DJF']
                        a2mam = da2dat[prjName,'MAM']
                        a2jja = da2dat[prjName,'JJA']
                        a2son = da2dat[prjName,'SON']


                        vmin, vmax = vminmax[varName]
                        cmap = 'jet'
    
                    elif figtype=="dif":
                        a2dat = da2dat[prjName,season]-da2dat["GSWP3",season]
                        a2all = da2dat[prjName,'ALL']-da2dat["GSWP3",'ALL']
                        a2djf = da2dat[prjName,'DJF']-da2dat["GSWP3",'DJF']
                        a2mam = da2dat[prjName,'MAM']-da2dat["GSWP3",'MAM']
                        a2jja = da2dat[prjName,'JJA']-da2dat["GSWP3",'JJA']
                        a2son = da2dat[prjName,'SON']-da2dat["GSWP3",'SON']

                        vmin, vmax = vminmax_dif[varName]
                        cmap = 'RdBu_r'
    
                    a2dat = ma.masked_where(a2orog==-999., a2dat)
                    a2all = ma.masked_where(a2orog==-999., a2all)
                    a2djf = ma.masked_where(a2orog==-999., a2djf)
                    a2mam = ma.masked_where(a2orog==-999., a2mam)
                    a2jja = ma.masked_where(a2orog==-999., a2jja)
                    a2son = ma.masked_where(a2orog==-999., a2son)
 
    
                    fig   = plt.figure(figsize=(4,2.3))
                    #-- Map (range) --
                    a2fig = a2dat
                    ax1   = fig.add_axes([0.1,0.22,0.6,0.75])
                    LatOneBnd = arange(-90,90+0.001, 1.0)
                    LonOneBnd = arange(0,360+0.001, 1.0)
            
                    X,Y = meshgrid(LonOneBnd, LatOneBnd)
            
                    M   = Basemap(resolution="l", llcrnrlat=-90, llcrnrlon=0, urcrnrlat=90, urcrnrlon=360)
                    im  = M.pcolormesh(X,Y, a2fig, cmap=cmap, vmin=vmin, vmax=vmax)
            
                    M.drawcoastlines()
                    M.drawparallels(arange(-90,90+0.1,30), labels=[1,0,0,0], fontsize=8, linewidth=0.3)
                    M.drawmeridians(arange(-180,360+0.1,30), labels=[0,0,0,1], fontsize=8, linewidth=0.3, rotation=45)
            
                    # colorbar
                    axcbar = fig.add_axes([0.1,0.12,0.6, 0.05])
                    #plt.colorbar(im, orientation="horizontal", cax=axcbar, ticks=arange(vmin,vmax+0.001, 0.05))
                    plt.colorbar(im, orientation="horizontal", cax=axcbar)
            
                    # zoal mean
                    #ax2   = fig.add_axes([0.8,0.34,0.1,0.515])
                    ax2   = fig.add_axes([0.71,0.34,0.1,0.515])
                    ax2.yaxis.tick_right()
                    LatOne= arange(-89.5,89.5+0.001,1.0)
                    lim = []
                    #vmin, vmax = vminmax[varName]
    
                    #dat   = a2dat.mean(axis=1)
                    #im = ax2.plot(dat, LatOne, linewidth=0.8)

                    im = ax2.plot(a2all.mean(axis=1), LatOne, linewidth=1.0, color='k')
                    im = ax2.plot(a2djf.mean(axis=1), LatOne, linewidth=0.6, color='b')
                    im = ax2.plot(a2mam.mean(axis=1), LatOne, linewidth=0.6, color='g')
                    im = ax2.plot(a2jja.mean(axis=1), LatOne, linewidth=0.6, color='red')
                    im = ax2.plot(a2son.mean(axis=1), LatOne, linewidth=0.6, color='orange')


                    ax2.set_yticks([-60,-30,0,30,60]) 
                    ax2.set_ylim([-90,90]) 
                    ax2.set_xlim([vmin, vmax]) 
        
                    # title
                    stitle = "%s %s %s %s %s"%(calctype, figtype, prjName, varName, season)
                    plt.suptitle(stitle)
                    
                    # save
                    figDir  = baseDir + "/fig"
                    util.mk_dir(figDir)
                    figPath = figDir + "/map.zonal.%s.%s.%s.%s.%04d-%04d.%s.png"%(calctype, figtype, varName,prjName, iYear,eYear,season)
    
                    plt.savefig(figPath)
                    print figPath
    
    
           
