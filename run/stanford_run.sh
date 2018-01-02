#!/bin/bash
 
if [ "`basename $(pwd)`" == "parsers" ]; 
	then    echo "Dir correct for parsing";
	else	echo "Dir incorrect for parsing";exit; 
fi

cp_loc="$(pwd)/src-parsers/stanford-parser-full-2017-06-09"
input_file_loc="$(pwd)/input/selected_sent_raw.txt"
output_file_loc_pcfg="$(pwd)/output/pcfg_stanford_parse_output.txt"
output_file_loc_nn="$(pwd)/output/nn_stanford_parse_output.txt"

java -mx200m -cp "$cp_loc/*" edu.stanford.nlp.parser.lexparser.LexicalizedParser  -model edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz -outputFormat "typedDependencies" -outputFormatOptions includePunctuationDependencies $input_file_loc > $output_file_loc_pcfg

java -Xmx2g -cp "$cp_loc/*" edu.stanford.nlp.parser.nndep.DependencyParser -model edu/stanford/nlp/models/parser/nndep/english_UD.gz -outputFormatOptions includePunctuationDependencies -textFile $input_file_loc -outFile $output_file_loc_nn
