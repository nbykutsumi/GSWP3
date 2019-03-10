import os, sys
import myfunc.util as util


lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]


lvarName = ["SWdown","LWdown","Prcp","Wind","Qair","PSurf","Rainf","Snowf"]

iYear = 1900
eYear = 2014
lYear = range(iYear, eYear+1)
baseDir = "/work/a01/utsumi/GSWP3"

calctype = 'mean'
#calctype = 'std'
for prjName in lprjName:
    for varName in lvarName:
        for Year in lYear:
    
            srcDir  = baseDir + "/Mon/%s"%(prjName)
            srcPath = srcDir + "/%s.%s.MonMap.%04d.npy"%(prjName, varName, Year)
            if not os.path.exists(srcPath): continue
    
    
            outPath = srcDir + "/%s.%s.%s.MonMap.%04d.npy"%(prjName, varName, calctype, Year)
            if not os.path.exists(outPath):
                print os.path.exists(outPath), outPath
                os.symlink(srcPath, outPath)
 
