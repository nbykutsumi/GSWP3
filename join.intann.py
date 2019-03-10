from numpy import *
import os, sys
from PIL import Image
import myfunc.util as util

lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]
#lprjName = ["GSWP3","PRINCETON","WFDEI"]

#lvarName = ["SWdown","LWdown","Rainf","Snowf","Wind","Tair","Qair","PSurf"]
#lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
lvarName = ["SWdown","LWdown","Prcp","Wind","Qair","PSurf"]
#lvarName = ["Tair"]
lseason = ["ALL"]
iYear = 1979
#iYear = 2009
eYear = 2010
#lcalctype = ['mean','std']
lcalctype = ['mean']

for calctype in lcalctype:
    for season in lseason:
        for varName in lvarName:
            da2dat = {}
            for i,prjName in enumerate(lprjName):
                figDir  = "/work/a01/utsumi/GSWP3/fig"
                if prjName =="GSWP3":
                    srcPath = figDir + "/time.lat.intann.%s.%s.%s.%s.%04d-%04d.png"%(calctype, "ref", varName, prjName, iYear,eYear)
                else:
                    #srcPath = figDir + "/time.lat.intann.%s.%s.%s.%s.%04d-%04d.png"%(calctype, "dif", varName, prjName, iYear,eYear)
                    srcPath = figDir + "/time.lat.intann.%s.%s.%s.%s.%04d-%04d.png"%(calctype, "ref", varName, prjName, iYear,eYear)
    
                iimg    = Image.open(srcPath)
                a2array = asarray(iimg)
                da2dat[i]  = a2array


            a2empty = da2dat[0]*0 + 255
            line0 = concatenate([da2dat[0], da2dat[1]],axis=1)
            line1 = concatenate([da2dat[2], da2dat[3]],axis=1)
    
            print line0.shape
            a2oarray = concatenate([line0, line1], axis=0)
            oimg     = Image.fromarray(a2oarray)
    
            outPath  = figDir + "/join.time.lat.intann.%s.dif.%04d-%04d.%s.png"%(calctype,iYear,eYear,varName)
            oimg.save(outPath)
            print outPath
    
    
