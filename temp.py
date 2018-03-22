from numpy import *
import numpy as np
import os, sys
import WFDEI

wf = WFDEI.WFDEI()
varName = "PSurf"
nc = wf.loac_nc(varName, 2014,1, compressed=True)
print nc
