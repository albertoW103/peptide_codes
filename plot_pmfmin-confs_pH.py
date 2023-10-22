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

python3 plot_pmfmin-confs_pH.py {path1}

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

#####################################################################
# conditions:
cprot = paths[0].split('cprot-')[1].split('_')[0]       # get protein concentration
cprot = convert_1dx_xxx(cprot)                          # change format
seq = re.search(r'_seq\d+-(\w+)_', paths[0]).group(1)   # read peptide sequence
csalt = paths[0].split('csalt-')[1].split('_')[0]       # read csalt
confs = paths[0].split('confs-')[1].split('_')[0]       # read confs
rsize = paths[0].split('rsize-')[1].split('_')[0]       # read rsize
symetry = path[0].split('symetry-')[1].split('_')[0]   # read symetry
dz = paths[0].split('dz-')[1].split('_')[0]             # read dz

#############################
# plot:
fig, ax=plt.subplots()

# apped gamma and cprot into two list:
pmfmin_list = []
confs_list = []
    
# loop for each file:
for path in paths:
    
    # read file:
    df = pd.read_csv(path, header=None, comment='#', skiprows=3, sep='\s+')
    df = df.iloc[:, :2]
    
    # get pmfmin:
    pmfmin = df.iloc[:, 1].min()
    pmfmin_list.append(pmfmin)
        
    # get confs:
    confs = path.split('confs-')[1].split('_')[0] 
    confs = float(confs)
    confs_list.append(confs)

# get plot:
ax.plot(confs_list, pmfmin_list, marker='o', label=seq)

#####################################################################
# format:
ax.set_box_aspect(1)
ax.set_xlabel("confs (n)", fontsize=12)
ax.set_ylabel("$PMF_{min}$ ($k_{B}T)$", fontsize=12)
add_text(ax, f'[NaCl] = {csalt} M', location='custom', offset=(0.025, 0.1), fontsize=12)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='best',
          fontsize=12,
          frameon=False)

ax.set_xscale('log')

plt.show()

save_file(fig, f'fig_pmfmin-confs_{seq}.png') 

exit()
