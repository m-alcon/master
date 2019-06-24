#!/bin/bash

input_folder=../instances/
output_folder=../out
debug_folder=../err

mkdir -p $output_folder
mkdir -p $debug_folder

rm $output_folder/*
rm $debug_folder/*

n_timeouts=`expr 0`

total_files=`ls -1 $input_folder | wc -l`

i=`expr 0`
SECONDS=0
for input in $input_folder*.inp; do
	file_name=`basename $input`
	file_name=${file_name%.*}
	is_timeout=0
	timeout 1m python3 nor_circuit.py < $input 1> $output_folder/${file_name}.out 2> $debug_folder/${file_name}.err || is_timeout=1
	if [ $is_timeout -eq 1 ]; then
		rm $output_folder/${file_name}.out
		let n_timeouts+=1
	fi
	let i+=1
	echo -ne "$i/$total_files instances | $n_timeouts timeouts | Last computed ${SECONDS}s"\\r
done
echo ""
echo "${SECONDS}s to compute all instances | $n_timeouts instances failed"
