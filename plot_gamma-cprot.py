#!/bin/python3

import matplotlib.pyplot as plt
import pandas as pd
import glob as glob
import os
import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.font_manager import FontProperties
import re
import sys

#####################################################################
# how to run the script:
'''
python3 plot_gamma-cprot.py {path1} {pH}

'''

#####################################################################
# import my_funtions.py:
current_directory = os.getcwd() # current directory path:
previous_directory = os.path.dirname(current_directory) # previous directory path:
sys.path.append(f'{previous_directory}/my_functions.py') 
from my_functions import *

#####################################################################
# inputs:
paths = sorted(glob.glob(sys.argv[1])) # Puddu2012_seq2-AFILPTG_cprot-*_csalt-0.01_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat
pHs = list(sys.argv[2].split(' ')) # pH = 7

#####################################################################
# conditions:
seq = re.search(r'_seq\d+-(\w+)_', paths[0]).group(1)   # read peptide sequence
csalt = paths[0].split('csalt-')[1].split('_')[0]       # read salt concentration
confs = paths[0].split('confs-')[1].split('_')[0]       # read confs
rsize = paths[0].split('rsize-')[1].split('_')[0]       # read rsize
symetry = path[0].split('symetry-')[1].split('_')[0]
dz = paths[0].split('dz-')[1].split('_')[0]             # read dz

#####################################################################
fig, ax=plt.subplots()
for pH in pHs:

    # apped gamma and cprot into two list:
    gamma_list= []
    cprot_list = []
    
    for path in paths:
    
        # load file:
        df = pd.read_csv(path, header=None, sep='\s+', names=['pH', 'gamma'])

        # y value:
        pH = float(pH)
        df_to_pH = df[df['pH'] == pH]
        gamma_list.append(df_to_pH['gamma'].values[0])

        # x value:
        cprot = path.split('cprot-')[1].split('_')[0]

        cprot = float(cprot)
        cprot_list.append(cprot)

    # get molecular weight:
    mw = mw_from_sequence(seq)

    # change y_scale from molecules/nm2 to mg/m2:
    gamma_list = [gamma_molec_to_mg_m2(x, mw) for x in gamma_list]

    # get plot:
    ax.plot(cprot_list, gamma_list, marker='o', label= 'pH = ' + str(pH))

#####################################################################
# format:
ax.set_box_aspect(1)
ax.set_xlabel("cprot (M)", fontsize=12)
ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12)
add_text(ax, f'{seq}\n[NaCl] = {csalt} M\nconfs = {confs}', location='custom', offset=(0.1, 0.2), fontsize=12)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='center',
          fontsize=12,
          frameon=False)

ax.set_xscale('log')

plt.show()

save_file(fig, f'fig_gamma-cprot_{seq}.png')

exit()
