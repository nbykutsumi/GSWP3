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
import scipy.stats


lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]
#lprjName = ["GSWP3","PRINCETON"]

#lvarName = ["SWdown","LWdown"]
#lvarName = ["Prcp"]
#lvarName = ["SWdown","LWdown","Rainf","Snowf","Wind","Tair","Qair","PSurf"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Qair","PSurf"]
#lvarName = ["Qair","PSurf"]
lvarName = ["Tair"]
#lvarName = ["SWdown"]
#lseason  = ["ALL","DJF","MAM","JJA","SON"]
lseason = ["ALL"]
baseDir = "/work/a01/utsumi/GSWP3"
#iYear = 1901   # GSWP3
#iYear = 1956   # PRINCETON
#eYear = 2014

iYear = 1979   # all
eYear = 2010   # all

#iYear  = 1979
#eYear  = 1982

lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
nYear = len(lYear)
miss  = -9999.

lcalctype = ['mean','std']
#calctype = 'mean'  # mean, std
#calctype = 'std'   # mean, std


us = Regrid.UpScale()

vminmax = {"SWdown":[100,300], "LWdown":[100,400], "Prcp":[0,10], "Rainf":[0,10],"Snowf":[0,10],"Wind":[0,10], "Tair":[230,310], "Qair":[0.002, 0.02], "PSurf":[800,1040]}

for calctype in lcalctype:
    for varName in lvarName:
    
        da2dat = {}
    
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
     
            a2all = zeros([ny,nx],float32)
            a2djf = zeros([ny,nx],float32)
            a2mam = zeros([ny,nx],float32)
            a2jja = zeros([ny,nx],float32)
            a2son = zeros([ny,nx],float32)
        
            for Year in lYear:
                print varName, prjName, Year
           
                #if (varName=="Prcp")&(prjName in ["GSWP3","WFDEI"]):
                if (varName=="Prcp")&(prjName in ["WFDEI"]):
                    srcDir  = baseDir + "/Mon/%s"%(prjName) 
                    # Rainf
                    if calctype=='mean':
                        srcPath1 = srcDir + "/%s.%s.MonMap.%04d.npy"%(prjName, "Rainf", Year)
                    else:
                        srcPath1 = srcDir + "/%s.%s.%s.MonMap.%04d.npy"%(prjName, "Rainf", calctype, Year)
                    a3in1    = np.load(srcPath1)
                    a3in1    = ma.masked_equal(a3in1,miss)
    
                    # Snowf
                    if calctype=='mean':
                        srcPath2 = srcDir + "/%s.%s.MonMap.%04d.npy"%(prjName, "Snowf", Year)
                    else:
                        srcPath2 = srcDir + "/%s.%s.%s.MonMap.%04d.npy"%(prjName, "Snowf", calctype, Year)
    
                    a3in2    = np.load(srcPath2)
                    a3in2    = ma.masked_equal(a3in2,miss)
    
                    a3in     = a3in1 + a3in2
    
                else: 
                    srcDir  = baseDir + "/Mon/%s"%(prjName) 
                    if calctype=='mean':
                        srcPath = srcDir + "/%s.%s.MonMap.%04d.npy"%(prjName, varName, Year)
                    else:
                        srcPath = srcDir + "/%s.%s.%s.MonMap.%04d.npy"%(prjName, varName, calctype, Year)
                    a3in    = np.load(srcPath)
                    a3in    = ma.masked_equal(a3in,miss)
    
    
                a2all   = a2all + a3in.mean(axis=0)
                a2djf   = a2djf + a3in[[0,1,11],:,:].mean(axis=0)
                a2mam   = a2mam + a3in[[2,3,4], :,:].mean(axis=0)
                a2jja   = a2jja + a3in[[5,6,7], :,:].mean(axis=0)
                a2son   = a2son + a3in[[8,9,10],:,:].mean(axis=0)
        
            a2all = a2all/nYear *coef
            a2djf = a2djf/nYear *coef    
            a2mam = a2mam/nYear *coef    
            a2jja = a2jja/nYear *coef    
            a2son = a2son/nYear *coef    
    
    
    
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
        
                if varName in ["Prcp","Rainf","Snowf"]:
                    if prjName =="CRUNCEP":
                        a2dat = a2dat * 4  # mm/6hr --> mm/day
                    else:
                        a2dat = a2dat *60*60*24   # mm/day
                elif varName=="PSurf":
                    a2dat = a2dat * 0.01
    
    
                # regrid to 1.0 degree
                if res=="hlf":
                    print prjName, a2dat.shape
                    LatOrg = arange(-89.75,89.75+0.001, 0.5)
                    LonOrg = arange(0.25,359.75+0.001, 0.5)
                    LatUp  = arange(-89.5,89.5+0.001, 1.0)
                    LonUp  = arange(0.5,359.5+0.001, 1.0)
                    us(LatOrg, LonOrg, LatUp, LonUp, globflag=True)
                    a2dat = us.upscale(a2dat, pergrid=False, miss_in = -9999., miss_out=-9999.)
    
                # mask sea
                a2dat = ma.masked_where(a2orog==-999., a2dat)
    
                da2dat[prjName,season] = a2dat
    
        #""" 
        # Figure
        for season in lseason:
    
            fig  = plt.figure(figsize=(5,4))
            ax   = fig.add_axes([0.1,0.1,0.8,0.8])
    
            for iprj, prjName in enumerate(lprjName):
                a2dat = da2dat[prjName,season]
                a2dat = ma.masked_where(a2orog==-999., a2dat)
    
                vmin, vmax = vminmax[varName]
                #bin_edges  = linspace(vmin,vmax,20)
                #hist, bin_edges_tmp = np.histogram(a2dat, bins=bin_edges, density=True)
    
                #x = 0.5*(bin_edges[:-1] + bin_edges[1:]) 
                #ax.plot(x, hist, '-')
    
                kde = scipy.stats.gaussian_kde(a2dat.flatten(), bw_method='scott')
                x   = np.linspace(a2dat.min(), a2dat.max(), 100)
                ax.plot(x, kde(x), label=prjName)
    
    
            plt.legend()
    
    
    
    
            # title
            stitle = "%s %s %s"%(calctype, varName, season)
            plt.suptitle(stitle)
            
            # save
            figDir  = baseDir + "/fig"
            util.mk_dir(figDir)
            figPath = figDir + "/pdf.%s.%s.%04d-%04d.%s.png"%(calctype, varName, iYear,eYear,season)
    
            plt.savefig(figPath)
            print figPath
    
    
