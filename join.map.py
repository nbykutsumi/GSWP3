from numpy import *
import os, sys
from PIL import Image
#import Image
import myfunc.util as util

lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]

#lvarName = ["SWdown","LWdown","Rainf","Snowf","Wind","Tair","Qair","PSurf"]
lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]
#lvarName = ["Prcp","Wind","Qair"]
lseason = ["ALL"]
iYear = 1979
eYear = 2010

for season in lseason:
    for varName in lvarName:
        da2dat = {}
        for i,prjName in enumerate(lprjName):
            figDir  = "/work/a01/utsumi/GSWP3/fig"
            srcPath = figDir + "/map.%s.%04d-%04d.%s.%s.png"%(prjName,iYear,eYear,varName,season)
            iimg    = Image.open(srcPath)
            a2array = asarray(iimg)
            da2dat[i]  = a2array

        line0 = concatenate([da2dat[0], da2dat[1]],axis=1)
        line1 = concatenate([da2dat[2], da2dat[3]],axis=1)

        print line0.shape
        a2oarray = concatenate([line0, line1], axis=0)
        oimg     = Image.fromarray(a2oarray)

        outPath  = figDir + "/join.map.%04d-%04d.%s.%s.png"%(iYear,eYear,varName,season)
        oimg.save(outPath)
        print outPath


