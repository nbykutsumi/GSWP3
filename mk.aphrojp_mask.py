import matplotlib
matplotlib.use('Agg')
from numpy import *
from datetime import datetime, timedelta
import myfunc.util as util
import calendar
import numpy as np
import myfunc.regrid.Regrid as Regrid

import matplotlib.pyplot as plt

miss_in = -999.9
miss_out= -9999.
#Year  = range(1901,2011+1)

lprjName = ["GSWP3","PRINCETON","CRUNCEP","WFDEI"]


LatOrg = arange(24.025,  24.025+0.05*440, 0.05)
LonOrg = arange(123.025, 123.025+0.05*460, 0.05)

for prjName in lprjName:
    if prjName in ["GSWP3","CRUNCEP","WFDEI"]:
        nyUp,nxUp = 360,720
        LatUp  = arange(-89.75,89.75+0.001, 0.5)
        LonUp  = arange(0.25, 359.75+0.0001, 0.5)
    elif prjName in ["PRINCETON"]:
        nyUp,nxUp = 180,360
        LatUp  = arange(-89.5,89.5+0.0001,1.0)
        LonUp  = arange(0.5,359.5+0.0001,1.0)
    else:
        print 'chekc prjName',prjName

    us = Regrid.UpScale()
    us(LatOrg, LonOrg, LatUp, LonUp, globflag=False)

 
    
    Year = 2010
    srcDir = '/work/data1/hjkim/APHRODITE/AphroJP_V1207_DPREC.CSTN'
    srcPath = srcDir + '/AphroJP_V1207_DPREC.CSTN.%04d'%(Year)
    a3in = fromfile(srcPath,float32).reshape(-1,440,460)
    a2in = a3in[0]
    
    a2ap   = us.upscale(a2in, pergrid=False, miss_in=-999.9, miss_out=-9999.)
    a2mask = ma.masked_less(a2ap, 0).mask
    a2out  = ones([nyUp,nxUp],float32)
    a2out  = ma.masked_where(a2mask, a2out).filled(miss_out)
    
    outDir = '/work/a01/utsumi/GSWP3/VS_APHRO_JP/mask'
    util.mk_dir(outDir)
    outPath= outDir + '/mask_aphrojp_%s.npy'%(prjName)
    np.save(outPath, a2out)

    fig = plt.figure()
    ax  = fig.add_axes()
    plt.imshow(a2out, origin='lower')
    plt.savefig(outPath+ '.png')
    print outPath
    plt.clf()

    #fig = plt.figure()
    #ax  = fig.add_axes()
    #plt.imshow(a2in, origin='lower')
    #plt.savefig(outPath+ '.org.png')
    #print outPath
    #plt.clf()
