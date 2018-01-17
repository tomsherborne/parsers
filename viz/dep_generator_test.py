# Documentation https://mirror.hmc.edu/ctan/graphics/pgf/contrib/tikz-dependency/tikz-dependency-doc.pdf
import string
import re 
import os
from collections import namedtuple

IndexedWord 	= namedtuple('IndexedWord','word index')
DependencyArc	= namedtuple('DependencyArc','start_word end_word label is_root')
ParseConfig 	= namedtuple('ParseConfig','dir output type')

doc_preamble = r'''
\documentclass{article}
\usepackage[margin=1cm]{geometry}
\usepackage{tikz-dependency}
\begin{document}
'''

doc_postamble=r'''
\end{document}
'''

fig_preamble=r'''
\begin{dependency}
'''

fig_postamble = r'''
\end{dependency}
'''

def _generate_arcs(elems,parse_type):
	'''
	Generate dependency arc from words and indices
	Check for the sentential semantic root for Stanford parsers
	Check for C&C parser and add a +1 offset as parse indexes from 0
	params:
	@elems: List of word parts
	@parse_type: parser
	ouput:
	@DependencyArc(): arc object
	'''	
	is_root = True if elems[0]=='root' else False
	offset  = 1 if parse_type=='candc' else 0

	startw 	= IndexedWord(elems[1],int(elems[2])+offset)
	endw 	= IndexedWord(elems[3],int(elems[4])+offset)

	return DependencyArc(startw,endw,elems[0],is_root)

def generate_dep_arcs_candc(input_string):
# 	'''
# 	Take list of grammatical relations and return
# 	1. list of DependencyArc objects
# 	2. list of IndexedWord objects
# 	'''

# 	words = set()
# 	dep_arcs = []

# 	for line in input_string.splitlines():
# 		arc_parts = []
# 		elems = list(filter(None, re.split(' ',line[1:len(line)-1],maxsplit=5)))

# 		# Handle special cases
# 		if elems[0]=='ncsubj':
# 			elems[0] = elems[0]+':'+elems[-1] if elems[-1]!='_' else elems[0]
# 			del elems[-1]
# 		elif elems[0]=='xcomp':
# 			if elems[1]!='_':
# 				parts = elems[1].rsplit('_',1)
# 				words.add(IndexedWord(parts[0],int(parts[1])+1))
# 				elems[0]='xcomp:{}'.format(parts[0])
# 			del elems[1]
# 		if elems[0]=='cmod':
# 			if elems[1]!='_':
# 				parts = elems[1].rsplit('_',1)
# 				words.add(IndexedWord(parts[0],int(parts[1])+1))
# 				elems[0]='cmod:{}'.format(parts[0])
# 				del[elems[1]]
# 		elif len(elems)==4:
# 			elems[0] = elems[0]+':'+elems[1] if elems[1]!='_' else elems[0]
# 			del elems[1]

# 		arc_parts.append(elems[0])

# 		for w in elems[1:]:
# 			parts = [part for part in w.rsplit('_',1) if part is not '']
# 			arc_parts+=parts

# 		new_arc = _generate_arcs(arc_parts,'candc')
# 		words.add(IndexedWord(arc_parts[1],int(arc_parts[2])+1))
# 		words.add(IndexedWord(arc_parts[3],int(arc_parts[4])+1))

# 		dep_arcs.append(new_arc)

# 	words_sorted = sorted(list(words), key=lambda x: x.index)
# 	return words_sorted,dep_arcs

# def generate_dep_arcs_stanford(input_string):
# 	'''
# 	Take list of grammatical relations and return parsed objects
# 	arc_parts is an intermediate object structured as [label,word1,index1,word2,index2]
# 	params:
# 	@input_string: list of dependencies
# 	output:
# 	@words_sorted: sorted list of IndexedWord objects
# 	@dep_arcs: list of DependencyArc objects
# 	'''

# 	# empty objects
# 	words = set()
# 	dep_arcs = []

# 	for line in input_string.splitlines():

# 		arc_parts = []

# 		# get part of dependency relation
# 		elems = list(filter(None, re.split('[\(\)]+',line,maxsplit=2)))

# 		# append label
# 		arc_parts.append(elems[0])

# 		# get words in this dependency relation
# 		arc_words = [w.strip() for w in filter(None, re.split(',',elems[1],maxsplit=1))]
# 		for w in arc_words:
# 			# get word and index for each arc constituent
# 			arc_parts += w.rsplit('-',1)
		
