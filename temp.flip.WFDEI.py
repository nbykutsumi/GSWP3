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
    print srcPath
