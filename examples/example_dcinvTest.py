# -*- coding: utf-8 -*-

"""
Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""

import numpy as np
import os, sys, time
from argparse import ArgumentParser
from copy import deepcopy
try:
    from mpi4py import MPI
    mpi_exist = True
except ImportError:
    mpi_exist = False
try:
    from evodcinv import DispersionCurve, LayeredModel, progress
except ImportError:
    sys.path.append("../")
    from evodcinv import DispersionCurve, LayeredModel, progress
    

if __name__ == "__main__":
    # Initialize MPI
    if mpi_exist:
        mpi_comm = MPI.COMM_WORLD
        mpi_rank = mpi_comm.Get_rank()
    else:
        mpi_rank = 0

    print(mpi_rank)
        
    # Parse arguments
    parser = ArgumentParser()
    parser.add_argument("-n", "--num_threads", type = int, default = 8)
    args = parser.parse_args()
        
    # Parameters
    ny = 200                        # Number of velocity discretization points
    max_run = 10                    # Number of runs
    outdir = "test_ewe"               # Output directory
    
    # Inversion boundaries
    # - params
    # - beta: S-wave boundaries in m/s
## TestParam for 2.0 thickness Ratio
   # beta = np.array([ [ 100., 1000. ], [ 500., 2500. ], [ 1000., 4000. ],[ 1000., 4000. ],[ 1000., 4000. ]])#,[1200.,4200. ]])
    # - NOTE: final layer 
   # thickness = np.array([ [ 20., 60. ], [ 30., 60. ] ,[60.,120],[120.,240.],[ 99999., 99999. ] ])
## TestParam for 3.0 thickness Ratio  
#    beta = np.array([ [ 100., 1000. ], [ 500., 2500. ], [ 1000., 4000. ],[ 1000., 4000. ],[ 1000., 4000. ]])#,[1200.,4200. ]])
    # - NOTE: final layer 
#    thickness = np.array([ [ 20., 60. ], [ 30., 60. ] ,[60.,180],[120.,660.],[ 99999., 99999. ] ])
## TestParams 3.0 for DAS data
    beta = np.array([ [ 100., 1000. ], [ 500., 2500. ], [ 1000., 4000. ],[ 1000., 4000. ]])#,[1200.,4200. ]])
    # - NOTE: final layer 
    thickness = np.array([ [ 40., 100. ], [ 50., 200. ] ,[500.,1200],[ 99999., 99999. ] ])
    
    # Initialize dispersion curves
    # - param in tuple. filename, wtype, mode
    # data- frequency list - phase vel
    # - 97 data points in the example
        #( "data/ewe_mode0.txt", "rayleigh", 0 ),
    disp_param = [
        ( "data/HRLRT/test2.5kDm--060.txt","rayleigh", 0 ),

        ]
    
    dcurves = []
    for param in disp_param:
        filename, wtype, mode = param
        faxis, disp = np.loadtxt(filename, unpack = True)
        dc = DispersionCurve(disp, faxis, mode, wtype)
        dcurves.append(dc)

    # Evolutionary optimizer parameters
    ## Edit this for loop control
    evo_kws = dict(popsize = 20, max_iter = 30, constrain = True, mpi = mpi_exist)
    opt_kws = dict(solver = "cpso")
        
    # Multiple inversions
    # - first proc make the folder
    if mpi_rank == 0:
        starttime = time.time()
        os.makedirs(outdir, exist_ok = True)
        progress(-1, max_run, "perc", prefix = "Inverting dispersion curves: ")
        
    # list of layered models
    models = []
    for i in range(max_run):
        lm = LayeredModel()
        lm.invert(dcurves, beta, thickness, ny = ny, n_threads = args.num_threads,
                  evo_kws = evo_kws, opt_kws = opt_kws)
        if mpi_rank == 0:
            # inversion results are saved in pickle
            # whole lm object
            lm.save("%s/run%d.pickle" % (outdir, i+1))
            models.append(deepcopy(lm))
            progress(i, max_run, "perc", prefix = "Inverting dispersion curves: ")
        
#    if mpi_rank == 0:
    with open('invResult.txt',"a") as myfile:
        print("\n",file=myfile)
        misfits = [ m.misfit for m in models ]
        print(models[np.argmin(misfits)],file=myfile)
        print("Elapsed time: %.2f seconds\n" % (time.time() - starttime),file=myfile)
