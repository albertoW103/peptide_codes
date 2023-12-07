#!/bin/python3

#########################################################################
# This script plot:
# gamma vs configurations
# for multiples pH values 
# for one peptide
#########################################################################

import matplotlib.pyplot as plt
import pandas as pd
import glob as glob
import os
import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.font_manager import FontProperties
import re
from natsort import natsorted
sys.path.append(os.path.expanduser('~/Research/github/my_functions/'))
from my_functions import *
from my_functions_style import *

#####################################################################
# inputs:
paths='familypep-1_seq1-DSARGFKKPGK_cprot-1d6_csalt-0.1_confs-*_rsize-1_dz-0.50/gamma_peptide-pH.dat'
pHs = [7.0, 7.5]
units = 'mg'







#####################################################################
paths = natsorted(glob.glob(paths))

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

# format:
# choose units:
if unit == 'mg':
    ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12, font=font_for_text)
else:
    ax.set_ylabel("$\Gamma$ (molecules nm$^{-2})$", fontsize=12, font=font_for_text)

ax.set_box_aspect(1)
ax.set_xlabel("pH", fontsize=12, font=font_for_text)
ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12, font=font_for_text)
add_text(ax, f'{seq}\n[NaCl] = {csalt} M\n[C] = {cprot} M', location='custom', offset=(0.7, 0.75), fontsize=10, fontprop=font_for_text)
ax.set_xlim(1.0, 12.0)
ax.legend(prop={'size':8, 'family': 'monospace'},
          loc='upper left',
          fontsize=12,
          frameon=False)
ax.set_xlim(1.0, 12.0)

# call my functions for style:
style_ticks_plot(ax, 1)

# set font for number:
set_font_for_numbers(ax,font_for_numbers)

plt.show()

save_file(fig, f'fig_gamma-pH-confs_{seq}.png') 

exit()
