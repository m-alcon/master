#!/bin/bash

input_folder=./instances/
sol_folder=out
output_folder=err

mkdir -p $sol_folder
mkdir -p $output_folder

rm $sol_folder/*
rm $output_folder/*

SECONDS=0

total_files=`ls -1 $input_folder | wc -l`

i=`(expr 0)`
for input in $input_folder*.inp; do
	file_name=`basename $input`
	file_name=${file_name%.*}
	./nor_circuit < $input 1> ./$sol_folder/$file_name.out 2> ./$output_folder/$file_name.err
	let i+=1
	echo -ne "$i/$total_files: last solution at ${SECONDS}s."\\r
done
echo "${SECONDS}s to compute all instances."
