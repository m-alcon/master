#!/bin/bash

input_folder=./instances/
output_folder=solutions
error_folder=output

mkdir -p $output_folder
mkdir -p $error_folder

total_files=`ls -1 $input_folder | wc -l`

i=`(expr 0)`
for input in $input_folder*.inp; do
	file_name=`basename $input`
	file_name=${file_name%.*}
	./nor_circuit < $input 1> ./$output_folder/$file_name.out 2> ./$error_folder/$file_name.err
	let i+=1
	echo -ne "$i/$total_files"\\r
	#bc <<< "$i/$total_files"
done
