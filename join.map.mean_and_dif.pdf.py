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

calctype='mean'
for season in lseason:
    for varName in lvarName:

        #-- Read Map -------------------
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

        #-- Read pdf ---------------
        dimgpdf = {}
        for i,calctypepdf in enumerate(['mean','std']):
            srcPath = figDir + "/pdf.%s.%s.%04d-%04d.%s.png"%(calctypepdf, varName, iYear,eYear,season)
            iimg    = Image.open(srcPath)
            iimg    = iimg.resize((int(iimg.width / 1.7), int(iimg.height / 1.7)), Image.LANCZOS)
            dimgpdf[i] = iimg

        #-- Joint ------------------
        a2empty = da2dat[0]*0+255

        line0 = concatenate([da2dat[0], da2dat[1]],axis=1)
        line1 = concatenate([a2empty,   da2dat[2]],axis=1)
        line2 = concatenate([a2empty,   da2dat[3]],axis=1)


        print line0.shape
        a2oarray = concatenate([line0, line1, line2], axis=0)
        oimg     = Image.fromarray(a2oarray)

        #-- Pase pdf ----------
        xback = oimg.width
        yback = oimg.height
        oimg.paste(dimgpdf[0], (0,yback/3))
        oimg.paste(dimgpdf[1], (0,yback/3*2))

        #----------------------
        outPath  = figDir + "/join.pdf.map.%s.dif.%04d-%04d.%s.%s.png"%(calctype,iYear,eYear,varName,season)
        oimg.save(outPath)
        print outPath
    
    
