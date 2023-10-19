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

files = sorted(glob.glob('Puddu2012_seq3-LDHSLHS_cprot-1d6_csalt-*_confs-2500_rsize-1_dz-0.50/gamma_peptide-pH.dat'))

pH_list = [7.5]
seq = files[0].split('/')[0].split('_')[1].split('-')[1]
cprot = files[0].split('/')[0].split('_')[2].split('-')[1]
#csalt = files[0].split('/')[0].split('_')[3].split('-')[1]
confs = files[0].split('/')[0].split('_')[4].split('-')[1]
rsize = files[0].split('/')[0].split('_')[5].split('-')[1]

# convertions:
cprot = convert_1dx_xxx(cprot)

################
fig, ax=plt.subplots()
for pH in pH_list:
    gamma_list= []
    csalt_list = []
    for file in files:
        df = pd.read_csv(file, header=None, sep='\s+', names=['pH', 'gamma'])
    
        # y value (gamma):
        gamma = df[df['pH'] == pH]
        gamma_list.append(gamma['gamma'].values[0])
    
        # x value (csalt):
        csalt = file.split('/')[0].split('_')[3].split('-')[1]
        csalt = float(csalt)
        csalt_list.append(csalt)

    # get molecular weight:
    mw = mw_from_sequence(seq)

    # change y_scale from molecules/nm2 to mg/m2:
    gamma_list = [gamma_molec_to_mg_m2(x, mw) for x in gamma_list]
    
    # plot:
    ax.plot(csalt_list, gamma_list, marker='o', label='pH = ' + str(pH))

# format:
ax.set_box_aspect(1)
ax.set_xlabel("csalt (M)", fontsize=12)
ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12)
#ax.set_ylabel("$\Gamma$ (molecules nm$^{-2})$", fontsize=12)
add_text(ax, '{}\n[cprot] = {} M\nconfs = {}'.format(seq, cprot, confs), location='custom', offset=(0.1, 0.2), fontsize=12)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='center',
          fontsize=12,
          frameon=False)

ax.set_xscale('log')

plt.show()

save_file(fig, 'figure_gamma-csalt_{}.png'.format(seq)) 

exit()
