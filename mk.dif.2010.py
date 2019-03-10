import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from numpy import *
from netCDF4 import *
import GSWP3
from mpl_toolkits.basemap import Basemap
import myfunc.util as util


expr = "EXP1"
gswp = GSWP3.GSWP3()
gswp(expr=expr)
ny,nx = gswp.ny, gswp.nx
Lat   = gswp.Lat
Lon   = gswp.Lon
LatBnd= gswp.LatBnd
LonBnd= gswp.LonBnd


Year  = 2010
lvarName = ["Prcp","Rainf","Snowf"]
#lvarName = ["Wind"]
#lvarName = ["Tair","Qair","PSurf"]
baseDir1 = "/work/data2/hjkim/GSWP3/in/EXP1"
baseDir2 = "/work/data2/hjkim/GSWP3/from_tank.bin/out"

vminmax = {"Prcp":[-1,1],"Rainf":[-1,1],"Snowf":[-1,1],"SWdown":[-20,20], "LWdown":[-20,20], "Wind":[-4,4], "Tair":[-2,2], "Qair":[-0.006, 0.006], "PSurf":[-20,20]}

for varName in lvarName:
    srcDir1 = baseDir1 + "/%s"%(varName)
    srcDir2 = baseDir2 + "/%s"%(varName)
    
    srcPath1 = srcDir1 + "/GSWP3.BC.%s.3hrMap.%04d.nc"%(varName, Year)
    srcPath2 = srcDir2 + "/GSWP3.%s.%04d-%04d.nc"%(varName,Year,Year)
   
    print srcPath2
    nc1 = Dataset(srcPath1, "r", format="NETCDF")
    nc2 = Dataset(srcPath2, "r", format="NETCDF")

    dat1 = nc1[varName][:]
    dat2 = nc2[varName][:]

    a2mean1 = dat1.mean(axis=0)
    a2mean2 = dat2.mean(axis=0)

    if varName in ["Prcp","Rainf","Snowf"]:
        a2mean1 = a2mean1*60*60*24.
        a2mean2 = a2mean2*60*60*24.

    print a2mean1.mean(), a2mean2.mean()
    a2dif = a2mean2 - a2mean1
    #a2dif = a2dif / a2mean1

    print varName, a2dif.min(), a2dif.max()
    print a2mean2

    # Figure
    BBox  = [[-90,0],[90,360]]
    [[lllat,lllon],[urlat,urlon]] = BBox
    X,Y   = meshgrid( LonBnd, LatBnd )
    vmin,vmax = vminmax[varName]

    figmap   = plt.figure(figsize=(5,3))
    axmap    = figmap.add_axes([0.1,0.1,0.8,0.8])
    M     = Basemap(resolution="l", llcrnrlat=lllat,llcrnrlon=lllon,urcrnrlat=urlat,urcrnrlon=urlon, ax=axmap)
    im    = M.pcolormesh(X,Y, a2dif, cmap="RdBu_r", vmin=vmin, vmax=vmax)
    #im    = M.pcolormesh(X,Y, a2dif, cmap="RdBu_r")

    # coastlines
    M.drawcoastlines()

    #
    M.drawparallels(arange(-90,90+0.1,30), labels=[1,0,0,0], fontsize=8, linewidth=0.3)
    M.drawmeridians(arange(-180,360+0.1,30), labels=[0,0,0,1], fontsize=8, linewidth=0.3, rotation=45)

    # title
    stitle = "new-old %s"%(varName)
    plt.title(stitle)

    # colorbar
    plt.colorbar(im, orientation="horizontal")

    # save
    figDir  = "/work/a01/utsumi/GSWP3/fig"
    util.mk_dir(figDir)
    figPath = figDir + "/dif.map.new-old.%s.%04d.png"%(varName,Year)
    plt.savefig(figPath)
    print figPath 
 
