#! /usr/bin/python
#--------------------------------------------------------------------
# PROGRAM    : bin2nc.py
# CREATED BY : hjkim @IIS.2017-04-30 06:47:26.462474
# MODIFED BY :
#
# USAGE      : $ ./bin2nc.py
#
# DESCRIPTION: for package s_wata Wind to GSWP3 Wind
#------------------------------------------------------cf0.2@20120401


import  os,sys
from    optparse                import OptionParser
from    cf.util.LOGGER          import *

from    netCDF4                 import Dataset
import  numpy       as np
import  glob

#from    collections             import OrderedDict  as odict    # DO NOT USE. DICTIONARY ORDER CHANGE
from    cf2.utils.ordereddict   import OrderedDict  as odict





def get_ncattr( ncobj ):

    ncattr      = odict( [ (attr, ncobj.getncattr( attr )) for attr in ncobj.ncattrs() ] )

    return ncattr


def set_ncattr( ncobj, attrs ):

    for k, v in attrs.items():
        ncobj.setncattr( k, v )


@ETA
def main(args,opts):
    print args
    print opts

    #srcpath = int(args[0])
    #despath = int(args[1])

    srcpath = '/data2/hjkim/GSWP3/in/EXP1/Wind.ori/GSWP3.BC.Wind.3hrMap.1901.nc'
    despath = '/data2/hjkim/GSWP3/from_tank.bin/out/Wind/GSWP3.Wind.2013-2013.nc'

    # EDIT --------------------------------------------------------------------
    addattr = odict((
              ('__global__', ['contributors', 'Satoshi Watanabe, Eun-Chul Chang, Nobuyuki Utsumi, Kei Yoshimura, Gilbert Compo, Hirabayashi Yukiko, James Famiglietti, and Taikan Oki'],),
              ))

    print addattr

    # SRC ----------------------------------------------------------------------
    ncsrc   = Dataset( srcpath )

    ncvars  = [ (name, ncvar) for name, ncvar in ncsrc.variables.iteritems() ]
    ncobjs  = ncvars + [ ('__global__', ncsrc) ]

    srcattrs= odict( [ (name, get_ncattr( ncobj )) for name, ncobj in ncobjs ] )

    ncsrc.close()
    # -------------------------------------------------------------------------

    '''
    ncattrs = odict()

    for var,attrs in srcattrs.items():
        ncattrs[ var ] = odict()

        for k,v in attrs.items():

            ncattrs[ var ][k]   = v if k not in addattr[ var ]

            if k in addattr[ var ]:

            print k,v
    '''


    # DESTINATION -------------------------------------------------------------
    ncdes   = Dataset( despath, 'r+' )

    ncobjs  = odict([ (name, ncvar) for name, ncvar in ncdes.variables.iteritems() ])
    ncobjs['__global__']    = ncsrc

    for name, ncobj in ncobjs.items():
        set_ncattr( ncobj, ncattrs[ name ] )

    for var, attrs in addattr.items():

        for k,v in attrs.items():
        ncobjs[ var ]

    ncdes.close()
    # -------------------------------------------------------------------------




    print ncattrs


    sys.exit()

    for year in range(syear, eyear+1):
        print '*'*100
        print '*', year
        print '*'*100
        bin2nc( year, outdir )
        print '*'*100


    return


if __name__=='__main__':
    usage   = 'usage: %prog [options] arg'
    version = '%prog 1.0'

    parser  = OptionParser(usage=usage,version=version)

#    parser.add_option('-r','--rescan',action='store_true',dest='rescan',
#                      help='rescan all directory to find missing file')

    (options,args)  = parser.parse_args()

#    if len(args) == 0:
#        parser.print_help()
#    else:
#        main(args,options)

#    LOG     = LOGGER()
    main(args,options)


