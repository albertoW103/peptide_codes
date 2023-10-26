import matplotlib.ticker as mtick
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os
import matplotlib.font_manager as fm

# my functions:
# style flag indicates function to style on plots
# for estyle use:
# plt.style.use("seaborn-bright")

# call my functions for style:
# style_ticks_plot(ax, 1)
# set_plotstyle(plt, ax)

#####################################################################
# import this to run my_funtions.py:
# import sys
# sys.path.append('/home/wilson/Research/styles_and_functions/')
# from my_functions import *
#####################################################################


my_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta', 'lime', 'teal', 'navy', 'maroon', 'aqua', 'silver', 'gold', 'indigo', 'coral', 'orchid', 'salmon', 'seagreen', 'sienna', 'tan', 'tomato', 'turquoise', 'violet', 'wheat', 'yellow']




def style_ticks_plot(ax, x_mayor_tick):
    '''
    Description of this function:

    ax: subplot ax
    x_mayor_tick: add mayor ticks every set value on x
    #y_mayor_tick: add mayor ticks every set value on y
    
    The functions provides 6 mayor ticks values on y axe with 1 minor tick between 2 mayor ticks 
    '''
    
    # set tick values on x: mayor and minor
    ax.xaxis.set_major_locator(mtick.MultipleLocator(x_mayor_tick)) # mayor tick on x
    x_minor_tick = x_mayor_tick*0.5                                 # set x_minor_tick value
    ax.xaxis.set_minor_locator(mtick.MultipleLocator(x_minor_tick)) # minor tick on x

    # set tick values on y: mayor and minor
    #ax.yaxis.set_major_locator(mtick.MultipleLocator(y_mayor_tick)) # mayor tick on y
    #y_minor_tick = y_mayor_tick*0.5                                 # set y_minor_tick value
    #ax.yaxis.set_minor_locator(mtick.MultipleLocator(y_minor_tick)) # minor tick on y

    # set amount of ticks on y axe:
    n_mayor_yticks=6
    n_minor_yticks=2
    ax.yaxis.set_major_locator(mtick.MaxNLocator(n_mayor_yticks))
    ax.yaxis.set_minor_locator(AutoMinorLocator(n_minor_yticks))
    
    # set specific format on x and y axes:
    #ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.1e"))

def save_file(fig, output_file):
    '''
    Description of this function:

    fig: this must be add on figure
    output_file: name of the output file
    
    The function save a figure with personal format and trim it
    '''
    fig.savefig(output_file, transparent=True, format="png", dpi=200) # save figure
    os.system('convert -trim {} {}'.format(output_file, output_file)) # trim


def set_plotstyle(plt, ax):
    '''
    Description of this function:
    plt: it must be added
    ax: for subplot ax
    This script set a personal style for plots on mathplotlib:
    - font: serif
    - fontsize: 15 for title, xlabel, ylabel
    - aspect ration 1
    - fontsize for legend: 10
    - layout plot
    '''
    # search font 'serif'
    serif_fonts = [font for font in fm.fontManager.ttflist if 'serif' in font.name.lower()]
    
    if serif_fonts:
        # get first font serif
        serif_font = serif_fonts[0].name
        
        # set fontsize on axes legends
        fontsize=12 # fontsize
        ax.set_title(ax.get_title(), fontname=serif_font, fontsize=fontsize)
        ax.set_xlabel(ax.get_xlabel(), fontname=serif_font, fontsize=fontsize)
        ax.set_ylabel(ax.get_ylabel(), fontname=serif_font, fontsize=fontsize)
            
        # set aspect ratio 1
        ax.set_box_aspect(1)
        
        # Set fontsize for tick labels on both axes
        fonstsize_ticks_labels=10
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(serif_font)
            label.set_fontsize(fonstsize_ticks_labels)  # You can adjust this fontsize as needed

        # set other elements on legends
        fontsize_legend=10
        legend = ax.legend(loc='best', fontsize=fontsize_legend, frameon=False)
        for text in legend.get_texts():
            text.set_fontname(serif_font)

        # layout graps on figure
        #plt.tight_layout()


def set_plotstyle_without_legend(plt, ax):
    '''
    Description of this function:
    plt: it must be added
    ax: for subplot ax
    This script set a personal style for plots on mathplotlib:
    - font: serif
    - fontsize: 15 for title, xlabel, ylabel
    - aspect ration 1
    - fontsize for legend: 10
    - layout plot
    '''
    # search font 'serif'
    serif_fonts = [font for font in fm.fontManager.ttflist if 'serif' in font.name.lower()]
    
    if serif_fonts:
        # get first font serif
        serif_font = serif_fonts[0].name
        
        # set font for elements on figure
        fontsize=15 # fontsize
        ax.set_title(ax.get_title(), fontname=serif_font, fontsize=fontsize)
        ax.set_xlabel(ax.get_xlabel(), fontname=serif_font, fontsize=fontsize)
        ax.set_ylabel(ax.get_ylabel(), fontname=serif_font, fontsize=fontsize)

        # set aspect ratio 1
        ax.set_box_aspect(1)
        
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(serif_font)

        # set other elements on legends
        #fontsize_legend=10
        #legend = ax.legend(loc='best', fontsize=fontsize_legend, frameon=False)
        #for text in legend.get_texts():
        #    text.set_fontname(serif_font)

        # layout graps on figure
        #plt.tight_layout()


def molec2mg_(mw):
    mw = mw   # molecular weitght in g/mol
    avogadro = 6.023*(10**23) # avogadro number in molecules/mol
    m_to_nm = 1*(10**9) # nm/m
    g_to_mg = 1000      # mg/g
    factor = (g_to_mg*mw*m_to_nm)/(avogadro)
    return factor


