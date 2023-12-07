#!/bin/python3

import random

# inputs:
sequences = ['CQSVTSTKC']

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
    #maximum_hydrophobicity = 4.5 * len(peptide)
    #minimum_hydrophobicity = -4.5 * len(peptide)
    peptide_hydrophobicity = sum(peptide_hydrophobicity_list)
    #peptide_relative_hydrophobicity = round(peptide_hydrophobicity / maximum_hydrophobicity, 2)
    peptide_relative_hydrophobicity = round(peptide_hydrophobicity / len(peptide), 2)
    return peptide_relative_hydrophobicity


for sequence in sequences:
    peptide_relative_hydrophobicity = calculate_peptide_hydrophobicity(sequence)
    print(f'peptide = {sequence}\nlength = {len(sequence)}\nhydrophobicity/maximum_hydrophobicity = {peptide_relative_hydrophobicity}\nhydrophobic = 4.5\nhydrophilic = -4.5')



exit()
