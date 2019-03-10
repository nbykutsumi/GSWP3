from numpy import *
from datetime import datetime, timedelta
import myfunc.util as util
import calendar
import numpy as np

lYear = arange(1900,2011+1)
#lYear = arange(1900,1900+1)

miss_in = -999.9
miss_out= -9999.
ny,nx = 440,460
for Year in lYear:
    srcDir = '/work/data1/hjkim/APHRODITE/AphroJP_V1207_DPREC.CSTN'
    srcPath = srcDir + '/AphroJP_V1207_DPREC.CSTN.%04d'%(Year)
    a3in = fromfile(srcPath,float32).reshape(-1,440,460)

    lMon  = arange(1,12+1)
    #lMon  = arange(1,3+1)

    a3mean = zeros([12,ny,nx],float32) 
    a3std  = zeros([12,ny,nx],float32) 
   
    idx0=0
    idx1=0 
    for iMon,Mon in enumerate(lMon):
        eDay = calendar.monthrange(Year,Mon)[1]
        idx0 = idx1
        idx1 = idx1 + eDay 
        a2mean= ma.masked_less(a3in[idx0:idx1,:,:], 0).mean(axis=0).filled(miss_out)
        a2std = ma.masked_less(a3in[idx0:idx1,:,:], 0).std (axis=0).filled(miss_out)

        #print Mon,idx0,idx1

        a3mean[iMon] = a2mean
        a3std [iMon] = a2std

    outDir   = '/work/a01/utsumi/GSWP3/Mon/APHRO_JP'
    util.mk_dir(outDir)

    meanPath = outDir + '/APHRO_JP.Prcp.mean.MonMap.%04d.npy'%(Year)
    stdPath  = outDir + '/APHRO_JP.Prcp.std.MonMap.%04d.npy'%(Year)

    np.save(meanPath, a3mean.astype(float32))
    np.save(stdPath , a3std.astype(float32))

    print meanPath
    print stdPath
