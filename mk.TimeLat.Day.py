import matplotlib as mpl
mpl.use("Agg")
import GSWP3
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util

prjName= "GSWP3"
expr = "EXP1"
gswp = GSWP3.GSWP3()
gswp(expr=expr)

lvarName = ["SWdown"]
baseDir = "/work/a01/utsumi/GSWP3"
calFlag = False
#calFlag = True
days    = 5
per_day = 8 # [#/days] (3-hour-step)
k       = days*per_day  
iYear = 2000
eYear = 2010
lYear = range(iYear,eYear+1)

for varName in lvarName:
    outDir = baseDir + "/TimeLat"
    outPath= outDir + "/TimeLat.%s.%04d-%04d.%sday.%s.npy"%(prjName, iYear, eYear, days, varName)
    
    a2out = array([])
    for Year in lYear:
        if calFlag ==False: continue
        ncIn=gswp.load_nc(varName=varName, Year=Year)
        a3in= ncIn.variables[varName][:]
        ni  = a3in.shape[0]/(k)
        l   = [a3in[i*k:(i+1)*k,:,:].mean(axis=(0,2)).reshape(-1,1) for i in range(ni)]
        a2tmp = concatenate(l, axis=1)
        if len(a2out)==0:
            a2out = a2tmp
        else:
            a2out = concatenate([a2out, a2tmp], axis=1)

    if calFlag ==True:   
        np.save(outPath, a2out)
        print outPath

    #************************
    # figure --
    a2dat = np.load(outPath)

    #a2dat = ma.masked_equal(a2dat,0)

    fig   = plt.figure(figsize=(6,3))
    ax    = fig.add_axes([0.1,0.1,0.8,0.8])
    im    = ax.imshow(a2dat, interpolation="nearest", cmap="jet", origin="lower")

    # aspect
    ax.set_aspect(aspect=0.7)

    # Y-ticks
    plt.yticks( arange(360+1)[::30] ,va="top")
    lylabel = arange(-90,90+1,0.5)[::30]
    ax.yaxis.set_ticklabels(lylabel, fontsize=10, va="top")

    # X-ticks
    n_per_year = int(365/days)
    nYear      = a2dat.shape[1]/n_per_year
    lxtick     = range(n_per_year*nYear)[::n_per_year]
    lxlabel    = lYear
    plt.xticks( lxtick )
    ax.xaxis.set_ticklabels(lxlabel, fontsize=10, ha="left")

    # title
    stitle = "%s %s"%(prjName, varName)
    plt.title(stitle)

    # colorbar
    plt.colorbar(im, orientation="horizontal")

    # save
    figDir  = baseDir + "/fig"
    util.mk_dir(figDir)
    figPath = figDir + "/TimeLat.%s.%04d-%04d.%sday.%s.png"%(prjName,iYear,eYear,days,varName)
    plt.savefig(figPath)
    print figPath
