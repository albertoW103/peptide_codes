#!/bin/python3

#########################################################################
# This script plot gamma vs configuration at a single or more pHs values
# Add * to select a list of files at different configurations
#########################################################################

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
sys.path.append(os.path.expanduser('~/Research/github/my_functions/'))
from my_functions import *
from my_functions_style import *

#####################################################################
# inputs:
paths='familypep-1_seq1-DSARGFKKPGK_cprot-1d6_csalt-0.1_confs-*_rsize-1_dz-0.50/gamma_peptide-pH.dat'
paths = natsorted(glob.glob(paths)

pHs = [7.0, 7.5]           # select pH values
unit = 'mg'                # select the unit in mg











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

# plot:
plt.style.use("~/Research/github/my_styles/temp_origin0.mpstyle")
fig, ax=plt.subplots()

# loop for each pH value:
for pH in pHs:

    # append gamma and cprot into two list:
    gamma_list = []
    confs_list = []
    
    # loop for each file:
    for path in paths:
    
        # read file:
        df = pd.read_csv(path, header=None, sep='\s+', names=['pH', 'gamma'])
        
        # get gamma:
        pH = float(pH)
        df_to_pH = df[df['pH'] == pH]
        gamma = df_to_pH['gamma'].values[0]
        
        # get molecular weight from peptide sequence:
        mw = mw_from_sequence(seq)
        
        # choose units:
        if unit == 'mg':
            # covert gamma unit from molecules/nm2 to mg/m2:
            gamma = gamma_molec_to_mg_m2(gamma, mw)
            
            # append new gamma:
            gamma_list.append(gamma)
            
        else:
            # left gamma unit in molecules/nm2:
            continue
    
        # get confs:
        confs = path.split('confs-')[1].split('_')[0] 
        confs = float(confs)
        confs_list.append(confs)

    # get plot:
    ax.plot(confs_list, gamma_list, marker='o', label=f'pH = {pH}', colors=my_colors[0])

# format:
# choose units:
if unit == 'mg':
    ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12, font=font_for_text)
else:
    ax.set_ylabel("$\Gamma$ (molecules nm$^{-2})$", fontsize=12, font=font_for_text)
    
ax.set_box_aspect(1)
ax.set_xlabel("confs (n)", fontsize=12, font=font_for_text)
add_text(ax, f'{seq}\n[NaCl] = {csalt} M', location='custom', offset=(0.025, 0.1), fontsize=12, fontprop=font_for_text)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='best',
          fontsize=12,
          frameon=False)

# select scale:
ax.set_xscale('log')

# set font for number:
set_font_for_numbers(ax,font_for_numbers)

plt.show()

save_file(fig, f'fig_gamma-confs_{seq}.png') 

exit()
