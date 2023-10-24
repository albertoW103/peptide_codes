#!/bin/python3
import random

# Description of the script's purpose
#########################################################################
# this script creates 10 random secuences of peptides using             #
# and compate with an SBP                                               #
# 1. create the SBP sequence                                            #
# 2. get SBP aminoacid into a list and shuffle into different sequences #
# 3. save the sequences into a file                                     #
#########################################################################

###################################################################
# inputs:
# list of SPBs:
# arbitrary list of SBP:
#sbp_list = ['RGRRRRLSCRLL', 'SSKKSGSYSGSKGSKRRIL', 'RKKRKKRKKRKK', 'KPTHHHHHHDG', 'SSRSSSHRRHDHHDHRRGS', 'DSARGFKKPGKR', 'MSPHPHPRHHHT']
sbp_list = ['KLPGWSG', 'AFILPTG', 'LDHSLHS', 'DSARGFKKPGKR']
#sbp_list = ['RGRRRRLSCRLL']
nseq = 10 # number of sequences

############################################################
# define the seed for reproducibility:
seed = 0
random.seed(seed)

label = 0
# main loop to create a file with an SBP and 10 sequence of ramdom aminoacids
# with the same length of the SPB.
for sequence in sbp_list:
    peptide_list = []   # empty list to append peptide sequences

    # first peptide
    peptide_list.append(sequence)                           # apped peptide one in the list

    # loop to create a list of 10 ramdom peptides:
    for _ in range(nseq):
        # convert the sequence to shuffle into a list of characters:
        sequence_list = list(sequence)

        # shuffle the sequence:
        random.shuffle(sequence_list)

        # undo the sequence list:
        shuffle_sequence = ''.join(sequence_list)

        # append peptide into a list:
        peptide_list.append(shuffle_sequence)

    # converting the list into one string:
    list_to_bash = ' '.join(peptide_list)

    # save the string into a file
    label += 1 # create labels
    with open('{}.txt'.format('familypep-' + str(label)), 'w') as file:
        file.write(list_to_bash)

exit()
