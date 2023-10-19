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
# import this to run my_funtions.py:
import sys
sys.path.append('/home/wilson/Research/styles_and_functions/')
from my_functions import *
#####################################################################

files = natsorted(glob.glob('familypep-1_seq1-DSARGFKKPGK_cprot-1d6_csalt-0.1_confs-*_rsize-1_dz-0.50/gamma_peptide-pH.dat'))
#files = list(os.system('ls -1v familypep-1_seq1-DSARGFKKPGK_cprot-1d6_csalt-0.1_confs-*_rsize-1_dz-0.50/gamma_peptide-pH.dat'))

seq = files[0].split('/')[0].split('_')[1].split('-')[1]
cprot = files[0].split('/')[0].split('_')[2].split('-')[1]
csalt = files[0].split('/')[0].split('_')[3].split('-')[1]
#confs = files[0].split('/')[0].split('_')[4].split('-')[1]
rsize = files[0].split('/')[0].split('_')[5].split('-')[1]

# convertions:
cprot = convert_1dx_xxx(cprot)

# get plot:
fig, ax=plt.subplots()
for file in files:
    df = pd.read_csv(file, header=None, sep='\s+', names=['pH', 'gamma'])
    seq = file.split('/')[0].split('_')[1].split('-')[1]
    confs_list = file.split('/')[0].split('_')[4].split('-')[1]
    
    #### add bold on K, R and H ###
    bold_letters = ['K', 'R', 'H']  # Specify the letters to be bolded
    seq_formatted = ''
    for letter in seq:
        if letter in bold_letters:
            seq_formatted += r'$\mathbf{' + letter + '}$'
        else:
            seq_formatted += letter
    ##### end bold ###

    # get molecular weight:
    mw = mw_from_sequence(seq)

    # change y_scale from molecules/nm2 to mg/m2:
    gamma_list = [gamma_molec_to_mg_m2(x, mw) for x in df['gamma']]
    
    # plot:
    ax.plot(df['pH'], gamma_list, label=confs_list)

# format:
ax.set_box_aspect(1)
ax.set_xlabel("pH", fontsize=12)
ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12)
#ax.set_ylabel("$\Gamma$ (molecules nm$^{-2})$", fontsize=12)
add_text(ax, '{}\n[NaCl] = {} M\n[C] = {} M}'.format(seq, csalt, cprot), location='custom', offset=(0.7, 0.75), fontsize=10)
ax.set_xlim(1.0, 12.0)
ax.legend(prop={'size':8, 'family': 'monospace'},
          loc='upper left',
          fontsize=12,
          frameon=False)
ax.set_xlim(1.0, 12.0)

# call my functions for style:
style_ticks_plot(ax, 1)

plt.show()
save_file(fig, 'figure_gamma-pH_{}.png'.format(seq)) 

exit()
