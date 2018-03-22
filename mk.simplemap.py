import matplotlib as mpl
mpl.use("Agg")
import GSWP3
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import myfunc.fig.Fig as Fig
import calendar
from datetime import datetime, timedelta
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap


prjName= "GSWP3"
expr = "EXP1"
gswp = GSWP3.GSWP3()
gswp(expr=expr)
ny, nx = gswp.ny, gswp.nx

#lvarName = ["SWdown","LWdown"]
#lvarName = ["Prcp","Wind","Tair","Qair","PSurf"]
lvarName = ["Prcp","Rainf","Snowf"]
#lvarName = ["SWdown","LWdown","Tair","Qair","PSurf"]
#lvarName  = ["Wind"]
baseDir = "/work/a01/utsumi/GSWP3"
iYear = 2014
eYear = 2014

#iYear = 2010
#eYear = 2010
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
miss  = -9999.

ver   = "new"
#ver   = "org"
#ver   = "sts"

vminmax = {"SWdown":[100,300], "LWdown":[100,400], "Prcp":[0,10], "Rainf":[0,10], "Snowf":[0,10],"Wind":[0,10], "Tair":[230,310], "Qair":[0.002, 0.02], "PSurf":[800,1020]}

for varName in lvarName:
    for Year in lYear:
    #for Year in lYear[::20]:
        if ver=="new":
            baseDir = "/data2/hjkim/GSWP3/from_tank.bin/out"
            srcDir  = baseDir + "/%s"%(varName)
            srcPath = srcDir + "/GSWP3.%s.%04d-%04d.nc"%(varName,Year,Year)
            #srcPath = srcDir + "/GSWP3.BC.%s.3hrMap.%04d.nc"%(varName, Year)

            ncIn  = Dataset(srcPath,"r",format="NETCDF")
            a3in  = ncIn.variables[varName][:]
        elif ver=="org":
            ncIn  = gswp.load_nc(varName=varName, Year=Year)
            a3in  = ncIn.variables[varName][:]

        elif ver=="sts":
            baseDir = "/data2/s_wata/tmp/GSWP3test/cor"
            srcDir  = baseDir
            srcPath = srcDir + "/cor_gswp3_%04d.hpn"%(Year)
            a3in    = fromfile(srcPath, float32).reshape(-1,ny,nx)

        Lat   = ncIn.variables["lat"][:]
        Lon   = ncIn.variables["lon"][:]
        LatBnd= arange(-90,90+0.001,0.5)
        LonBnd= arange(0,360+0.001,0.5)
        a2dat = a3in.mean(axis=0)

        if varName in ["Prcp","Rainf","Snowf"]:
            a2dat = a2dat*60*60*24
        if varName in ["Snowf"]:
            a2dat = ma.masked_equal(a2dat,0)
        if varName in ["PSurf"]:
            a2dat = a2dat/100.

        print srcPath
        print "-- a3in --"
        print a3in.min(), a3in.mean(), a3in.max()
        print "-- a2dat --"
        print a2dat.min(),a2dat.mean(), a2dat.max()
        print a2dat
        #-- figure ---

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
        stitle = "%s %s %04d"%(ver, varName, Year)
        plt.title(stitle)
        
        # colorbar
        plt.colorbar(im, orientation="horizontal")
        
        # save
        figDir  = "/work/a01/utsumi/GSWP3/fig"
        util.mk_dir(figDir)
        figPath = figDir + "/map.simgle.%s.%s.%04d.png"%(ver, varName,Year)
        plt.savefig(figPath)
        print figPath
        #-------------


    
