
declare -a allvars=("fO"
		    #"fHis"
    "Qsurf"
    "pH0" "DV"
    "gamma_peptide" "Q_peptide"
)




#######################################################



pH_pat="pH="
pH_col=2


for var in ${allvars[@]};do


pat=$var
    

if [[ $var == "" ]];then
    exit



elif [[ $var == "pH0" ]];then
    pat="pH_r0="
    cols=2

    
elif [[ $var == "DV" ]];then
    pat="DV="
    cols=2

    
elif [[ $var == "gamma_peptide" ]];then
    pat="peptide_gamma="
    cols=2

elif [[ $var == "Q_peptide" ]];then
    pat="peptide_<Q>_h/p/b="
    cols="2 3 4"


elif [[ $var == "Qsurf" ]];then
    pat="surface_Qs_tot="
    cols=2


elif [[ $var == "fO" ]];then
    pat="sOH(1)-="
    cols="2 3"


fi



outfiname=$var"-pH.dat"

for i in freen_T*cs*pH*.dat
do


vals=""
val=""

for col in $cols;do

val=`grep $pat $i | gawk -v col=$col '{print $col}'`
#val=`gawk -v pat=$pat -v col=$col '$0 ~ pat {print $col}' $i`

vals=$vals" "$val

done

ph=`gawk -v pat=$pH_pat -v col=$pH_col ' $1 == pat {print $col}' $i`

echo  $ph $vals

done > $outfiname

echo " " $outfiname "created"


done

