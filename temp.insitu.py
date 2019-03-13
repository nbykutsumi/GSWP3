import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from numpy import *

obsPath='/work/a01/utsumi/GSWP3/insitu/Tair/cdp/SnowMIP_gswp3c.pre.3hr.1980.npy'
modelPath='/work/a01/utsumi/GSWP3/insitu/Tair/cdp/GSWP3.3hr.1980.npy'


a= np.load(obsPath,'r')
b= np.load(modelPath,'r')


outPath = '/work/a01/utsumi/GSWP3/insitu/snowmip.png'
plt.scatter(ma.masked_less(a,0), ma.masked_less(b,0))
plt.savefig(outPath)
print outPath

print a
print b
