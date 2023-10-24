#!/bin/python3

import random

#########################################################################
# this script creates x random sequences of an SBP

#########################################################################
# inputs:
sequences = ['KLPGWSG', 'AFILPTG', 'LDHSLHS', 'YITPYAHLRGGN', 'KSLSRHDHIHHH', 'MHRSDLMSAAVR', 'MSPHPHPRHHHT', 'RGRRRRLSCRLL']
nseq = 10 # number of sequences

#########################################################################
# define a seed for reproducibility:
seed = 0
random.seed(seed)

label = 0

# main loop to create a file with an SBP and 10 sequence of ramdom aminoacids:
for sequence in sequences:

    # empty list to append peptide sequences:
    peptides_list = []

    # first peptide:
    peptides_list.append(sequence)

    # loop to create a list of 10 ramdom peptides:
    for _ in range(nseq):

        # convert the sequence into a list of characters:
        peptide = list(sequence)

        # shuffle the sequence:
        random.shuffle(peptide)

        # undo the sequence list:
        new_peptide = ''.join(peptide)

        # append peptide into a list:
        peptides_list.append(new_peptide)

    # converting the list into one string:
    peptides_string = ' '.join(peptides_list)

    # save the string into a file:
    label += 1
    with open('{}.txt'.format('familypep-' + str(label)), 'w') as file:
        file.write(peptides_string)

exit()
