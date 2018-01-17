#!/bin/bash

if [ "`basename $(pwd)`" == "parsers" ]; 
	then    echo "Dir correct for parsing";
	else	echo "Dir incorrect for parsing";exit; 
fi

bin_loc="$(pwd)/src-parsers/candc-1.00/bin"
model_loc="$(pwd)/src-parsers/candc-1.00/models/"
input_file_loc="$(pwd)/input/aux-sent.txt"
output_file_loc="$(pwd)/output-2/ccg_candc_parse_output.txt"
log_file_loc="$(pwd)/output-2/ccg_candc_parse_stats.txt"

$bin_loc/candc --candc-trans_brackets=true --candc-printer=grs --candc-decoder=derivs --models $model_loc --input $input_file_loc --output $output_file_loc --log $log_file_loc

