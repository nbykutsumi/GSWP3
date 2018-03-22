from numpy import *
from myfunc.regrid import Regrid



LatOrg = arange(-89.75,89.75+0.0001,0.5)
LonOrg = arange(0.25,359.75+0.0001,0.5)

LatUp  = arange(-89.5,89.5+0.0001,1.0)
LonUp  = arange(0.5,359.5+0.0001,1.0)


us = Regrid.UpScale()
us(LatOrg, LonOrg, LatUp, LonUp, globflag=True)

srcPath = "/work/a01/utsumi/GSWP3/const/cru_ts3.23.1901.2014.halfdesg.elv.02.sa.hlf"
outPath = "/work/a01/utsumi/GSWP3/const/cru_ts3.23.1901.2014.halfdesg.elv.02.sa.one"

a2org = fromfile(srcPath,float32).reshape(360,720)
a2up  = us.upscale(a2org, pergrid=False, miss_in=-999., miss_out=-999.)

a2up.tofile(outPath)
print outPath

