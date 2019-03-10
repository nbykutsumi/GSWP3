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

#lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]
lprjName = ["GSWP3"]

#lvarName = ["SWdown","LWdown","Rainf","Snowf","Wind","Tair","Qair","PSurf"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Qair","PSurf"]   # No Tair
lvarName = ["Wind"]
baseDir = "/work/a01/utsumi/GSWP3"
#iYear = 1901   # GSWP3
#iYear = 1956   # PRINCETON
#eYear = 2014

iYear = 1901   # all
eYear = 2010   # all

#iYear = 2000
#eYear = 2010

lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
nYear = len(lYear)
miss  = -9999.

calctype = 'mean'
if calctype=='mean':
    vminmax = {"SWdown":[-20,20], "LWdown":[-20,20], "Prcp":[-1,1], "Rainf":[-1,1],"Snowf":[-1,1],"Wind":[-2,2], "Tair":[-2,2], "Qair":[-0.005, 0.005], "PSurf":[-10,10]}

    vminmax_dif = {"SWdown":[-20,20], "LWdown":[-20,20], "Prcp":[-1,1], "Rainf":[-1,1],"Snowf":[-1,1],"Wind":[-2,2], "Tair":[-10,10], "Qair":[-0.005, 0.005], "PSurf":[-100,100]}

elif calctype=='std':
    vminmax = {"SWdown":[-10,10], "LWdown":[-10,10], "Prcp":[-1,1], "Rainf":[-1,1],"Snowf":[-1,1],"Wind":[-1,1], "Tair":[-2,2], "Qair":[-0.005, 0.005], "PSurf":[-5,5]}

    vminmax_dif = {"SWdown":[-40,40], "LWdown":[-20,20], "Prcp":[-4,4], "Rainf":[-1,1],"Snowf":[-1,1],"Wind":[-2,2], "Tair":[-10,10], "Qair":[-0.002, 0.002], "PSurf":[-5,5]}


us = Regrid.UpScale()

for varName in lvarName:

    da2dat = {}
    da2mean= {}

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
        a3orog= array([a2orog for i in range(12)])

        a1dat  = []
        for kyear, Year in enumerate(lYear):
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

            # regrid to 1.0 degree
            if res=="hlf":
                LatOrg = arange(-89.75,89.75+0.001, 0.5)
                LonOrg = arange(0.25,359.75+0.001, 0.5)
                LatUp  = arange(-89.5,89.5+0.001, 1.0)
                LonUp  = arange(0.5,359.5+0.001, 1.0)
                us(LatOrg, LonOrg, LatUp, LonUp, globflag=True)
                a3in = array([ us.upscale(a3in[i], pergrid=False, miss_in = -9999., miss_out=-9999.) for i in range(12)])


            # mask sea
            a3in = ma.masked_where(a3orog==-999., a3in)

            # extract 60S ~ 60N
            a3in = a3in[:,30:180-30,:]

            # mask missing
            a3in = ma.masked_equal(a3in, miss)

            # mean
            a1in = a3in.mean(axis=(1,2)) * coef
 
            a1dat.extend(a1in.tolist())
        
        #************************
        a1dat = array(a1dat)

        if varName in ["Prcp","Rainf","Snowf"]:
            if prjName =="CRUNCEP":
                a1dat = a1dat * 4  # mm/6hr --> mm/day
            else:
                a1dat = a1dat *60*60*24   # mm/day

        elif varName=="PSurf":
            a1dat = a1dat * 0.01

        #""" 
        # Figure time-lat
        fig   = plt.figure(figsize=(15,2.3))
        #----
        ax    = fig.add_axes([0.1,0.12,0.8,0.73])

        #-------------
        im  =ax.plot(a1dat)
    
        # X-ticks
        n_per_year = 12
        nYear      = eYear-iYear+1
        stepYear   = 5
        lxtick     = range(n_per_year*nYear)[::n_per_year*stepYear]
        lxlabel    = lYear[::stepYear]
        plt.xticks( lxtick )
        ax.xaxis.set_ticklabels(lxlabel, fontsize=10)

        lxtick_minor= range(n_per_year*nYear)[::n_per_year]
        ax.set_xticks( lxtick_minor, minor=True)        

    
        # title
        stitle = "%s %s %s"%(calctype, prjName, varName)
        plt.suptitle(stitle)
        
        # save
        figDir  = baseDir + "/fig"
        util.mk_dir(figDir)
        figPath = figDir + "/plot.ts.%s.%s.%s.%04d-%04d.png"%(calctype, varName,prjName, iYear,eYear)

        plt.savefig(figPath)
        print figPath
    

       
