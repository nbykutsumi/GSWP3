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

#lprjName = ["GSWP3","PRINCETON","WFDEI","CRUNCEP"]
lprjName = ["GSWP3","PRINCETON","WFDEI"]

#lvarName = ["SWdown","LWdown"]
#lvarName = ["Prcp"]
#lvarName = ["SWdown","LWdown","Rainf","Snowf","Wind","Tair","Qair","PSurf"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Qair","PSurf"]
lvarName = ["Tair"]
baseDir = "/work/a01/utsumi/GSWP3"
#iYear = 1901   # GSWP3
#iYear = 1956   # PRINCETON
#eYear = 2014

iYear = 1979   # all
eYear = 2010   # all

#iYear = 2009   # all
#eYear = 2010   # all

lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
nYear = len(lYear)
miss  = -9999.

lcalctype = ['mean','std']


us = Regrid.UpScale()


for calctype in lcalctype:
    if calctype=='mean':
        vminmax = {"SWdown":[100,300], "LWdown":[100,400], "Prcp":[0,10], "Rainf":[0,10],"Snowf":[0,10],"Wind":[0,10], "Tair":[230,310], "Qair":[0.002, 0.02], "PSurf":[800,1020]}
    
        vminmax_dif = {"SWdown":[-20,20], "LWdown":[-20,20], "Prcp":[-1,1], "Rainf":[-1,1],"Snowf":[-1,1],"Wind":[-2,2], "Tair":[-3,3], "Qair":[-0.005, 0.005], "PSurf":[-100,100]}
    
    elif calctype=='std':
        vminmax = {"SWdown":[0,100], "LWdown":[0,50], "Prcp":[0,10], "Rainf":[0,10],"Snowf":[0,10],"Wind":[0,5], "Tair":[0,10], "Qair":[0, 0.004], "PSurf":[0,10]}
    
        vminmax_dif = {"SWdown":[-40,40], "LWdown":[-20,20], "Prcp":[-4,4], "Rainf":[-1,1],"Snowf":[-1,1],"Wind":[-2,2], "Tair":[-2,2], "Qair":[-0.002, 0.002], "PSurf":[-5,5]}
    
    
    
    for varName in lvarName:
    
        da3dat = {}
    
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
     
            a3dat = zeros([12,ny,nx],float32)
    
    
    
            for Year in lYear:
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
    
    
                a3dat   = a3dat + a3in
        
            a3dat = a3dat/nYear *coef
    
    
    
            #************************
            if varName in ["Prcp","Rainf","Snowf"]:
                if prjName =="CRUNCEP":
                    a3dat = a3dat * 4  # mm/6hr --> mm/day
                else:
                    a3dat = a3dat *60*60*24   # mm/day
            elif varName=="PSurf":
                a3dat = a3dat * 0.01
    
    
            # regrid to 1.0 degree
            if res=="hlf":
                LatOrg = arange(-89.75,89.75+0.001, 0.5)
                LonOrg = arange(0.25,359.75+0.001, 0.5)
                LatUp  = arange(-89.5,89.5+0.001, 1.0)
                LonUp  = arange(0.5,359.5+0.001, 1.0)
                us(LatOrg, LonOrg, LatUp, LonUp, globflag=True)
                a3dat = array([ us.upscale(a3dat[i], pergrid=False, miss_in = -9999., miss_out=-9999.) for i in range(12)])
    
            # mask sea
            a3dat = ma.masked_where(a3orog==-999., a3dat)
    
            da3dat[prjName] = a3dat


        #""" 
        # Figure time-lat
        for prjName in lprjName:
            for figtype in ["ref","dif"]:
                if (prjName=="GSWP3")&(figtype=="dif"):
                    continue
    
                if (prjName !="GSWP3")&(figtype=="ref"):
                    continue
    
                if figtype =="ref":
                    a2dat = da3dat[prjName].mean(axis=2)
                    vmin, vmax = vminmax[varName]
    
                elif figtype=="dif":
                    a2dat = da3dat[prjName].mean(axis=2) -da3dat["GSWP3"].mean(axis=2)
                    vmin, vmax = vminmax_dif[varName]
    
    
                fig   = plt.figure(figsize=(4,2.3))
                #----
                a2fig = a2dat.T
                ax    = fig.add_axes([0.1,0.1,0.8,0.75])
                LatOneBnd = arange(-90,90+0.001, 1.0)
                a1mon_edge= arange(0.5,12.5+1,1)
    
    
                # cut lat <-60
                a2fig = a2fig[30:]
                LatOneBnd = LatOneBnd[30:]
    
                #-------------
     
                X,Y = meshgrid(a1mon_edge, LatOneBnd)
       
                if figtype=='dif': cmap='RdBu_r'
                else: cmap='jet'
                im  =ax.pcolormesh(X,Y, a2fig, cmap=cmap, vmin=vmin, vmax=vmax)
        
                # colorbar
                #axcbar = fig.add_axes([0.1,3012,0.6, 0.05])
                #plt.colorbar(im, orientation="horizontal", cax=axcbar, ticks=arange(vmin,vmax+0.001, 0.05))
                #plt.colorbar(im, orientation="horizontal", cax=axcbar)
                plt.colorbar(im, orientation="horizontal")
        
                # title
                stitle = "%s %s %s %s"%(calctype, figtype, prjName, varName)
                plt.suptitle(stitle)
                
                # save
                figDir  = baseDir + "/fig"
                util.mk_dir(figDir)
                figPath = figDir + "/time.lat.%s.%s.%s.%s.%04d-%04d.png"%(calctype, figtype, varName,prjName, iYear,eYear)
    
                plt.savefig(figPath)
                print figPath


       
