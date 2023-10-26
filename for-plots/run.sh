#!/bin/bash

####################################
# this scipt create directories    #
# where to run simulation          #
####################################

####################################
# inputs:

csalt_list='0.1' # in M
confs_list='1'
#cprot_list='1d7 1d6 1d5 1d4'   # 1d6 mean 1d-6 in the param.in file
cprot_list='1d3 1d2 1d1 1d0'   # 1d6 mean 1d-6 in the param.in file
dist='0.4'
np='8'
ebs='no'
guessx='yes'  # use guessx.in
#path='~/wilson/Research/codes_gabi/mt_1d/code/mt1d.x' # on cordoba
path='../../../../codes_gabi/mt_1d/code/mt1d.x' # on cordoba
#path='../../../mt_1d/code/mt1d.x'               # on indiana and zacate
dz_list='0.50'
#symetries='planar sphere'
symetries='planar'
rplanar='1'
#rsize_list='1 10 20 30 40 50 100 500 1000' # in nm, 1: plane; > 1 sphere
#rsize_list='1 10 20 30 40 50 100 500 1000' # in nm, 1: plane; > 1 sphere
group_position='0.1'                         # define the position of the silanol group, it must fall on the first layer!!!
nlayes='100'                                 # n amount of layes
file_list=$(ls -1v inputs/*.txt)             # select all paperpep-*.txt








####################################
# Initialize the basename_list variable
basename_list=""
# Loop through the file_list and extract basenames
for file in $file_list; do
    #echo "File: $file"
    basename_file=$(basename "$file" .txt) # Select basenames, and use double quotes around $file to handle filenames with spaces
    #echo "Basename: $basename_file"
    basename_list="$basename_list $basename_file" # Append the basename to the list
done

####################################
# Create a mapping dictionary for one-letter to three-letter code conversion
declare -A aa_mapping=(
  ["A"]="Ala"
  ["R"]="Arg"
  ["N"]="Asn"
  ["D"]="Asp"
  ["C"]="Cys"
  ["Q"]="Gln"
  ["E"]="Glu"
  ["G"]="Gly"
  ["H"]="His"
  ["I"]="Ile"
  ["L"]="Leu"
  ["K"]="Lys"
  ["M"]="Met"
  ["F"]="Phe"
  ["P"]="Pro"
  ["S"]="Ser"
  ["T"]="Thr"
  ["W"]="Trp"
  ["Y"]="Tyr"
  ["V"]="Val"
)

##############################################################
# run a simulation without protein to create a guessx.in file:
##############################################################
if [ $guessx = 'yes' ]; then            # for planar we use 1
    for csalt in $csalt_list; do
        for symetry in $symetries; do
            if [ $symetry = 'planar' ]; then
                rsize_list_new=$rplanar
            elif [ $symetry = 'sphere' ]; then
                rsize_list_new=$rsize_list
            else
               continue
            fi
            for rsize in $rsize_list_new; do
                for dz in $dz_list; do
                    # create directory and copy files:
	            mkdir no-protein_csalt-${csalt}_symetry-${symetry}_rsize-${rsize}_dz-${dz}/
	            cd no-protein_csalt-${csalt}_symetry-${symetry}_rsize-${rsize}_dz-${dz}/

	            # copy files from inputs:
                    # copy ebs file:
                    if [ $ebs = 'yes' ]; then
                        cp ../inputs/CG_model-ebs_XXX.mol .     # copy file
                        mv CG_model-ebs_XXX.mol CG_model.mol    # change name
                    else
                        cp ../inputs/CG_model_XXX.mol .         # copy file
                        mv CG_model_XXX.mol CG_model.mol        # change name
                    fi

	            cp ../inputs/surface_XXX.mol .              # copy files
	            cp ../inputs/param_XXX.in .                 # copy files

	            # change name of files:
	            mv param_XXX.in param.in                    # change name
                    mv surface_XXX.mol surface.mol              # change name

	            # sed on param.in:
	            sed -i "s/POS1/$csalt/g" param.in    # sed salt concentration
	            sed -i "s/POS2/0/g" param.in         # sed number of adsorbates
	            sed -i "s/POS4/0/g" param.in         # sed guessx=0,2,3
	            sed -i "s/POS6/$dz/g" param.in       # sed dz, usually 100

                    # plane and surface:
                    if [ $symetry = 'planar' ]; then            # for planar we use 1
                        # on param.in:
                        sed -i "s/POS5/planar/g" param.in
                        sed -i "s/POS7/$rsize/g" param.in      # seed r size
                        rmax=$(echo "$rsize + $nlayes" | bc)   #
                        sed -i "s/POS8/$rmax/g" param.in       #
                        # on surface.mol:
                        surface=$(echo "$rsize + $group_position" | bc)
                        sed -i "s/POS1/$surface/g" surface.mol
                        
                    elif [ $symetry = 'sphere' ]; then
                        # on param.in:
                        sed -i "s/POS5/sphere/g" param.in
                        sed -i "s/POS7/$rsize/g" param.in      # seed r size
                        rmax=$(echo "$rsize + $nlayes" | bc)   #
                        sed -i "s/POS8/$rmax/g" param.in       #
                        
                        # on surface.mol:
                        surface=$(echo "$rsize + $group_position" | bc)
                        sed -i "s/POS1/$surface/g" surface.mol
                        
                    else
                        continue
                    fi

	            # run simulation:
	            sleep 2
	            mpirun -np $np $path | tee output
	            sleep 2

	            # go back:
                    cd ../
                    
                done
            done
        done
    done
else
    # No hacer nada cuando no se cumple la condición
    # Deja este bloque else vacío o usa 'true' como marcador
    # true
    echo 'simulations without protein are not run'
fi

#exit
for family_seq in $basename_list; do                     # for every main file that contains many differenet SBP sequences
    peptide_list=$(more inputs/$family_seq.txt)          # create a list with peptide sequences
    for cprot in $cprot_list; do                         # for every protein concentration
        for csalt in $csalt_list; do                     # for every salt concentration
            for symetry in $symetries; do
                if [ $symetry = 'planar' ]; then
                    rsize_list_new=$rplanar
                elif [ $symetry = 'sphere' ]; then
                    rsize_list_new=$rsize_list
                else
                    continue
                fi
                for rsize in $rsize_list_new; do
                    for dz in $dz_list; do
                        for confs in $confs_list; do             # for every conformation
                            label=1                              # create a label
                            for sequence in $peptide_list; do    # for every peptide sequence
                                label=$(printf "%02d" $label)
	                        # create directory and copy files:
	                        mkdir ${family_seq}_seq${label}-${sequence}_cprot-${cprot}_csalt-${csalt}_confs-${confs}_symetry-${symetry}_rsize-${rsize}_dz-${dz}/    # build a directory
                                cd ${family_seq}_seq${label}-${sequence}_cprot-${cprot}_csalt-${csalt}_confs-${confs}_symetry-${symetry}_rsize-${rsize}_dz-${dz}/       # go to the directory

	                        # copy files from inputs:
                                cp ../inputs/adsorbate_XXX.mol .     # copy file
                                cp ../inputs/surface_XXX.mol .       # copy file

                                # copy ebs file:
                                if [ $ebs = 'yes' ];then
                                    cp ../inputs/CG_model-ebs_XXX.mol .     # copy file
                                    mv CG_model-ebs_XXX.mol CG_model.mol    # change name
                                else
                                    cp ../inputs/CG_model_XXX.mol .         # copy file
                                    mv CG_model_XXX.mol CG_model.mol        # change name
                                fi

                                cp ../inputs/*.sh .              # copy file
                                cp ../inputs/*.in .              # copy file

                                # get the basename of the xs file at the highest pH:
                                highest_pH_xs_file=$(ls ../no-protein_csalt-${csalt}_symetry-${symetry}_rsize-${rsize}_dz-${dz}/xs* | awk -F'pH' '{print $2, $0}' | sort -n | tail -n 1 | awk '{print $2}' | xargs -I {} basename {})
                                cp ../no-protein_csalt-${csalt}_symetry-${symetry}_rsize-${rsize}_dz-${dz}/$highest_pH_xs_file .   # copy xs file

		                # change name of files:
		                mv $highest_pH_xs_file guessx.in    # create a guessx.in file
                                mv adsorbate_XXX.mol adsorbate.mol  # change name
                                mv param_XXX.in param.in            # change name
                                mv surface_XXX.mol surface.mol      #

                                # plane and surface:
                                if [ $symetry = 'planar' ]; then
                                
                                    # on param.in:
                                    sed -i "s/POS5/planar/g" param.in
                                    sed -i "s/POS7/$rsize/g" param.in      # seed r size
                                    rmax=$(echo "$rsize + $nlayes" | bc)   #
                                    sed -i "s/POS8/$rmax/g" param.in       #
                                    
                                    # on surface.mol:
                                    surface=$(echo "$rsize + $group_position" | bc)
                                    sed -i "s/POS1/$surface/g" surface.mol
                                    
                                elif [ $symetry = 'sphere' ]; then
                                
                                    # on param.in:
                                    sed -i "s/POS5/sphere/g" param.in
                                    sed -i "s/POS7/$rsize/g" param.in      # seed r size
                                    rmax=$(echo "$rsize + $nlayes" | bc)   #
                                    sed -i "s/POS8/$rmax/g" param.in       #
                                    
                                    # on surface.mol:
                                    surface=$(echo "$rsize + $group_position" | bc)
                                    sed -i "s/POS1/$surface/g" surface.mol
                                    
                                else
                                    continue
                                fi

                                # Convert the peptide sequence to the desired formate
                                #####################################
	                        # split the peptide sequence into three parts
	                        first_aa=${sequence:0:1}     # first aminoacid, on-letter code
	                        middle_seq=${sequence:1:-1}  # middle aminoacid seq, one code
	                        last_aa=${sequence: -1}      # last aminoacid , one-letter code

	                        # add space to the middle_aa sequence
                                middle_seq=$(echo "$middle_seq" | sed 's/./& /g')

                                # Convert one-letter code to three-letter code
                                # first aminoacid
                                first_aa="${first_aa}_Nt"

                                # middle sequence
                                middle_seq_space=""
                                for aa in $middle_seq; do
                                    to_append=${aa_mapping[$aa]}
                                    middle_seq_space+=" $to_append"
                                done

                                # last aminoacid
                                last_aa="${last_aa}_Ct"

	                        # create a new variable to sed in the format we want in the code of gabi
	                        seq_to_sed="1 $first_aa\n"         # load first aa in the variable
	                            for aa in $middle_seq_space; do    # load middle sequence in the variable
    	    	                    seq_to_sed+="1 $aa\n"          # append
                                done
                                seq_to_sed+="1 $last_aa"           # load last aa in the variable

                                ######################################
	                        # count:
                                letter_count=$(echo "$sequence" | tr -cd [:alpha:]  | wc -m)

	                        # seds on adsorbate.mol:
	                        # Replace the placeholder with the converted sequence in the file:
                                awk -v var="$seq_to_sed" '{gsub("POS4", var)}1' adsorbate.mol > adsorbate_temp.mol
                                mv adsorbate_temp.mol adsorbate.mol
                                sed -i "s/POS1/$confs/g" adsorbate.mol             # sed
                                sed -i "s/POS2/$dist/g" adsorbate.mol              # sed
	                        sed -i "s/POS3/$letter_count/g" adsorbate.mol      # sed

	                        # sed on param.in:
	                        sed -i "s/POS1/$csalt/g" param.in       # sed
                                sed -i "s/POS2/1/g" param.in            # sed number of adsorbates
	                        cprot_XXX="${cprot/d/d-}"	        # add minus to protein concnetration label
	                        sed -i "s/POS3/$cprot_XXX/g" param.in   # sed protein concentration
                                sed -i "s/POS4/2/g" param.in            # sed guessx=0,2,3
                                sed -i "s/POS6/$dz/g" param.in          # sed dz

	                        # run simulation:
	                        sleep 2
	                        mpirun -np $np $path | tee output
	                        sleep 2

	                        # get results:
	                        bash get-v-pH.sh

                               cd ../
                               # Increment label
                               label=$((10#$label))
                               label=$((label + 1))
                               #label=$(printf "%02d" $label)
                            done
                        done
                    done
                done
            done
        done
    done
done
cd ../

exit
