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

#####################################################################
# how to run the script:
'''

python3 plot_pmf-z-rsize.py {path1} {pH}

'''

#####################################################################
# import my_funtions.py:
current_directory = os.getcwd()                         # current directory path:
previous_directory = os.path.dirname(current_directory) # previous directory path:
sys.path.append(f'{previous_directory}/my_functions.py') 
from my_functions import *

#####################################################################
# inputs:
paths = sorted(glob.glob(sys.argv[1]))
pH = float(sys.argv[2])

#####################################################################
# conditions:
seq = re.search(r'_seq\d+-(\w+)_', paths[0]).group(1)   # read peptide sequence
cprot = convert_1dx_xxx(cprot)                          # change format
csalt = paths[0].split('csalt-')[1].split('_')[0]       # read salt concentration
confs = paths[0].split('confs-')[1].split('_')[0]       # read confs
rsize = paths[0].split('rsize-')[1].split('_')[0]       # read rsize
symetry = path[0].split('symetry-')[1].split('_')[0]
dz = paths[0].split('dz-')[1].split('_')[0]             # read dz

#####################################################################
# plot:
fig, ax=plt.subplots()
    
# loop for each file:
for path in paths:
    
    # read file:
    df = pd.read_csv(path, header=None, comment='#', skiprows=3, sep='\s+')
    df = df.iloc[:, :2]
    df.columns = ['z', 'pmf']

# get plot:
ax.plot(df['z'], df['pmf'], marker='o', label=seq)

#####################################################################
# format:
ax.set_box_aspect(1)
ax.set_xlabel("rsize (nm)", fontsize=12)
ax.set_ylabel("$PMF_{min}$ ($k_{B}T)$", fontsize=12)
add_text(ax, f'[NaCl] = {csalt} M', location='custom', offset=(0.025, 0.1), fontsize=12)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='best',
          fontsize=12,
          frameon=False)

ax.set_xscale('log')

plt.show()

save_file(fig, f'fig_pmf-z-rsise_{seq}.png') 

exit()