# 		# update arc list
# 		new_arc = _generate_arcs(arc_parts,'stanford')
# 		dep_arcs.append(new_arc)

# 		# update set of words
# 		words.add(new_arc.start_word)
# 		words.add(new_arc.end_word)

# 	# sort words in set of words
# 	words_sorted = sorted(list(words), key=lambda x: x.index)
# 	return words_sorted,dep_arcs


def arc_parse_stanford(input_string):
	'''
	Take list of grammatical relations and return parsed objects STANFORD
	arc_parts is an intermediate object structured as [label,word1,index1,word2,index2]
	params:
	@input_string: list of dependencies
	output:
	@words:    list of IndexedWord objects
	@dep_arcs: list of DependencyArc objects
	'''

	# empty objects
	words = set()
	dep_arcs = []

	for line in input_string.splitlines():

		arc_parts = []

		# get part of dependency relation
		elems = list(filter(None, re.split('[\(\)]+',line,maxsplit=2)))

		# append label
		arc_parts.append(elems[0])

		# get words in this dependency relation
		arc_words = [w.strip() for w in filter(None, re.split(',',elems[1],maxsplit=1))]
		for w in arc_words:
			# get word and index for each arc constituent
			arc_parts += w.rsplit('-',1)
		
		# update arc list
		new_arc = _generate_arcs(arc_parts,'stanford')
		dep_arcs.append(new_arc)

		# update set of words
		words.add(new_arc.start_word)
		words.add(new_arc.end_word)
	return words,dep_arcs

def arc_parse_candc(input_string):
	'''
	Take list of grammatical relations and return parsed objects CANDC
	arc_parts is an intermediate object structured as [label,word1,index1,word2,index2]
	params:
	@input_string: list of dependencies
	output:
	@words:    list of IndexedWord objects
	@dep_arcs: list of DependencyArc objects
	'''

	words = set()
	dep_arcs = []

	for line in input_string.splitlines():
		arc_parts = []
		elems = list(filter(None, re.split(' ',line[1:len(line)-1],maxsplit=5)))

		# Handle special cases (ncsubj, xcomp, cmod)
		if elems[0]=='ncsubj':
			elems[0] = elems[0]+':'+elems[-1] if elems[-1]!='_' else elems[0]
			del elems[-1]
		elif elems[0]=='xcomp':
			if elems[1]!='_':
				parts = elems[1].rsplit('_',1)
				words.add(IndexedWord(parts[0],int(parts[1])+1))
				elems[0]='xcomp:{}'.format(parts[0])
			del elems[1]
		if elems[0]=='cmod':
			if elems[1]!='_':
				parts = elems[1].rsplit('_',1)
				words.add(IndexedWord(parts[0],int(parts[1])+1))
				elems[0]='cmod:{}'.format(parts[0])
				del[elems[1]]
		elif len(elems)==4:
			elems[0] = elems[0]+':'+elems[1] if elems[1]!='_' else elems[0]
			del elems[1]

		arc_parts.append(elems[0])

		for w in elems[1:]:
			parts = [part for part in w.rsplit('_',1) if part is not '']
			arc_parts+=parts

		new_arc = _generate_arcs(arc_parts,'candc')
		words.add(IndexedWord(arc_parts[1],int(arc_parts[2])+1))
		words.add(IndexedWord(arc_parts[3],int(arc_parts[4])+1))

		dep_arcs.append(new_arc)
	return words,dep_arcs

def generate_dep_arcs(input_string,parse_type):
	'''
	Take list of grammatical relations and return parsed objects
	arc_parts is an intermediate object structured as [label,word1,index1,word2,index2]
	params:
	@input_string: list of dependencies
	output:
	@words_sorted: sorted list of IndexedWord objects
	@dep_arcs: list of DependencyArc objects
	'''

	# switch on parser type
	if parse_type=='stanford':
		words,dep_arcs = arc_parse_stanford(input_string)
	elif parse_type=='candc':
		words,dep_arcs = arc_parse_candc(input_string)

	words_sorted = sorted(list(words), key=lambda x: x.index)
	return words_sorted,dep_arcs

	
