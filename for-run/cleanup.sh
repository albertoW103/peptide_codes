
read -r -p "Are you sure you want to remove everything? [y/N] " response


if [[ "$response" =~ ^(yes|y)$ ]];then


rm -f *.dat
rm -f *.bad


declare -a allvars=("guess*.in"#
"output*txt" "err*.txt")

for var in ${allvars[@]};do

if [[ -a $var ]];then
    rm -i $var
fi

done

fi
