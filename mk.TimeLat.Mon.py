import matplotlib as mpl
mpl.use("Agg")
import GSWP3
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import calendar
from datetime import datetime, timedelta

prjName= "GSWP3"
expr = "EXP1"
gswp = GSWP3.GSWP3()
gswp(expr=expr)

#lvarName = ["SWdown","LWdown"]
lvarName = ["Prcp","Wind","Tair","Qair","PSurf"]
baseDir = "/work/a01/utsumi/GSWP3"
per_day = 8 # [#/days] (3-hour-step)
iYear = 1901
#eYear = 2014
eYear = 2010
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)

for varName in lvarName:

    a2out = array([])
    for Year in lYear:
        print Year
    
        srcDir  = baseDir + "/Mon"  
        srcPath = srcDir + "/%s.%s.MonMap.%04d.npy"%(prjName, varName, Year)
        a3in    = np.load(srcPath)
        a2tmp   = a3in.mean(axis=2).T
    
        if len(a2out)==0:
            a2out = a2tmp
        else:
            a2out = concatenate([a2out, a2tmp], axis=1)
    
    #************************
    a2dat = a2out
    
    fig   = plt.figure(figsize=(9,3))
    ax    = fig.add_axes([0.1,0.1,0.8,0.8])
    im    = ax.imshow(a2dat, interpolation="nearest", cmap="jet", origin="lower")
    
    # aspect
    ax.set_aspect(aspect=1)
    
    # Y-ticks
    plt.yticks( arange(360+1)[::30] ,va="top")
    lylabel = arange(-90,90+1,0.5)[::30]
    ax.yaxis.set_ticklabels(lylabel, fontsize=10, va="center")
    
    # X-ticks
    n_per_year = 12
    nYear      = eYear-iYear+1
    stepYear   = 10
    lxtick     = range(n_per_year*nYear)[::n_per_year*stepYear]
    lxlabel    = lYear[::stepYear]
    plt.xticks( lxtick )
    ax.xaxis.set_ticklabels(lxlabel, fontsize=10)
    
    # title
    stitle = "%s %s"%(prjName, varName)
    plt.title(stitle)
    
    # colorbar
    plt.colorbar(im, orientation="horizontal")
    
    # save
    figDir  = baseDir + "/fig"
    util.mk_dir(figDir)
    figPath = figDir + "/TimeLat.%s.%04d-%04d.mon.%s.png"%(prjName,iYear,eYear,varName)
    plt.savefig(figPath)
    print figPath
