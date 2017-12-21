#!/bin/bash
 
cp_loc="~/stanford-tools/stanford-parser-full-2017-06-09"
input_file_loc="./input_raw.txt"
output_file_loc_pcfg="./pcfg_stanford_parse_output.txt"
output_file_loc_nn="./nn_stanford_parse_output.txt"

/Users/tom/stanford-tools/stanford-parser-full-2017-06-09/lexparser.sh $input_file_loc >> $output_file_loc_pcfg

java -Xmx2g -cp $cp_loc edu.stanford.nlp.parser.nndep.DependencyParser -model edu/stanford/nlp/models/parser/nndep/english_UD.gz -textFile $input_file_loc -outFile $output_file_loc_nn
