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
import myfunc.regrid.Regrid as Regrid

prjName1= "GSWP3"
prjName2= "PRINCETON"

expr = "EXP1"
gswp = GSWP3.GSWP3()
gswp(expr=expr)
ny1,nx1 = gswp.ny, gswp.nx
Lat1   = gswp.Lat
Lon1   = gswp.Lon
LatBnd1= gswp.LatBnd
LonBnd1= gswp.LonBnd

if prjName2== "PRINCETON":
    dc    = PRINCETON.PRINCETON()
    ny2,nx2 = dc.ny, dc.nx
    Lat2   = dc.Lat
    Lon2   = dc.Lon
    LatBnd2= dc.LatBnd
    LonBnd2= dc.LonBnd
   

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
#eYear = 2010
eYear = 1957
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
nYear = len(lYear)
miss  = -9999.

vminmax = {"SWdown":[100,300], "LWdown":[100,400], "Prcp":[0,10], "Wind":[0,60], "Tair":[230,310], "Qair":[0.002, 0.02], "PSurf":[800,1020]}
for varName in lvarName:

    #-- (1) GSWP3, (2) Comared data ---
    a2all1 = zeros([ny1,nx1],float32)
    a2djf1 = zeros([ny1,nx1],float32)
    a2mam1 = zeros([ny1,nx1],float32)
    a2jja1 = zeros([ny1,nx1],float32)
    a2son1 = zeros([ny1,nx1],float32)

    a2all2 = zeros([ny2,nx2],float32)
    a2djf2 = zeros([ny2,nx2],float32)
    a2mam2 = zeros([ny2,nx2],float32)
    a2jja2 = zeros([ny2,nx2],float32)
    a2son2 = zeros([ny2,nx2],float32)


    for Year in lYear:
        print Year
    
        srcDir1  = baseDir + "/Mon/%s"%(prjName1) 
        srcPath1 = srcDir1 + "/%s.%s.MonMap.%04d.npy"%(prjName1, varName, Year)
        a3in1    = np.load(srcPath1)
        a3in1    = ma.masked_equal(a3in1,miss)

        a2all1   = a2all1 + a3in1.mean(axis=0)
        a2djf1   = a2djf1 + a3in1[[0,1,11],:,:].mean(axis=0)
        a2mam1   = a2mam1 + a3in1[[2,3,4], :,:].mean(axis=0)
        a2jja1   = a2jja1 + a3in1[[5,6,7], :,:].mean(axis=0)
        a2son1   = a2son1 + a3in1[[8,9,10],:,:].mean(axis=0)

        srcDir2  = baseDir + "/Mon/%s"%(prjName2) 
        srcPath2 = srcDir2 + "/%s.%s.MonMap.%04d.npy"%(prjName2, varName, Year)
        a3in2    = np.load(srcPath2)
        a3in2    = ma.masked_equal(a3in2,miss)

        a2all2   = a2all2 + a3in2.mean(axis=0)
        a2djf2   = a2djf2 + a3in2[[0,1,11],:,:].mean(axis=0)
        a2mam2   = a2mam2 + a3in2[[2,3,4], :,:].mean(axis=0)
        a2jja2   = a2jja2 + a3in2[[5,6,7], :,:].mean(axis=0)
        a2son2   = a2son2 + a3in2[[8,9,10],:,:].mean(axis=0)



    a2all1 = a2all1/nYear    
    a2djf1 = a2djf1/nYear    
    a2mam1 = a2mam1/nYear    
    a2jja1 = a2jja1/nYear    
    a2son1 = a2son1/nYear    

    a2all2 = a2all2/nYear    
    a2djf2 = a2djf2/nYear    
    a2mam2 = a2mam2/nYear    
    a2jja2 = a2jja2/nYear    
    a2son2 = a2son2/nYear    


    print "*"*50
    print a2all1
    print "-"*50
    print a2all2
    print "*"*50
    #************************
    for season in lseason:
        if   season=="ALL":
            a2dat1 = a2all1
            a2dat2 = a2all2
        elif season=="DJF":
            a2dat1 = a2djf1
            a2dat2 = a2djf2
        elif season=="MAM":
            a2dat1 = a2mam1
            a2dat2 = a2mam2
        elif season=="JJA":
            a2dat1 = a2jja1
            a2dat2 = a2jja2
        elif season=="SON":
            a2dat1 = a2son1
            a2dat2 = a2son2

        if varName == "Prcp":
            a2dat1 = a2dat1 *60*60*24   # mm/day
            a2dat2 = a2dat2 *60*60*24   # mm/day
        elif varName=="PSurf":
            a2dat1 = a2dat1 * 0.01
            a2dat2 = a2dat2 * 0.01
   
        a2dat2 = Regrid.biIntp(Lat2,Lon2,a2dat2, Lat1, Lon1, miss=miss).reshape(ny1,nx1)
        
        print a2dat2.shape

        """ 
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
        """ 
