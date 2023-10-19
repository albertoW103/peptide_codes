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

files_seq1 = natsorted(glob.glob('Puddu2012_seq1-KLPGWSG_*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'))
files_seq2 = natsorted(glob.glob('Puddu2012_seq2-AFILPTG_*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'))
files_seq3 = natsorted(glob.glob('Puddu2012_seq3-LDHSLHS_*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'))
seqs = [files_seq1, files_seq2, files_seq3]

pH = [7.5]
#seq = files[0].split('/')[0].split('_')[1].split('-')[1]
#cprot = files[0].split('/')[0].split('_')[2].split('-')[1]
csalt = files_seq1[0].split('/')[0].split('_')[3].split('-')[1]
confs = files_seq1[0].split('/')[0].split('_')[4].split('-')[1]
rsize = files_seq1[0].split('/')[0].split('_')[5].split('-')[1]

#############################
# plots:
fig, ax=plt.subplots()

for seq in seqs:
    gamma_list= []
    cprot_list = []
    for file in seq:
        df = pd.read_csv(file, header=None, sep='\s+', names=['pH', 'gamma'])

        # y value (gamma):
        gamma = df[df['pH'] == pH[0]]
        gamma_list.append(gamma['gamma'].values[0])
    
        # x value (cprot):
        cprot = file.split('/')[0].split('_')[2].split('-')[1]
        cprot = convert_1dx_xxx(cprot)
        cprot = float(cprot)
        cprot_list.append(cprot)

        seq_name = file.split('/')[0].split('_')[1].split('-')[1]
        
    # convert to M to mM:
    #cprot_list = [x * 1000 for x in cprot_list]

    # get molecular weight:
    mw = mw_from_sequence(seq_name)

    # change y_scale from molecules/nm2 to mg/m2:
    gamma_list = [gamma_molec_to_mg_m2(x, mw) for x in gamma_list]
    
    # get plot:
    ax.plot(cprot_list, gamma_list, marker='o', label= '{}'.format(seq_name))

# format:
ax.set_box_aspect(1)
ax.set_xlabel("cprot (M)", fontsize=12)
# plot gammas:
ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12)
#ax.set_ylabel("$\Gamma$ (molecules nm$^{-2})$", fontsize=12)
add_text(ax, 'pH = {}\n[NaCl] = {} M'.format(pH[0], csalt), location='custom', offset=(0.1, 0.2), fontsize=12)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='center',
          fontsize=12,
          frameon=False)

#plt.xlim(0, 1)
ax.set_xscale('log')
plt.show()

save_file(fig, 'figure_gamma-cprot_peptides.png') 

exit()
