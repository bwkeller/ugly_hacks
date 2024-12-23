#!/usr/bin/env python3

from sys import argv
from glob import glob
import numpy as np
from pytipsy import rtipsy, wtipsy, rarray, warray

def split_snap(fname, ratio):
    h,g,d,s = rtipsy(fname)
    h['n'] *= ratio
    h['ngas'] *= ratio
    h['ndark'] *= ratio
    h['nstar'] *= ratio
    for p in [g,d,s]:
        for k in p.keys():
            p[k] = np.repeat(p[k], ratio)
            if k == 'mass':
                p[k] /= ratio
            if k == 'pos':
                p[k] *= 1 + 1e-7*(np.random.rand(p[k].shape)-0.5)
    wtipsy('split_'+str(ratio)+'_'+fname, h,g,d,s)

if __name__ == "__main__":
    if lens(argv) < 3:
        print("USAGE: hideous_splitter.py snapshot_filename split_ratio") 
    filename = argv[1]
    ratio = int(argv[2])
    aux_files = glob(filename+".*")
