from numpy import *
import numpy as np
import glob
import sys, os

prjName = "WFDEI"
baseDir = "/work/a01/utsumi/GSWP3"
srcDir  = baseDir + "/Mon/%s"%(prjName)
#srcPath= srcDir + "/%s.%s.MonMap.%04d.npy"%(prjName, varName, Year)

print srcDir
lsrcPath = glob.glob(srcDir+ "/*")
for srcPath in lsrcPath:
    fName = os.path.basename(srcPath)
    varName = fName.split(".")[1]
    Year    = int(fName.split(".")[3])
    if Year == 2000:
        if not varName in ["SWdown", "LWdown"]:
            continue
    #print varName, Year
    #a = np.load(srcPath)
    #a = flipud(a)
    #np.save(srcPath, a)
    #print srcPath
