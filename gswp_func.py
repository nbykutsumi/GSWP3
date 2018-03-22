from numpy import *

def load_orog(res="hlf"):
    if   res=="hlf": ny,nx = 360, 720
    elif res=="one": ny,nx = 180, 360
    srcPath = "/work/a01/utsumi/GSWP3/const/cru_ts3.23.1901.2014.halfdesg.elv.02.sa.%s"%(res)
    return fromfile(srcPath, float32).reshape(ny,nx) 




