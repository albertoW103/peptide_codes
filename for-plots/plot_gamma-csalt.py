#!/bin/python3

import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.font_manager import FontProperties
import sys
import re

#####################################################################
# how to run the script:
'''

python3 plot_gamma-csalt.py {path1} {path1} {path1} {pH} {unit}
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
path1 = sys.argv[1]
path2 = sys.argv[2]
path3 = sys.argv[3]
paths = [path1, path2, path3]

pH = float(sys.argv[4])
unit = sys.argv[5]

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

#####################################################################
# format:
# choose units:
if unit == 'mg':
    ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12)
else:
    ax.set_ylabel("$\Gamma$ (molecules nm$^{-2})$", fontsize=12)
    
ax.set_box_aspect(1)
ax.set_xlabel("csalt (M)", fontsize=12)
ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12)
add_text(ax, f'{seq}\n[cprot] = {cprot} M\nconfs = {confs}', location='custom', offset=(0.1, 0.2), fontsize=12)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='center',
          fontsize=12,
          frameon=False)

#ax.set_xscale('log')

plt.show()

save_file(fig, f'fig_gamma-csalt_{seq}.png') 

exit()
