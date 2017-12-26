#!/bin/bash

if [ "`basename $(pwd)`" == "parsers" ]; 
	then    echo "Dir correct for parsing";
	else	echo "Dir incorrect for parsing";exit; 
fi

bin_loc="$(pwd)/src-parsers/candc-1.00/bin/"
model_loc="$(pwd)/src-parsers/candc-1.00/models/"
input_file_loc="$(pwd)/input_raw.txt"
output_file_loc="$(pwd)/ccg_candc_parse_output.txt"

$bin_loc/candc --models $model_loc --input $input_file_loc --output $output_file_loc