def gamma_molec_to_mg_m2(gamma1, mw):
    '''
    Parameters:
        gamma1: gamma in molecules/nm^2
        mw: molecular weight in g/mol
    Return:
        gamma2: gamma in mg/m^2
    '''
    avogadro = 6.023*(10**23) # avogadro number in molecules by mol
    m2nm = 1/(1*(10**9)**2)   # conversion factor from m^2 to nm^2
    g2mg = 1/1000             # conversion factor from g to mg
    gamma2 = (gamma1 * mw)/(avogadro * m2nm * g2mg)
    return gamma2


def convert_1dx_xxx(text):
    """
    Converts, for example 1d6 string into 1*10**-6 M float

    Args:
        text (str): 1d6 string 

    Returns:
        float: 1*10**-6

    Raises:
        ValueError: If the input string does not follow the '1dx' format or if 'x' is not an integer.
    """
    base = float(text.split('d')[0])    # base
    exponent = int(text.split('d')[1])  # exponent
    
    cprot = base * 10 **(-exponent)     # float data
    
    return cprot


def mw_from_sequence(sequence):
    """
    Calculate the molecular weight (MW) of a protein or peptide sequence.

    Parameters:
        sequence (str): A string representing the sequence of amino acids.

    Returns:
        float: The calculated molecular weight in g/mol.
    """
    # Defines a dictionary that maps the 20 common amino acids to their atomic masses
    atomic_weights = {
        'A': 89.1, 'R': 174.2, 'N': 132.1, 'D': 133.1, 'C': 121.2,
        'Q': 146.2, 'E': 147.1, 'G': 75.1, 'H': 155.2, 'I': 131.2,
        'L': 131.2, 'K': 146.2, 'M': 149.2, 'F': 165.2, 'P': 115.1,
        'S': 105.1, 'T': 119.1, 'W': 204.2, 'Y': 181.2, 'V': 117.1
    }
    # from https://www.thermofisher.com/

    # Calculate the molecular weight by summing the atomic weights of the amino acids
    mw = sum(atomic_weights.get(aminoacid, 0) for aminoacid in sequence)
    return mw


def add_text(ax, text, location, offset=(0, 0), fontsize=12):
    '''
    Add text to the specified location on the given axes.

    Parameters:
        ax (matplotlib.axes.Axes): The axes object to which text will be added.
        text (str): The text content to be added.
        location (str): The location where the text should be placed ('upper left', 'upper right', 'lower left', 'lower right', 'center', 'right', 'left', 'upper', 'lower', or 'custom').
        offset (tuple): Offset for custom positioning (default is (0, 0)).
        fontsize (int): Font size of the text (default is 12).
    '''
    if location == 'upper left':
        ax.text(0.05 + offset[0], 0.95 + offset[1], text, transform=ax.transAxes, fontsize=fontsize)
    elif location == 'upper right':
        ax.text(0.95 + offset[0], 0.95 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, horizontalalignment='right')
    elif location == 'lower left':
        ax.text(0.05 + offset[0], 0.05 + offset[1], text, transform=ax.transAxes, fontsize=fontsize)
    elif location == 'lower right':
        ax.text(0.95 + offset[0], 0.05 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, horizontalalignment='right')
    elif location == 'center':
        ax.text(0.5 + offset[0], 0.5 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, horizontalalignment='center', verticalalignment='center')
    elif location == 'right':
        ax.text(0.95 + offset[0], 0.5 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, horizontalalignment='right', verticalalignment='center')
    elif location == 'left':
        ax.text(0.05 + offset[0], 0.5 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, verticalalignment='center')
    elif location == 'upper':
        ax.text(0.5 + offset[0], 0.95 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, horizontalalignment='center')
    elif location == 'lower':
        ax.text(0.5 + offset[0], 0.05 + offset[1], text, transform=ax.transAxes, fontsize=fontsize, horizontalalignment='center')
    elif location == 'custom':
        ax.text(offset[0], offset[1], text, transform=ax.transAxes, fontsize=fontsize)
    else:
        raise ValueError("Invalid location. Supported locations: 'upper left', 'upper right', 'lower left', 'lower right', 'center', 'right', 'left', 'upper', 'lower', or 'custom'.")




def get_xyz1(filename, skiprows=2):
    block = []
    # open a file:
    with open(filename, "r") as file:
        # save all lines:
        lines = file.readlines()
        # skip first two lines:
        lines = lines[skiprows:]

        # create a list if lists:
        for line in lines:
            line_xyz = line.strip().split("\t")
            line_xyz[1] = float(line_xyz[1])
            line_xyz[2] = float(line_xyz[2])
            line_xyz[3] = float(line_xyz[3])
            block.append(line_xyz)
    return block

def get_xyz2(filename):
    blocks = []
    current_block = []
    with open(filename, 'r') as file:
        ### skip rows with rare numbers:
        lines = []
        for line in file:
            value_to_test = len(line.split())
            if value_to_test == 1:  
                continue
            else:
                lines.append(line)

        ### save blocks of data by spacing
        for line in lines:
            value_to_test = line.strip()
            if value_to_test == '':   # if empty line is found, then block is save into block list 
                if current_block: # save non empty block
                    blocks.append(current_block) # append block into a block list
                current_block = []               # inicialize a new block
            else:   # append lines into current block:
                line_xyz = line.strip().split()
                line_xyz[1] = float(line_xyz[1])
                line_xyz[2] = float(line_xyz[2])
                line_xyz[3] = float(line_xyz[3]) 
                current_block.append(line_xyz)
        return blocks

def a_to_nm(block):
    for element in block:
        element[1] = round(element[1]/10,4)
        element[2] = round(element[2]/10,4)
        element[3] = round(element[3]/10,4)
    return block
