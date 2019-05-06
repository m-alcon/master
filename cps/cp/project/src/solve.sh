#!/bin/bash

input_folder=../instances/
output_folder=../out
debug_folder=../err

mkdir -p $output_folder
mkdir -p $debug_folder

rm $output_folder/*
rm $debug_folder/*

n_threads=4
n_timeouts=`expr 0`
if [ -z $1 ]; then
	n_threads=$1
fi


total_files=`ls -1 $input_folder | wc -l`

i=`expr 0`
SECONDS=0
for input in $input_folder*.inp; do
	file_name=`basename $input`
	file_name=${file_name%.*}
	is_timeout=0
	timeout 1m ./nor_circuit $n_threads < $input 1> $output_folder/${file_name}.out 2> $debug_folder/${file_name}.err || is_timeout=1
	if [ $is_timeout -eq 1 ]; then
		rm $output_folder/${file_name}.out
		let n_timeouts+=1
	fi
	let i+=1
	echo -ne "Finished $i/$total_files instances | $n_timeouts instances failed | Last instance computed at ${SECONDS}s"\\r
done
echo "${SECONDS}s to compute all instances | $n_timeouts instances failed"