def make_root_arc(sent,dep_arcs):
	'''
	Generate special string for root arc for Stanford parser outputs
	params:
	@sent 	:list of IndexedWord objects representing parsed sentence
	@dep_arcs:list of DependencyArc objects
	output:
	@sent   :list of IndexedWord objects representing parsed sentence
	@dep_arcs:list of Dependency Arcs objects
	@root_str: tikz TeX object for root arc
	'''

	# start with empty str
	root_str = ''

	# find any roots in the sentence
	root_arcs = [arc for arc in dep_arcs if arc.is_root==True]

	# if roots exist generate tikz object 
	for arc in root_arcs:
		root_idx = arc.end_word.index
		root_str += '\\deproot{}{}\n'.format('{'+str(root_idx)+'}','{root}')

	# Trim root from sent and dep_arcs 
	if sent[0].word=='ROOT':
		sent = sent[1:]
	dep_arcs = [a for a in dep_arcs if a.is_root==False]

	return sent, dep_arcs, root_str
	

def make_plain_sent(sent,text_options):
	'''
	Generate tikz format string object of sentence
	Arcs are then added as annotations to this sentence
	params:
	@sent 	:list of IndexedWord objects representing parsed sentence
	@text_options: text style options
	output:
	@str 	:output string of sentence
	'''

	# form string as tokens with \& between and ending in \\
	sent_str = ' \& '.join([w.word for w in sent]) + '\\\\'

	return '{}[{}]\n{}\n{}\n'.format(
		'\\begin{deptext}',
		text_options,
		sent_str,
		'\\end{deptext}'
		)


def make_dep_arcs(dep_arcs):
	'''
	Generate tikz format string object of every dependency arc
	params:
	@dep_arcs: list of DependencyArc objects
	output:
	arc_str:  string object of every arc tex object
	'''

	# start with empty string
	arc_str = ''

	# iterate over each arc
	for arc in dep_arcs:

		# starting index
		start = arc.start_word.index

		# ending index
		end = arc.end_word.index

		# Typed Dependency Grammar (RASP or Universal) label
		label = arc.label

		# Form string
		current_arc_str = u"\\depedge{%s}{%s}{%s}\n"%(start,end,label)
		arc_str += current_arc_str

	return arc_str

def write_tex_fig(sent,dep_arcs,full_dir,filename,doc,text_options):
	'''
	Generate a tikz-dependency figure @full_dir
	params:
	@sent : 	list of IndexedWord objects representing parsed sentence
	@dep_arcs: 	list of dependency arcs annotating sentence
	@full_dir: 	location of file.tex
	@doc: 		generate full document (add doc post+preamble)
	@text_options: add style options
	'''
	file = open('{}/{}'.format(full_dir,filename),'w')

	# dump document opening object
	if doc:
		file.writelines(doc_preamble)

	# dump figure preample
	file.writelines(fig_preamble)

	# generate root if exists
	sent,dep_arcs,root_str = make_root_arc(sent,dep_arcs)

	# generate sentence object for arcs to annotate
	sent_str = make_plain_sent(sent,text_options)

	# generate dep arc annotations
	arcs = make_dep_arcs(dep_arcs)
	
	# add sentence, dep arcs and root
	file.writelines(sent_str)
	file.writelines(root_str)
	file.writelines(arcs)

	# add figure postamble
	file.writelines(fig_postamble)
	file.close()

if __name__ == '__main__':

	# get parent folder (parsers project root)
	root_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

	# declare parsing objects
    parses = [
    ParseConfig(
    	'output/pcfg_stanford_parse_output.txt',
    	'output/stanford-pcfg-tex',
    	'stanford'
    	),

    ParseConfig(
    	'output/nn_stanford_parse_output.txt',
    	'output/stanford-nn-tex',
    	'stanford'
    	),

    ParseConfig(
    	'output/ccg_candc_parse_output.txt',
    	'output/candc-raw-tex',
    	'candc'
    	)
    ]

    for parse in parses:

    	# open file with parse results
    	in_file_path = root_dir + os.sep + parse.dir
    	with open(in_file_path,'r') as fh:
    		text = fh.read()

    	# split into parsees
    	parse_list = text.split('\n\n')

    	# generate parse graphs for each dep-parse read in
    	for p in parse_list:
    		print('Running AfterParsey for parser{} on parse {} of {}...'.format(parse.type,parse_list.index(p)+1,len(parse_list)))
    		sent, dep_arcs = generate_dep_arcs(p)


    		print('Writing TeX fig for parse {} of {}...'.format(parse_list.index(p)+1,len(parse_list)))
    		print()
    		print('Sentence recovered from depparse: {} ...'.format(' '.join(w.word for w in sent)))
    		print()

    		out_file_path = root_dir + os.sep + parse.output

    		#write_tex_fig(sent=sent,dep_arcs=dep_arcs,full_dir=out_file_path,filename='parse{}.tex'.format(parse_list.index(p)+1),doc=False,text_options='column sep=0.3cm')

