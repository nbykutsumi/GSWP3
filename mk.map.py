import matplotlib as mpl
mpl.use("Agg")
#import GSWP3, PRINCETON, CRUNCEP
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import calendar
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
import gswp_func

lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]
#lprjName = ["PRINCETON","CRUNCEP","WFDEI"]

#lvarName = ["SWdown"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
lvarName = ["Prcp","Wind","Tair","Qair","PSurf"]
#lseason  = ["ALL","DJF","MAM","JJA","SON"]
lseason = ["ALL"]
baseDir = "/work/a01/utsumi/GSWP3"
#iYear = 1901   # GSWP3
#iYear = 1956   # PRINCETON
#eYear = 2014
#iYear = 2010
#eYear = 2010
iYear = 1979
eYear = 2010
#eYear = 1905
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
nYear = len(lYear)
miss  = -9999.


vminmax = {"SWdown":[100,300], "LWdown":[100,400], "Prcp":[0,8], "Rainf":[0,8],"Snowf":[0,8],"Wind":[0,10], "Tair":[230,310], "Qair":[0.002, 0.02], "PSurf":[800,1020]}
for prjName in lprjName:
    for varName in lvarName:

        if prjName in ["GSWP3","CRUNCEP","WFDEI"]:
            ny,nx   = 360,720
            Lat     = arange(-89.75,89.75+0.0001,0.5)
            Lon     = arange(0.25,359.75+0.0001,0.5)
            LatBnd  = arange(-90,90+0.001, 0.5)
            LonBnd  = arange(0,360+0.001,0.5)
            res     = "hlf"
        elif prjName in ["PRINCETON"]:
            ny,nx   = 180,360
            Lat     = arange(-89.5,89.5+0.0001,1.0)
            Lon     = arange(0.5,359.5+0.0001,1.0)
            LatBnd  = arange(-90,90+0.001, 1.0)
            LonBnd  = arange(0,360+0.001,1.0)
            res     = "one"
        else:
            print "check prjName",prjName

        a2orog= gswp_func.load_orog(res=res)
 
        a2all = zeros([ny,nx],float32)
        a2djf = zeros([ny,nx],float32)
        a2mam = zeros([ny,nx],float32)
        a2jja = zeros([ny,nx],float32)
        a2son = zeros([ny,nx],float32)
    
        for Year in lYear:
            print Year
            if (varName=="Prcp")&(prjName in ["GSWP3","WFDEI"]):
                srcDir  = baseDir + "/Mon/%s"%(prjName)
                srcPath1 = srcDir + "/%s.%s.mean.MonMap.%04d.npy"%(prjName, "Rainf", Year)
                a3in1    = np.load(srcPath1)
                a3in1    = ma.masked_equal(a3in1,miss)

                srcPath2 = srcDir + "/%s.%s.mean.MonMap.%04d.npy"%(prjName, "Snowf", Year)
                a3in2    = np.load(srcPath2)
                a3in2    = ma.masked_equal(a3in2,miss)

                a3in     = a3in1 + a3in2

            else:
                srcDir  = baseDir + "/Mon/%s"%(prjName)
                srcPath = srcDir + "/%s.%s.mean.MonMap.%04d.npy"%(prjName, varName, Year)
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
    

            # coeficients
            # Prcp
            if varName in ["Prcp","Rainf","Snowf"]:
                if prjName =="CRUNCEP":
                    a2dat = a2dat * 4  # mm/6hr --> mm/day
                else:
                    a2dat = a2dat *60*60*24   # mm/day
            elif varName=="PSurf":
                a2dat = a2dat * 0.01

            # SWdown
            if (prjName=="CRUNCEP")&(varName in ["SWdown"]):
                coef = 1./(60*60*6)
    
            else:
                coef = 1.0

            a2dat = a2dat*coef 


            # mask sea
            a2dat = ma.masked_where(a2orog==-999., a2dat)
        
            # Figure 
            BBox  = [[-90,0],[90,360]]
            [[lllat,lllon],[urlat,urlon]] = BBox
            X,Y   = meshgrid( LonBnd, LatBnd )
            vmin,vmax = vminmax[varName]
            #sys.exit()
        
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
