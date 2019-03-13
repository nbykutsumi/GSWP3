import glob
import os, shutil
import subprocess
lvarName = ["SWdown","LWdown","Tair","Qair","PSurf","Prcp","Wind"]

obaseDir = '/work/a01/utsumi/GSWP3/insitu'

ibaseDir =  '/work/a01/utsumi/GSWP3'

for varName in lvarName:
    ssearch   = obaseDir + '/%s/*'%(varName)
    loutDir  = glob.glob(ssearch)

    for outDir in loutDir:
        siteName = outDir.split('/')[-1]

        inDir = ibaseDir + '/%s/%s'%(varName,siteName)


        if os.path.exists(inDir):
            lsrcPath = glob.glob(inDir+'/*')
            for srcPath in lsrcPath:
                scmd = 'mv %s %s/'%(srcPath, outDir)
                print scmd
                subprocess.call(scmd.split())
