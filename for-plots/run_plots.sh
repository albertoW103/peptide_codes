#!/bin/bash

#: <<'END'
# plot gamma vs cprot for one peptide at multiple pHs:
# one peptide as an example:
path='Puddu2012_seq2-AFILPTG_cprot-*_csalt-0.01_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
pH='4 5 7'
./../plot_gamma-cprot.py "$path" "$pH" "mg"


# plot gamma vs cprot at one pH for multiples peptides:
path1='Puddu2012_seq1-KLPGWSG_cprot-*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
path2='Puddu2012_seq2-AFILPTG_cprot-*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
path3='Puddu2012_seq3-LDHSLHS_cprot-*_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
pH='7'
./../plot_gamma-pH_peps.py "$path1" "$path2" "$path3" "mg"
./../plot_gamma-cprot_peps.py "$path1" "$path2" "$path3" "$pH" "mg"


#END
# plot gamma vs pH for one peptide at multiple salt concentration:
path1='Puddu2012_seq1-KLPGWSG_cprot-1d6_csalt-0.1_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
path2='Puddu2012_seq1-KLPGWSG_cprot-1d6_csalt-0.01_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
path3='Puddu2012_seq1-KLPGWSG_cprot-1d6_csalt-0.001_confs-1000_rsize-1_dz-0.50/gamma_peptide-pH.dat'
./../plot_gamma-csalt.py "$path1" "$path2" "$path3" "mg"


# plot gamma vs rsize:
path1='Puddu2012_seq1-KLPGWSG_cprot-1d6_csalt-0.1_confs-1000_rsize-*_dz-0.50/peptide_T300.0cs1.00E-01pH07.00.dat'
pH='7'
./../plot_pmf-z-rsize.py "$path1" "$pH"
./../plot_pmfmin-rsize.py "$path1" "$pH"

exit
