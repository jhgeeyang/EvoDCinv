# -*- coding: utf-8 -*-

"""
Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
import glob
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
    

## generate curve list 
curvelist =glob.glob("./data/DAS_pick_3km/*.txt")

## generate curve tuple - inside loop
## tag the curve filename in the inversion result
## print the output into txt file - by title
for curve in curvelist:

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
        outdir = "test_0124_4layer"               # Output directory
        
        # Inversion boundaries
        # - params
        # - beta: S-wave boundaries in m/s
        beta = np.array([ [ 100., 1000. ], [ 500., 2500. ], [ 1000., 4000. ],[1200.,4200. ]])
        # - NOTE: final layer 
        thickness = np.array([ [ 100., 1000. ], [ 100., 500. ],[100.,1000.] ,[ 99999., 99999. ] ])
        
        # Initialize dispersion curves
        # - param in tuple. filename, wtype, mode

        # data- frequency list - phase vel
        # - 97 data points in the example
        disp_param = [
            ( curve, "rayleigh", 0 ),
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
            
        if mpi_rank == 0:
# useful Output part
# but anyhow only one output is written(4 in console)
            with open(curve[20:-4]+'.txt','w') as f:
                saved_stdout = sys.stdout
                sys.stdout = f
                print("\n")
                misfits = [ m.misfit for m in models ]
# get the output of the model w/ lowest misfit. check the __str__ of layered model
                print(models[np.argmin(misfits)])
                print("Elapsed time: %.2f seconds\n" % (time.time() - starttime))
                sys.stdout.close()
                sys.stdout = saved_stdout
