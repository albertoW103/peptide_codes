#!/bin/python3

import matplotlib.pyplot as plt
import pandas as pd
import glob as glob
import os
import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.font_manager import FontProperties
from natsort import natsorted

#####################################################################
# import this to run my_funtions.py:                                #
import sys                                                          #
sys.path.append('/home/wilson/Research/styles_and_functions/')      #
from my_functions import *                                          #
#####################################################################

files = 'Puddu2012_seq1-KLPGWSG_cprot-*_csalt-0.1_confs-1000_rsize-*_dz-0.50/peptide_T300.0cs1.00E-01pH07.00.dat'

print(files)
exit()
seq = files[0].split('/')[0].split('_')[1].split('-')[1]
#cprot = files[0].split('/')[0].split('_')[2].split('-')[1]
csalt = files[0].split('/')[0].split('_')[3].split('-')[1]
confs = files[0].split('/')[0].split('_')[4].split('-')[1]
#rsize = files[0].split('/')[0].split('_')[5].split('-')[1]

pH = 7.0

# convertions:
cprot = convert_1dx_xxx(cprot)

#############################
# plots:
fig, ax=plt.subplots()

for rsize in rsize_list:

    pmfmin_list = []
    cprot_list = []
    for file in files:
        # get data:
        df = pd.read_csv(file, skiprows=3, header=None, sep='\s+', usecols=[0,1], names=['r', 'pmf'])
    
        # get pmf_min:
        pmfmin = df['pmf'].min()
        pmfmin_list.append(pmfmin)
    
        # ge cprot:
        cprot = file.split('/')[0].split('_')[2].split('-')[1]
        cprot_list.append(cprot)
    
    # get sequence:
    rsize = file[0].split('/')[0].split('_')[5].split('-')[1]
    
    # get plot:
    ax.plot(df['r'], df['pmf'], linestyle='solid', label='rsize = {}'.format())

# format:
ax.set_box_aspect(1)
ax.set_xlabel("r (nm)", fontsize=12)
ax.set_ylabel("$PMF$ ($k_BT)$", fontsize=12)
add_text(ax, 'pH = {}\n[NaCl] = {} M\n[cprot] = {}\nconfs = {}'.format(pH, csalt, cprot, confs), location='custom', offset=(0.1, 0.2), fontsize=12)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='center',
          fontsize=12,
          frameon=False)
plt.xlim(0, 10)
plt.show()

save_file(fig, 'figure_pmf-r_peptides.png') 

exit()
