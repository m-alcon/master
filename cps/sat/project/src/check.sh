#!/bin/bash

input_folder=../out
output_file=../checkers.out

rm -f $output_file

total_files=`ls -1 $input_folder | wc -l`

i=`expr 0`
errors=`expr 0`
for input in $input_folder/*.out; do
	file_name=`basename $input`
	file_name=${file_name%.*}
	echo "$file_name" >> $output_file
	./checker < $input &>> $output_file
	last_line=`tac $output_file | egrep -m 1 .`
	if [[ $last_line != *"OK!"* ]]; then
		let errors+=1
	fi
	let i+=1
	echo -ne "$i/$total_files checked solutions."\\r
done
echo "$errors errors while checking the $total_files solutions."
