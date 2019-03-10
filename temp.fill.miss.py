from numpy import *
import glob
import numpy as np
import sys, os

prjName = "CRUNCEP"
srcDir = "/work/a01/utsumi/GSWP3/Mon/%s"%(prjName)

lsrcPath = glob.glob(srcDir + "/*.npy")

for srcPath in lsrcPath[:50]:
    a = np.load(srcPath)
    varName = srcPath.split(".")[1]
    print varName, a.min(), a.max()
