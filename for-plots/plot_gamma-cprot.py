#!/bin/python3

#########################################################################
# This script plot:
# gamma vs protein concentration
# for one pH value or multiples pH value 
# for one peptide
#
# Add * to select a list of files at different configurations
#########################################################################

import matplotlib.pyplot as plt
import pandas as pd
import glob as glob
import os
import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.font_manager import FontProperties
import re
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

# plots:
plt.style.use("~/Research/github/my_styles/temp_origin0.mpstyle")
fig, ax=plt.subplots()

# loop for each pH value:
for pH in pHs:

    # apped gamma and cprot into two list:
    gamma_list= []
    cprot_list = []
    
    # loop for each path:
    for path in paths:
    
        # from path load a file:
        df = pd.read_csv(path, header=None, sep='\s+', names=['pH', 'gamma'])

        # get gamma:
        df_to_pH = df[df['pH'] == pH]
        gamma = df_to_pH['gamma'].values[0]
        
        # get molecular weight:
        mw = mw_from_sequence(seq)
        
        # choose units:
        if unit == 'mg':
            # covert gamma unit from molecules/nm2 to mg/m2:
            gamma = gamma_molec_to_mg_m2(gamma, mw)
            
            # append gamma into gamma list:
            gamma_list.append(gamma)
            
        else:
            # left gamma unit in molecules/nm2:
            continue

        # get cprot:
        cprot = path.split('cprot-')[1].split('_')[0]
        cprot = convert_1dx_xxx(cprot)
        cprot = float(cprot)
        
        # choose units:
        if unit == 'mg':
            # covert cprot unit from M to mg/ml:
            cprot = cprot*mw
            
            # append coprot into cprot list:     
            cprot_list.append(cprot)
            
        else:
            # left cprot unit in M:
            continue

    # get plot:
    ax.plot(cprot_list, gamma_list, marker='o', label= 'pH = ' + str(pH))

# format:
# choose units:
if unit == 'mg':
    ax.set_xlabel("cprot (mg/ml)", fontsize=12)
    ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12, font=font_for_text)
else:
    ax.set_xlabel("cprot (M)", fontsize=12)
    ax.set_ylabel("$\Gamma$ (molecules nm$^{-2})$", fontsize=12, font=font_for_text)

add_text(ax, f'{seq}\n[NaCl] = {csalt} M\nconfs = {confs}', location='custom', offset=(0.1, 0.2), fontsize=12, fontprop=font_for_text)      
ax.set_box_aspect(1)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='center',
          fontsize=12,
          frameon=False)

# select scale:
ax.set_xscale('log')

# set font for number:
set_font_for_numbers(ax,font_for_numbers)

plt.show()

save_file(fig, f'fig_gamma-cprot_{seq}.png')

exit()
