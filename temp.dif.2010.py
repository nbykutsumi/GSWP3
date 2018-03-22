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
#Year  = 2014
#lvarName = ["Prcp","Rainf","Snowf"]
lvarName = ["Wind"]
#lvarName = ["Tair","Qair","PSurf"]
baseDir1 = "/data2/hjkim/GSWP3/in/EXP1"
baseDir2 = "/data2/hjkim/GSWP3/from_tank.bin/out"
baseDir3 = "/data2/s_wata/tmp/GSWP3test/cor"

vminmax = {"SWdown":[-20,20], "LWdown":[-20,20], "Prcp":[-1,1], "Wind":[-4,4], "Tair":[-2,2], "Qair":[-0.006, 0.006], "PSurf":[-20,20]}

def mk_fig(a2dat, stitle, figPath):
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
    #stitle = "new-old %s"%(varName)
    plt.title(stitle)

    # colorbar
    plt.colorbar(im, orientation="horizontal")

    # save
    #figDir  = "/work/a01/utsumi/GSWP3/fig"
    #util.mk_dir(figDir)
    #figPath = figDir + "/dif.map.new-old.%s.png"%(varName)
    plt.savefig(figPath)
    print figPath 
 

for varName in lvarName:
    srcDir1 = baseDir1 + "/%s"%(varName)
    srcDir2 = baseDir2 + "/%s"%(varName)
    srcDir3 = baseDir3
    
    srcPath1 = srcDir1 + "/GSWP3.BC.%s.3hrMap.%04d.nc"%(varName, Year)
    srcPath2 = srcDir2 + "/GSWP3.%s.%04d-%04d.nc"%(varName,Year,Year)
    #srcPath3 = srcDir3 + "/cor_gswp3_%04d.hpn"%(Year)
   
    print srcPath2
    nc1 = Dataset(srcPath1, "r", format="NETCDF")
    nc2 = Dataset(srcPath2, "r", format="NETCDF")

    dat1 = nc1[varName][:]
    dat2 = nc2[varName][:]
    #dat3 = fromfile(srcPath3, float32).reshape(-1,ny,nx)

    a2mean1 = dat1.mean(axis=0)
    a2mean2 = dat2.mean(axis=0)
    #a2mean3 = dat3.mean(axis=0)

    print "*"*50
    print dat1[0]
    print "*"*50
    print a2mean1
    print a2mean1.mean(), a2mean2.mean(), a2mean3.mean()

    a2dif = a2mean2 - a2mean1
    stitle = "new-old %s"%(varName)
    figDir  = "/work/a01/utsumi/GSWP3/fig"
    util.mk_dir(figDir)
    figPath = figDir + "/dif.map.new-old.%s.%04d.png"%(varName,Year)

    #a2dif = a2mean1 - a2mean3
    #stitle = "old-s_wata %s"%(varName)
    #figDir  = "/work/a01/utsumi/GSWP3/fig"
    #util.mk_dir(figDir)
    #figPath = figDir + "/dif.map.old-s_wata.%s.png"%(varName)
    #mk_fig(a2dif, stitle, figPath)

    #a2dif = a2mean2 - a2mean3
    #print a2dif
    #stitle = "new-s_wata %s"%(varName)
    #figDir  = "/work/a01/utsumi/GSWP3/fig"
    #util.mk_dir(figDir)
    #figPath = figDir + "/dif.map.new-s_wata.%04d.%s.png"%(varName,Year)
    #mk_fig(a2dif, stitle, figPath)

    #print a2mean2.mean()

    #a2dif  = a2mean2
    #stitle = "new %s"%(varName)
    #figDir  = "/work/a01/utsumi/GSWP3/fig"
    #util.mk_dir(figDir)
    #figPath = figDir + "/map.new.%s.%04d.png"%(varName,Year)
    #mk_fig(a2dif, stitle, figPath)

    #print a2mean3.mean()
    #a2dif  = a2mean3
    #stitle = "s_wata %s"%(varName)
    #figDir  = "/work/a01/utsumi/GSWP3/fig"
    #util.mk_dir(figDir)
    #figPath = figDir + "/map.s_wata.%s.%04d.png"%(varName,Year)
    #mk_fig(a2dif, stitle, figPath)


