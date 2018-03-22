#import matplotlib as mpl
#mpl.use("Agg")
from numpy import *
import GSWP3
import matplotlib.pyplot as plt
import myfunc.util as util

prjName = "GSWP3"
expr    = "EXP1"
gswp = GSWP3.GSWP3()
gswp(expr=expr)
#lYear   = range(2000,2000+1)
lYear   = range(2000,2000+1)
#lvarName = ["LWdown"]
lvarName = ["SWdown","LWdown","Prcp","Wind","Tair","Qair","PSurf"]

#lvarName = ["Wind"]
for varName in lvarName:
    a2out = zeros([360,720],float32)
    for Year in lYear:
        nc = gswp.load_nc(varName, Year)
        a  = nc.variables[varName][0]
        print "*"*50
        print varName, Year
        print a
        



