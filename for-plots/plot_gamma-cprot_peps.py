#!/bin/python3

#########################################################################
# This script plot:
# gamma vs protein concentration
# for one pH value 
# for multiple peptides
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
path1='Puddu2012_seq1-KLPGWSG_cprot-*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
path2='Puddu2012_seq2-AFILPTG_cprot-*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
path3='Puddu2012_seq3-LDHSLHS_cprot-*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
pH = 7.0
unit = 'mg'












#####################################################################
paths1 = sorted(glob.glob(paths1)
paths2 = sorted(glob.glob(paths2)
paths3 = sorted(glob.glob(paths3)
paths_peps = [paths1, paths2, paths3]

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

# loop for each file:
for paths in paths_peps:
    
    # apped gamma and cprot into two list:
    gamma_list= []
    cprot_list = []
    
    # loop for each file:
    for path in paths:
    
        # load file:   
        df = pd.read_csv(path, header=None, sep='\s+', names=['pH', 'gamma'])

        # get gamma:
        df_to_pH = df[df['pH'] == pH]
        gamma = df_to_pH['gamma'].values[0]
        
        # get sequence:
        seq = re.search(r'_seq\d+-(\w+)_', path).group(1)
                
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
    ax.plot(cprot_list, gamma_list, marker='o', label= f'{seq}')

# format:
# choose units:
if unit == 'mg':
    ax.set_xlabel("cprot (mg/ml)", fontsize=12, font=font_for_text)
    ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12, font=font_for_text)
else:
    ax.set_xlabel("cprot (M)", fontsize=12)
    ax.set_ylabel("$\Gamma$ (molecules nm$^{-2})$", fontsize=12, font=font_for_text)
 
ax.set_box_aspect(1)
add_text(ax, f'pH = {pH}\n[NaCl] = {csalt} M', location='custom', offset=(0.1, 0.2), fontsize=12, fontprop=font_for_text)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='center',
          fontsize=12,
          frameon=False)

#plt.xlim(0, 1)
# select scale:
ax.set_xscale('log')

# set font for number:
set_font_for_numbers(ax,font_for_numbers)

plt.show()

save_file(fig, f'fig_gamma-cprot_peps.png') 

exit()
