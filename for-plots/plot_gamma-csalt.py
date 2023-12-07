#!/bin/python3

#########################################################################
# This script plot:
# gamma vs salt concentration
# for one pH value 
# for multiple peptides
#########################################################################

import matplotlib.pyplot as plt
import pandas as pd
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
path1='Puddu2012_seq1-KLPGWSG_cprot-1d6_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
path2='Puddu2012_seq1-KLPGWSG_cprot-1d6_csalt-0.01_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
path3='Puddu2012_seq1-KLPGWSG_cprot-1d6_csalt-0.001_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
pH = 7
unit = 'mg'











#####################################################################
paths = [path1, path2, path3]

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

    # load file:
    df = pd.read_csv(path, header=None, sep='\s+', names=['pH', 'gamma'])

    # get molecular weight from peptide sequence:
    seq = re.search(r'_seq\d+-(\w+)_', path).group(1)
    mw = mw_from_sequence(seq)

    # choose units:
    if unit == 'mg':
        # convert gamma from molecules/nm2 to mg/m2:
        gamma_list = [gamma_molec_to_mg_m2(x, mw) for x in df['gamma']]
            
    else:
        # left gamma unit in molecules/nm2:
        continue
        
    # get salt concentration:
    csalt = path.split('csalt-')[1].split('_')[0]
        
    # get plot:
    ax.plot(df['pH'], df['gamma'], label= f'[NaCl] = {csalt} M')

# format:
# choose units:
if unit == 'mg':
    ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12, font=font_for_text)
else:
    ax.set_ylabel("$\Gamma$ (molecules nm$^{-2})$", fontsize=12, font=font_for_text)
    
ax.set_box_aspect(1)
ax.set_xlabel("csalt (M)", fontsize=12)
ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12)
add_text(ax, f'{seq}\n[cprot] = {cprot} M\nconfs = {confs}', location='custom', offset=(0.1, 0.2), fontsize=12, fontprop=font_for_text)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='center',
          fontsize=12,
          frameon=False)

# select scale:
#ax.set_xscale('log')

# set font for number:
set_font_for_numbers(ax,font_for_numbers)

plt.show()

save_file(fig, f'fig_gamma-csalt_{seq}.png') 

exit()
