#!/bin/bash
 
if [ "`basename $(pwd)`" == "parsers" ]; 
	then    echo "Dir correct for parsing";
	else	echo "Dir incorrect for parsing";exit; 
fi

cp_loc="$(pwd)/src-parsers/stanford-parser-full-2017-06-09"
input_file_loc="$(pwd)/input/input_raw.txt"
output_file_loc_pcfg="$(pwd)/output/pcfg_stanford_parse_output.txt"
output_file_loc_nn="$(pwd)/output/nn_stanford_parse_output.txt"

$cp_loc/lexparser.sh $input_file_loc >> $output_file_loc_pcfg

java -Xmx2g -cp "$cp_loc/*" edu.stanford.nlp.parser.nndep.DependencyParser -model edu/stanford/nlp/models/parser/nndep/english_UD.gz -textFile $input_file_loc -outFile $output_file_loc_nn
