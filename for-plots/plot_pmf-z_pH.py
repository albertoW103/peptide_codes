#!/bin/python3

import matplotlib.pyplot as plt
import pandas as pd
import glob as glob
import os
import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.font_manager import FontProperties
import re
from natsort import natsorted
import sys
sys.path.append(os.path.expanduser('~/Research/github/my_functions/'))
from my_functions import *
from my_functions_style import *

#####################################################################
# how to run the script:
'''

python3 plot_pmf-z_pH.py {path1} {pH}

'''


#####################################################################
# inputs:
paths = natsorted(glob.glob(sys.argv[1]))
pH = sys.argv[2]

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

#############################
# plot:
fig, ax=plt.subplots()

# loop for each file:
for path in paths:
    
    # read file:
    df = pd.read_csv(path, header=None, comment='#', skiprows=3, sep='\s+')
    df = df.iloc[:, :2]
    df.columns = ['z', 'pmf']
    
    # get confs:
    confs = path.split('confs-')[1].split('_')[0] 

    # get plot:
    ax.plot(df['z'], df['pmf'], label=confs)

#####################################################################
# format:
ax.set_xlim(0, 4)
ax.set_box_aspect(1)
ax.set_xlabel("z (nm)", fontsize=12)
ax.set_ylabel("$PMF_{min}$ ($k_{B}T)$", fontsize=12)
add_text(ax, f'pH = {pH}\n[NaCl] = {csalt} M', location='custom', offset=(0.025, 0.1), fontsize=12)
ax.legend(prop={'size':8, 'family': 'monospace'},
          loc='best',
          fontsize=12,
          frameon=False)

plt.show()

save_file(fig, f'fig_pmf-z_pH_{seq}.png') 

exit()
