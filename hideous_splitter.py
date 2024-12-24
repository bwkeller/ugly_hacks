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

def split_aux_2phase(fname, ratio, text=False):
    if text:
        massHot = np.genfromtxt(fname+'.massHot', skip_header=1)
        u = np.genfromtxt(fname+'.u', skip_header=1)
        uHot = np.genfromtxt(fname+'.uHot', skip_header=1)
    else:
        massHot = rarray(fname+'.massHot')
        u = rarray(fname+'.u')
        uHot = rarray(fname+'.uHot')
    h,g,d,s = rtipsy(fname)
    mass = g['mass']
    frac = ratio*massHot[:h['ngas']]/mass
    num_full = np.floor(frac)
    leftovers = (frac - num_full)*mass
    repidx = np.tile(np.arange(ratio), h['ngas'])
    fullidx = np.repeat(leftovers, ratio)
    split_massHot = np.repeat(np.zeros(mass.shape), ratio)
    split_uHot = np.repeat(np.zeros(mass.shape), ratio)
    split_u = np.repeat(np.zeros(u[:h['ngas']), ratio)
    split_mass = np.repeat(mass, ratio)

    split_massHot[repidx == fullidx] = leftovers
    split_uHot[repidx == fullidx] = uHot[:h['ngas']]
    split_u[repidx < fullidx] = np.repeat(uHot[:h['ngas']], ratio)[repidx < fullidx]

    split_massHot_all = np.repeat(np.zeros(massHot.shape), ratio)
    split_massHot_all[:h['ngas']*ratio] = split_massHot
    split_uHot_all = np.repeat(np.zeros(uHot.shape), ratio)
    split_uHot_all[:h['ngas']*ratio] = split_uHot

    warray('split_'+str(ratio)+'_'+fname+'.massHot', split_massHot_all)
    warray('split_'+str(ratio)+'_'+fname+'.u', split_u_all)
    warray('split_'+str(ratio)+'_'+fname+'.uHot', split_uHot_all)

def split_aux(fname, ratio, text=False):
    if fname.split('.')[-1] in ['massHot', 'u', 'uHot']:
        return
    if text:
        data = np.genfromtxt(fname, skip_header=1)
    else:
        data = rarray(fname)
    if fname.split('.')[-1] in ['massform', 'ESNRate']:
        data =/ ratio
    warray('split_'+str(ratio)+'_'+fname, np.repeat(data, ratio))

if __name__ == "__main__":
    if lens(argv) < 3:
        print("USAGE: hideous_splitter.py snapshot_filename split_ratio") 
    filename = argv[1]
    ratio = int(argv[2])
    aux_files = glob(filename+".*")
