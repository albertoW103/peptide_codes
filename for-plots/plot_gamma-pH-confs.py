#!/bin/python3

import matplotlib.pyplot as plt
import pandas as pd
import glob as glob
import os
import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.font_manager import FontProperties
import sys
import re
from natsort import natsorted

#####################################################################
# how to run the script:
'''

python3 plot_gamma-pH-confs.py {path1} {pHs} {unit}
{unit} = 'mg'

'''

#####################################################################
# import my_funtions.py:
current_directory = os.getcwd()                         # current directory path:
previous_directory = os.path.dirname(current_directory) # previous directory path:
sys.path.append(f'{previous_directory}/my_functions.py') 
from my_functions import *

#####################################################################
# inputs:
paths = natsorted(glob.glob(sys.argv[1]))
pHs = list(sys.argv[2].split(' '))
units = sys,.argv[3]

#####################################################################
# conditions:
seq = re.search(r'_seq\d+-(\w+)_', paths[0]).group(1)   # read peptide sequence
cprot = path[0].split('cprot-')[1].split('_')[0]        # read cprot
cprot = convert_1dx_xxx(cprot)                          # change format
csalt = paths[0].split('csalt-')[1].split('_')[0]       # read salt concentration
confs = paths[0].split('confs-')[1].split('_')[0]       # read confs
rsize = paths[0].split('rsize-')[1].split('_')[0]       # read rsize
symetry = path[0].split('symetry-')[1].split('_')[0]    # read symetry
dz = paths[0].split('dz-')[1].split('_')[0]             # read dz

#####################################################################
# plot:
fig, ax=plt.subplots()

# loop for each file:
for path in paths:

    # read file:
    df = pd.read_csv(path, header=None, sep='\s+', names=['pH', 'gamma'])
        
    # get molecular weight from peptide sequence:
    mw = mw_from_sequence(seq)
    
    # choose units:
    if unit == 'mg':
        # covert gamma unit from molecules/nm2 to mg/m2:
        gamma_list = [gamma_molec_to_mg_m2(x, mw) for x in df['gamma']]
            
    else:
        # left gamma unit in molecules/nm2:
        continue
    
    # get confs:
    confs = path.split('confs-')[1].split('_')[0] 

    # get plot:
    ax.plot(df['pH'], df['gamma'], label=confs)

#####################################################################
# format:
# choose units:
if unit == 'mg':
    ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12)
else:
    ax.set_ylabel("$\Gamma$ (molecules nm$^{-2})$", fontsize=12)

ax.set_box_aspect(1)
ax.set_xlabel("pH", fontsize=12)
ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12)
add_text(ax, f'{seq}\n[NaCl] = {csalt} M\n[C] = {cprot} M', location='custom', offset=(0.7, 0.75), fontsize=10)
ax.set_xlim(1.0, 12.0)
ax.legend(prop={'size':8, 'family': 'monospace'},
          loc='upper left',
          fontsize=12,
          frameon=False)
ax.set_xlim(1.0, 12.0)

# call my functions for style:
style_ticks_plot(ax, 1)

plt.show()
save_file(fig, f'fig_gamma-pH-confs_{seq}.png') 

exit()
