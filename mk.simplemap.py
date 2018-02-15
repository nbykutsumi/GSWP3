import matplotlib as mpl
mpl.use("Agg")
import GSWP3
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import myfunc.util as util
import myfunc.fig.Fig as Fig
import calendar
from datetime import datetime, timedelta



prjName= "GSWP3"
expr = "EXP1"
gswp = GSWP3.GSWP3()
gswp(expr=expr)

#lvarName = ["SWdown","LWdown"]
#lvarName = ["Prcp","Wind","Tair","Qair","PSurf"]
lvarName = ["PSurf"]
baseDir = "/work/a01/utsumi/GSWP3"
#calFlag = False
calFlag = True
per_day = 8 # [#/days] (3-hour-step)
iYear = 1901
#eYear = 2014
eYear = 2010
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
miss  = -9999.

for varName in lvarName:
    for Year in lYear:
        ncIn  = gswp.load_nc(varName=varName, Year=Year)
        a3in  = ncIn.variables[varName][:]
        Lat   = ncIn.variables["lat"][:]
        Lon   = ncIn.variables["lon"][:]

        print Lat
        print Lon
        a2tmp = a3in.mean(axis=0)
        #-- figure ---
        figPath = "./tmp.%s.png"%(varName)
        cbarPath= "./tmp.cbar.%s.png"%(varName)
        Fig.DrawMapSimple(a2tmp, Lat, Lon, figname=figPath, cbarname=cbarPath)
        #-------------


    
