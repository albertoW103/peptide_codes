#!/bin/python3
#nota
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

#files = natsorted(glob.glob('Puddu2012_seq1-KLPGWSG_*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'))
#files = natsorted(glob.glob('Puddu2012_seq2-AFILPTG_*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'))
files = natsorted(glob.glob('Puddu2012_seq3-LDHSLHS_*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'))

pH_list = [3, 5, 7.5, 8.5]
seq = files[0].split('/')[0].split('_')[1].split('-')[1]
#cprot = files[0].split('/')[0].split('_')[2].split('-')[1]
csalt = files[0].split('/')[0].split('_')[3].split('-')[1]
confs = files[0].split('/')[0].split('_')[4].split('-')[1]
rsize = files[0].split('/')[0].split('_')[5].split('-')[1]

#############################
fig, ax=plt.subplots()
for pH in pH_list:
    gamma_list= []
    cprot_list = []
    for file in files:
        df = pd.read_csv(file, header=None, sep='\s+', names=['pH', 'gamma'])
    
        # y value:
        gamma = df[df['pH'] == pH]
        gamma_list.append(gamma['gamma'].values[0])
    
        # x value:
        cprot = file.split('/')[0].split('_')[2].split('-')[1]
        cprot = convert_1dx_xxx(cprot)
        cprot = float(cprot)
        cprot_list.append(cprot)

    # get molecular weight:
    mw = mw_from_sequence(seq)
    
    # change y_scale from molecules/nm2 to mg/m2:
    gamma_list = [gamma_molec_to_mg_m2(x, mw) for x in gamma_list]
    
    # get plot:
    ax.plot(cprot_list, gamma_list, marker='o', label= 'pH = ' + str(pH))

# format:
ax.set_box_aspect(1)
ax.set_xlabel("cprot (M)", fontsize=12)
#ax.set_ylabel("$\Gamma$ (molecules nm$^{-2})$", fontsize=12)
ax.set_ylabel("$\Gamma$ (mg m$^{-2})$", fontsize=12)
add_text(ax, '{}\n[NaCl] = {} M\n confs = {}'.format(seq, csalt, confs), location='custom', offset=(0.1, 0.2), fontsize=12)
ax.legend(prop={'size':12, 'family': 'monospace'},
          loc='center',
          fontsize=12,
          frameon=False)

ax.set_xscale('log')

plt.show()

save_file(fig, 'figure_gamma-cprot_{}.png'.format(seq)) 

exit()
