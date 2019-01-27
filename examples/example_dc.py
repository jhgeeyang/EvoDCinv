# -*- coding: utf-8 -*-

"""
Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
try:
    from evodcinv import ThomsonHaskell
    from evodcinv import DispersionCurve
except ImportError:
    import sys
    sys.path.append("../")
    from evodcinv import ThomsonHaskell
    

if __name__ == "__main__":
    # Parameters
    #vel = np.loadtxt("data/true_model.txt")
    vel = np.loadtxt("DAS_3km_063_5_lay_3_edit.txt")
    modes = [ int(i) for i in np.arange(3) ]
    # frequency map
    fmin, fmax, df = 0.1, 1., 0.1
    f = np.arange(fmin, fmax+df, df)
    ny = 200
    n_threads = 8
    
    # Initialize figure
    fig = plt.figure(figsize = (10, 5), facecolor = "white")
    fig.patch.set_alpha(0.)
    ax1 = fig.add_subplot(1, 2, 1)
    
    # Rayleigh-wave FC panel
    th = ThomsonHaskell(vel)
    th.propagate(f, ny = ny, domain = "fc", n_threads = n_threads)
    th.plot(axes = ax1)
    # - th pick curves and outputs curve list
    dcurves = th.pick(modes)
    for dcurve in dcurves:
# draw each curves
        dcurve.plot(axes = ax1, plt_kws = dict(color = "white", linewidth = 0.5))
    true =np.loadtxt("./data/DAS_pick_3km/DAS_3km_063.txt")
    print(dcurves[0]._phase_velocity)
    print(dcurves[0]._faxis)
    print(true[0])
    trueDC = DispersionCurve(true[:,1],true[:,0],0)
    print(trueDC._phase_velocity)
    print(trueDC._faxis)
    trueDC.plot(axes = ax1, plt_kws = dict(color = "red", linewidth = 0.5))

    ax1.set_title("Rayleigh-wave")
    
#   # Love-wave FC panel
#   th = ThomsonHaskell(vel, "love")
#   th.propagate(f, ny = ny, domain = "fc", n_threads = n_threads)
#   th.plot(axes = ax2)
#   dcurves = th.pick(modes)
#   for dcurve in dcurves:
#       dcurve.plot(axes = ax2, plt_kws = dict(color = "white", linewidth = 0.5))
#   ax2.set_title("Love-wave")

    fig.tight_layout()
    fig.show()
    plt.savefig('foo.png')
