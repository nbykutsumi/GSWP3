from numpy import *
import os, sys
from PIL import Image
import myfunc.util as util

lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]

#lvarName = ["SWdown","LWdown","Rainf","Snowf","Wind","Tair","Qair","PSurf"]
lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
#lvarName = ["Tair"]
lseason = ["ALL"]
iYear = 1979
eYear = 2010
lcalctype = ['std']
#lcalctype = ['std','mean']

for calctype in lcalctype:
    for season in lseason:
        for varName in lvarName:
            da2dat = {}
            for i,prjName in enumerate(lprjName):
                figDir  = "/work/a01/utsumi/GSWP3/fig"
                if prjName =="GSWP3":
                    srcPath = figDir + "/map.zonal.%s.%s.%s.%s.%04d-%04d.%s.png"%(calctype, "ref", varName, prjName, iYear,eYear,season)
                else:
                    srcPath = figDir + "/map.zonal.%s.%s.%s.%s.%04d-%04d.%s.png"%(calctype, "dif", varName, prjName, iYear,eYear,season)
    
                iimg    = Image.open(srcPath)
                a2array = asarray(iimg)
                da2dat[i]  = a2array
 

            a2empty = da2dat[0]*0+255
   
            line0 = concatenate([da2dat[0], da2dat[1]],axis=1)
            line1 = concatenate([da2dat[2], da2dat[3]],axis=1)

    
            print line0.shape
            a2oarray = concatenate([line0, line1], axis=0)
            oimg     = Image.fromarray(a2oarray)
    
            outPath  = figDir + "/join.map.%s.dif.%04d-%04d.%s.%s.png"%(calctype,iYear,eYear,varName,season)
            oimg.save(outPath)
            print outPath
    
    
