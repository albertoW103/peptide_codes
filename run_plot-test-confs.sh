#!/bin/bash

# plot gammas:
path='familypep-1_seq1-DSARGFKKPGK_cprot-1d6_csalt-0.1_confs-*_rsize-1_dz-0.50/gamma_peptide-pH.dat'
pH='7 7.5'
./../plot_gamma-pH-confs.py "$path"
./../plot_gamma-confs_pH.py "$path" "$pH"


# plot pmfs for one peptide:
path='familypep-1_seq1-DSARGFKKPGK_cprot-1d6_csalt-0.1_confs-*_rsize-1_dz-0.50/peptide_T300.0cs1.00E-01pH07.00.dat'
pH='7'
./../plot_pmf-z_pH.py "$path" "$pH"
./../plot_pmfmin-confs_pH.py "$path"


exit

