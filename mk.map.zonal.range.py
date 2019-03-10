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

lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]
#lprjName = ["CRUNCEP"]

#lvarName = ["SWdown","LWdown"]
#lvarName = ["Prcp"]
#lvarName = ["SWdown","LWdown","Rainf","Snowf","Wind","Tair","Qair","PSurf"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
lvarName = ["SWdown","LWdown","Prcp","Wind","Qair"]
#lvarName = ["Qair","PSurf"]
#lvarName = ["PSurf"]
#lvarName = ["Wind"]
#lseason  = ["ALL","DJF","MAM","JJA","SON"]
lseason = ["ALL"]
baseDir = "/work/a01/utsumi/GSWP3"
#iYear = 1901   # GSWP3
#iYear = 1956   # PRINCETON
#eYear = 2014
iYear = 1979
eYear = 2010
#eYear = 1905
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
nYear = len(lYear)
miss  = -9999.

us = Regrid.UpScale()

vminmax = {"SWdown":[100,300], "LWdown":[100,400], "Prcp":[0,10], "Rainf":[0,10],"Snowf":[0,10],"Wind":[0,60], "Tair":[230,310], "Qair":[0.002, 0.02], "PSurf":[800,1020]}
for varName in lvarName:
    dla1dat = {"%s"%(season):[] for season in lseason}
    dla2dat = {"%s"%(season):[] for season in lseason}

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
                srcPath1 = srcDir + "/%s.%s.MonMap.%04d.npy"%(prjName, "Rainf", Year)
                a3in1    = np.load(srcPath1)
                a3in1    = ma.masked_equal(a3in1,miss)

                srcPath2 = srcDir + "/%s.%s.MonMap.%04d.npy"%(prjName, "Snowf", Year)
                a3in2    = np.load(srcPath2)
                a3in2    = ma.masked_equal(a3in2,miss)

                a3in     = a3in1 + a3in2

            else: 
                srcDir  = baseDir + "/Mon/%s"%(prjName) 
                srcPath = srcDir + "/%s.%s.MonMap.%04d.npy"%(prjName, varName, Year)
                a3in    = np.load(srcPath)
                a3in    = ma.masked_equal(a3in,miss)

            print "-"*50
            print a3in.min(), a3in.mean(), a3in.max()
            print "-"*50
 
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
        for season in lseason:
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
                print prjName, a2dat.shape
                LatOrg = arange(-89.75,89.75+0.001, 0.5)
                LonOrg = arange(0.25,359.75+0.001, 0.5)
                LatUp  = arange(-89.5,89.5+0.001, 1.0)
                LonUp  = arange(0.5,359.5+0.001, 1.0)
                us(LatOrg, LonOrg, LatUp, LonUp, globflag=True)
                a2dat = us.upscale(a2dat, pergrid=False, miss_in = -9999., miss_out=-9999.)

            # mask sea
            a2dat = ma.masked_where(a2orog==-999., a2dat)


            a1dat = a2dat.mean(axis=1)
            dla1dat[season].append(a1dat)
            dla2dat[season].append(a2dat)

    da3dat = {}
    for season in lseason:
        da3dat[season] = array(dla2dat[season]) # list to array
    #""" 
    # Figure 
    for season in lseason:
        fig   = plt.figure(figsize=(4,2.3))

        #-- Map (range) --
        ax1   = fig.add_axes([0.1,0.22,0.6,0.75])
        da3dat[season] = ma.masked_equal(da3dat[season], miss)
        #a2fig = da3dat[season].max(axis=0) - da3dat[season].min(axis=0)
        a2fig = da3dat[season].std(axis=0)
        a2fig = ma.masked_invalid(a2fig / da3dat[season].mean(axis=0))
        a2fig = ma.masked_where(a2orog==-999., a2fig)
        LatOneBnd = arange(-90,90+0.001, 1.0)
        LonOneBnd = arange(0,360+0.001, 1.0)
        vmin, vmax = 0, 0.2

        X,Y = meshgrid(LonOneBnd, LatOneBnd)

        M   = Basemap(resolution="l", llcrnrlat=-90, llcrnrlon=0, urcrnrlat=90, urcrnrlon=360)
        im  = M.pcolormesh(X,Y, a2fig, cmap="jet", vmin=vmin, vmax=vmax)

        M.drawcoastlines()
        M.drawparallels(arange(-90,90+0.1,30), labels=[1,0,0,0], fontsize=8, linewidth=0.3)
        M.drawmeridians(arange(-180,360+0.1,30), labels=[0,0,0,1], fontsize=8, linewidth=0.3, rotation=45)

        # colorbar
        axcbar = fig.add_axes([0.1,0.12,0.6, 0.05])
        plt.colorbar(im, orientation="horizontal", cax=axcbar, ticks=arange(vmin,vmax+0.001, 0.05))

        #ax1   = fig.add_axes([0.1,0.22,0.6,0.75])
        #ax2   = fig.add_axes([0.7,0.22,0.2,0.75])
        ax2   = fig.add_axes([0.8,0.34,0.1,0.515])
        LatOne= arange(-89.5,89.5+0.001,1.0)
        lim = []
        vmin, vmax = vminmax[varName]
        for dat in dla1dat[season]:
            im = ax2.plot(dat, LatOne, linewidth=0.8)
            lim.append(im[0])

        ax2.set_ylim([-90,90]) 
        ax2.set_xlim([vmin, vmax]) 
        # title
        stitle = "%s %s"%(varName, season)
        plt.suptitle(stitle)
        
        # save
        figDir  = baseDir + "/fig"
        util.mk_dir(figDir)
        figPath = figDir + "/plot.zonal.%04d-%04d.%s.%s.png"%(iYear,eYear,varName,season)
        plt.savefig(figPath)
        print figPath

        # Legend
        #legPath = figDir + "/legend.plot.zonal.png"
        #figleg  = plt.figure(figsize=(1.5,1.5))
        #figleg.legend(lim, lprjName)
        #figleg.savefig(legPath)
        #plt.close()
        #print legPath
