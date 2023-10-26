#!/bin/python3
import random

#####################################################################
# this scripts create 10 random secuences of peptides               #
# and compare to an SBP                                             #
# 1. create the SBP sequence                                        #
# 2. calculate the relative hidrophobicity of the SBP               #
# 3. create random peptide which hidrophobicity is equal to the SBP #
# 4. save into a file                                               #
#####################################################################

#####################################################################
# inputs:
sequences = ['KLPGWSG', 'AFILPTG', 'LDHSLHS', 'YITPYAHLRGGN', 'KSLSRHDHIHHH', 'MHRSDLMSAAVR', 'MSPHPHPRHHHT', 'RGRRRRLSCRLL']
nseq = 10

#####################################################################
# list of amino acids:
aminoacids = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I',\
               'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']

# Define a dictionary mapping each aminoacid to its hydrophobicity value
# Author(s): Kyte J., Doolittle R.F.
# Reference: J. Mol. Biol. 157:105-132(1982).
hydrophobicity_values = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
    'M': 1.9, 'A': 1.8, 'G': -0.4,'T': -0.7, 'W': -0.9,
    'S': -0.8, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'E': -3.5,
    'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5
}

# more_polar = -4.5
# less_polar = 4.5

#####################################################################
# define functions:

# Calculate the hydrophobicity of the peptide:
def calculate_peptide_hydrophobicity(peptide):
    '''
    Calculate the hydrophobicity of a peptide.

    This function calculates the relative hydrophobicity of a peptide
    based on the hydrophobicity values of its constituent amino acids.

    :param peptide: A string representing the peptide sequence (e.g. KLPGWSG).
    :return: The relative hydrophobicity of the peptide as a float.
    '''
    
    peptide_hydrophobicity_list = [hydrophobicity_values[aminoacid] for aminoacid in peptide]
    maximum_hidrophobicity = -4.5 * len(peptide)
    peptide_hydrophobicity = sum(peptide_hydrophobicity_list)
    peptide_relative_hydrophobicity = round(peptide_hydrophobicity / maximum_hidrophobicity, 2)
    return peptide_relative_hydrophobicity

#####################################################################
# define a seed for reproducibility:
seed = 0
random.seed(seed)

# create peptides:
label = 0

# this main loop create a file with an SBP and 10 sequence of ramdom aminoacids with the same length of the SPB.
# additionaly, only aminoacids with a certain hydrophobicity value are choosen: 
for sequence in sequences:

    # create an empty list of peptides:
    peptides_list = []

    # append first sequence:
    peptides_list.append(sequence)

    # calculate hydrophobicity:
    peptide_hydrophobicity_sbp = calculate_peptide_hydrophobicity(sequence)

    # loop to create a list of 10 ramdom peptides:
    counter = 0 # set counter
    while counter < nseq:
        peptide = ''
        for i in range(len(sequence)):
            pep = random.choice(aminoacids)
            peptide = peptide + pep

        # calculate hydrophobicity:
        peptide_hydrophobicity = calculate_peptide_hydrophobicity(peptide)

        # append peptide is the condition is fulfilled:
        if peptide_hydrophobicity >= abs(peptide_hydrophobicity_sbp):
            peptides_list.append(peptide)
            counter += 1

    # save  peptide sequence into a file:
    # converting the list into one string:
    peptides_string = ' '.join(peptides_list)

    # save the string into a file:
    label += 1
    with open(f'familypep-{str(label)}.txt', 'w') as file:
        file.write(peptides_string)

exit()
