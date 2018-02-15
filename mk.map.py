import matplotlib as mpl
mpl.use("Agg")
import GSWP3, PRINCETON
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import calendar
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap

#prjName= "GSWP3"
prjName= "PRINCETON"

if prjName == "GSPW3":
    expr = "EXP1"
    gswp = GSWP3.GSWP3()
    gswp(expr=expr)
    ny,nx = gswp.ny, gswp.nx
    Lat   = gswp.Lat
    Lon   = gswp.Lon
    LatBnd= gswp.LatBnd
    LonBnd= gswp.LonBnd
elif prjName== "PRINCETON":
    pg    = PRINCETON.PRINCETON()
    ny,nx = pg.ny, pg.nx
    Lat   = pg.Lat
    Lon   = pg.Lon
    LatBnd= pg.LatBnd
    LonBnd= pg.LonBnd
   


lvarName = ["SWdown"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
#lvarName = ["PSurf"]
#lseason  = ["ALL","DJF","MAM","JJA","SON"]
lseason = ["MAM"]
baseDir = "/work/a01/utsumi/GSWP3"
per_day = 8 # [#/days] (3-hour-step)
iYear = 1901   # GSWP3
iYear = 1956   # PRINCETON
#eYear = 2014
eYear = 2010
#eYear = 1905
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
nYear = len(lYear)
miss  = -9999.

vminmax = {"SWdown":[100,300], "LWdown":[100,400], "Prcp":[0,10], "Wind":[0,60], "Tair":[230,310], "Qair":[0.002, 0.02], "PSurf":[800,1020]}
for varName in lvarName:

    a2all = zeros([ny,nx],float32)
    a2djf = zeros([ny,nx],float32)
    a2mam = zeros([ny,nx],float32)
    a2jja = zeros([ny,nx],float32)
    a2son = zeros([ny,nx],float32)

    for Year in lYear:
        print Year
    
        srcDir  = baseDir + "/Mon/%s"%(prjName) 
        srcPath = srcDir + "/%s.%s.MonMap.%04d.npy"%(prjName, varName, Year)
        a3in    = np.load(srcPath)
        a3in    = ma.masked_equal(a3in,miss)

        a2all   = a2all + a3in.mean(axis=0)
        a2djf   = a2djf + a3in[[0,1,11],:,:].mean(axis=0)
        a2mam   = a2mam + a3in[[2,3,4], :,:].mean(axis=0)
        a2jja   = a2jja + a3in[[5,6,7], :,:].mean(axis=0)
        a2son   = a2son + a3in[[8,9,10],:,:].mean(axis=0)

    a2all = a2all/nYear    
    a2djf = a2djf/nYear    
    a2mam = a2mam/nYear    
    a2jja = a2jja/nYear    
    a2son = a2son/nYear    

    print "*"*50
    print a2all
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

        if varName == "Prcp":
            a2dat = a2dat *60*60*24   # mm/day
        elif varName=="PSurf":
            a2dat = a2dat * 0.01
    
        # Figure 
        BBox  = [[-90,0],[90,360]]
        [[lllat,lllon],[urlat,urlon]] = BBox
        X,Y   = meshgrid( LonBnd, LatBnd )
        vmin,vmax = vminmax[varName]
    
        figmap   = plt.figure(figsize=(5,3))
        axmap    = figmap.add_axes([0.1,0.1,0.8,0.8])
        M     = Basemap(resolution="l", llcrnrlat=lllat,llcrnrlon=lllon,urcrnrlat=urlat,urcrnrlon=urlon, ax=axmap)
        im    = M.pcolormesh(X,Y, a2dat, cmap="jet", vmin=vmin, vmax=vmax)
        #im    = M.pcolormesh(X,Y, a2dat, cmap="jet")

        # coastlines
        M.drawcoastlines()

        # 
        M.drawparallels(arange(-90,90+0.1,30), labels=[1,0,0,0], fontsize=8, linewidth=0.3)
        M.drawmeridians(arange(-180,360+0.1,30), labels=[0,0,0,1], fontsize=8, linewidth=0.3, rotation=45)
 
        # title
        stitle = "%s %s (%s) %04d-%04d"%(prjName, varName, season, iYear, eYear)
        plt.title(stitle)
        
        # colorbar
        plt.colorbar(im, orientation="horizontal")
        
        # save
        figDir  = baseDir + "/fig"
        util.mk_dir(figDir)
        figPath = figDir + "/map.%s.%04d-%04d.%s.%s.png"%(prjName,iYear,eYear,varName,season)
        plt.savefig(figPath)
        print figPath
