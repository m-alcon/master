#!/bin/bash

input_folder=./out
output_file=./err/checks.out

mkdir -p output
rm $output_file

total_files=`ls -1 $input_folder | wc -l`

i=`(expr 0)`
for input in $input_folder/*.out; do
	file_name=`basename $input`
	file_name=${file_name%.*}
	echo "$file_name" >> $output_file
	./checker < $input &>> $output_file
	let i+=1
	echo -ne "$i/$total_files"\\r
done
