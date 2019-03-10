import os, sys
import subprocess
import myfunc.util as util

baseurl = 'https://vesg.ipsl.upmc.fr/thredds/catalog/work/p529viov/cruncep/V9_1901_2017/catalog.html'

baseurl = 'https://vesg.ipsl.upmc.fr/thredds/catalog/work/p529viov/cruncep/V9_1901_2017/catalog.html?dataset=DatasetScanTGCCWORK/p529viov/cruncep/V9_1901_2017'

lvar=["swdown","lwdown","rain","uwind","vwind",'tair','qair','press']
#lvar=["swdown"]

lYear = range(1901,2014+1)
#lYear = range(1901,1901+1)

for Year in lYear:
    for varName in lvar:
        srcurl = baseurl + '/cruncepv9_%s_%04d.nc.gz'%(varName, Year)

        outDir = '/work/hk01/CRUNCEP/%s'%(varName)
        outPath= outDir + '/' +  srcurl.split('/')[-1]
        util.mk_dir(outDir)
        scmd   = 'wget %s -O %s'%(srcurl, outPath)
        lcmd   = scmd.split() 
        subprocess.call(lcmd)
