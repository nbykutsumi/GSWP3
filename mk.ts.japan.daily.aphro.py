import matplotlib
matplotlib.use('Agg')
from numpy import *
from datetime import datetime, timedelta
import myfunc.util as util
import calendar
import numpy as np
import matplotlib.pyplot as plt

miss_in = -999.9
miss_out= -9999.
#lYear  = range(1900,2010+1)
lYear  = range(1984,2010+1)


for Year in lYear:
    srcDir = '/work/data1/hjkim/APHRODITE/AphroJP_V1207_DPREC.CSTN'
    srcPath = srcDir + '/AphroJP_V1207_DPREC.CSTN.%04d'%(Year)
    a3in = fromfile(srcPath,float32).reshape(-1,440,460)

    lout = []
    for iday in range(a3in.shape[0]):
        a2in = a3in[iday]
        vout = ma.masked_less(a2in,0).mean()
        lout.append(vout)

    sout = util.list2csv(lout)

    #-- Save ------ 
    outDir = '/work/a01/utsumi/GSWP3/VS_APHRO_JP/APHRO_JP'
    util.mk_dir(outDir)
    outPath= outDir + '/prcp.daily.JPN.APHRO_JP.%04d.csv'%(Year)
    f=open(outPath,'w'); f.write(sout); f.close()

    print outPath

    #fig = plt.figure()
    #ax  = fig.add_axes()
    #plt.imshow(a2out, origin='lower')
    #plt.savefig(outPath+ '.png')
    #print outPath
    #plt.clf()

