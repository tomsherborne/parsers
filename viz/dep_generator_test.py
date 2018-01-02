# Documentation https://mirror.hmc.edu/ctan/graphics/pgf/contrib/tikz-dependency/tikz-dependency-doc.pdf
import string
import re 
from collections import namedtuple


IndexedWord = namedtuple('IndexedWord','word index')
DependencyArc = namedtuple('DependencyArc','start_word end_word label is_root')
stanford_re = r'(\(|\)|,)'
filter_out = ['','(',')','.',',',' ']

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


def _generate_arcs(elems):
	new_arc = []
	
	label = elems[0]
	is_root = True if elems[0]=='root' else False

	startw = IndexedWord(elems[1],elems[2])
	endw = IndexedWord(elems[3],elems[4])

	return DependencyArc(startw,endw,label,is_root)

	# for word in elems[1:]:
	# 	#word_elems = word.replace('_','-').split('-')
	# 	word_elems = [w for w in word_elems if w is not '' or not ' ']
	# 	#print(word_elems)
	# 	new_word = IndexedWord(word_elems[0],int(word_elems[1]))
	# 	new_arc.append(new_word)
	# 	new_words.add(new_word)
	# is_root = True if elems[0]=='root' else False
	#return DependencyArc(new_arc[0],new_arc[1],elems[0],is_root),new_words

def generate_dep_arcs_stanford(input_string):
	'''
	Take list of grammatical relations and return
	1. list of DependencyArc objects
	2. list of IndexedWord objects
	'''
	words = set()
	dep_arcs = []

	for line in input_string.splitlines():
		arc_parts = []
		elems = list(filter(None, re.split('[\(\)]+',line,maxsplit=2)))
		arc_parts.append(elems[0])

		arc_words = [w.strip() for w in filter(None, re.split(',',elems[1],maxsplit=1))]
		for w in arc_words:
			arc_parts += w.rsplit('-',1)
		
		new_arc = _generate_arcs(arc_parts)

		words.add(IndexedWord(arc_parts[1],int(arc_parts[2])))
		words.add(IndexedWord(arc_parts[3],int(arc_parts[4])))

		dep_arcs.append(new_arc)

	words_sorted = sorted(list(words), key=lambda x: x.index)
	return words_sorted,dep_arcs


def generate_dep_arcs_candc(input_string):
	'''
	Take list of grammatical relations and return
	1. list of DependencyArc objects
	2. list of IndexedWord objects
	'''

	words = set()
	dep_arcs = []

	for line in input_string.splitlines():
		arc_parts = []
		elems = list(filter(None, re.split(' ',line[1:len(line)-1],maxsplit=5)))

		# Handle special cases
		if elems[0]=='ncsubj':
			elems[0] = elems[0]+':'+elems[-1] if elems[-1]!='_' else elems[0]
			del elems[-1]
		elif elems[0]=='xcomp':
			if elems[1]!='_':
				parts = elems[1].rsplit('_',1)
				words.add(IndexedWord(parts[0],int(parts[1])))
				elems[0]='xcomp:{}'.format(parts[0])
			del elems[1]
		if elems[0]=='cmod':
			if elems[1]!='_':
				parts = elems[1].rsplit('_',1)
				words.add(IndexedWord(parts[0],int(parts[1])))
				elems[0]='cmod:{}'.format(parts[0])
				del[elems[1]]
		elif len(elems)==4:
			elems[0] = elems[0]+':'+elems[1] if elems[1]!='_' else elems[0]
			del elems[1]

		arc_parts.append(elems[0])

		for w in elems[1:]:
			parts = [part for part in w.rsplit('_',1) if part is not '']
			arc_parts+=parts

		new_arc = _generate_arcs(arc_parts)
		words.add(IndexedWord(arc_parts[1],int(arc_parts[2])))
		words.add(IndexedWord(arc_parts[3],int(arc_parts[4])))

		dep_arcs.append(new_arc)

	words_sorted = sorted(list(words), key=lambda x: x.index)
	return words_sorted,dep_arcs
	
def handle_root_arc(sent,dep_arcs):
	root_str = ''
	root_arcs = [a for a in dep_arcs if a.is_root==True]
	for arc in root_arcs:
		root_idx = arc.end_word.index
		root_str += '\\deproot{}{}\n'.format('{'+str(root_idx)+'}','{root}')

	if sent[0].word=='ROOT':
		sent = sent[1:]

	dep_arcs = [a for a in dep_arcs if a.is_root==False]

	return sent, dep_arcs, root_str
	

def make_plain_sent(sent,text_options):
	sent_str = ' \& '.join([w.word for w in sent]) + ' \\\\'
	return '{}[{}]\n{}\n{}\n'.format(
		'\\begin{deptext}',
		text_options,
		sent_str,
		'\\end{deptext}')


def make_dep_arcs(dep_arcs):
	arc_str = ''

	for arc in dep_arcs:
		start = arc.start_word.index
		end = arc.end_word.index
		label = arc.label
		current_arc_str = u"\\depedge{%s}{%s}{%s}\n"%(start,end,label)
		arc_str += current_arc_str

	return arc_str

def write_tex_fig(sent,dep_arcs,full_dir,filename,text_options):
	file = open('{}/{}'.format(full_dir,filename),'w+')
	file.writelines(fig_preamble)

	sent,dep_arcs,root_str = handle_root_arc(sent,dep_arcs)
	sent_str = make_plain_sent(sent,text_options)
	arcs = make_dep_arcs(dep_arcs)
	
	file.writelines(sent_str)
	file.writelines(root_str)
	file.writelines(arcs)

	file.writelines(fig_postamble)
	file.close()

def write_tex_doc(sent,dep_arcs,full_dir,filename):
	pass


if __name__ == '__main__':

    parses = [
    {'dir':'/Users/tom/Desktop/Cambridge/L95-SyntaxParsing/parsers/output/pcfg_stanford_parse_output.txt',
    'output':'/Users/tom/Desktop/Cambridge/L95-SyntaxParsing/parsers/output/stanford-pcfg-tex',
    'type':'stanford'},
    {'dir':'/Users/tom/Desktop/Cambridge/L95-SyntaxParsing/parsers/output/nn_stanford_parse_output.txt',
    'output':'/Users/tom/Desktop/Cambridge/L95-SyntaxParsing/parsers/output/stanford-nn-tex',
     'type':'stanford'},
	{'dir':'/Users/tom/Desktop/Cambridge/L95-SyntaxParsing/parsers/output/ccg_candc_parse_output_clean.txt',
	 'output':'/Users/tom/Desktop/Cambridge/L95-SyntaxParsing/parsers/output/candc-raw-tex',
	 'type':'candc'},
	{'dir':'/Users/tom/Desktop/Cambridge/L95-SyntaxParsing/parsers/output/ccg_candc_parse_punc_output_clean.txt',
	 'output':'/Users/tom/Desktop/Cambridge/L95-SyntaxParsing/parsers/output/candc-punc-tex',
	 'type':'candc'}
    ]

    for parse in parses:
    	with open(parse['dir'],'r') as fh:
    		text = fh.read()
    	parse_list = text.split('\n\n')
    	print(parse['type'])
    	for p in parse_list:
    		print('Running afterparsey for {} of {}'.format(parse_list.index(p),len(parse_list)))
    		if parse['type']=='stanford':
    			sent, dep_arcs = generate_dep_arcs_stanford(p)
    		elif parse['type']=='candc':
    			sent, dep_arcs = generate_dep_arcs_candc(p)
    		print(' '.join(w.word for w in sent))
    		write_tex_fig(sent,dep_arcs,parse['output'],'parse{}.tex'.format(parse_list.index(p)),'column sep=0.5cm')

	#print(sent1)
	#print()
	#print(dep_arcs1)

    # with open(stanford_parse1,'r') as fh:
    # 	text = fh.read()

    # parses = text.split('\n\n')
    # for l in parses:
    # 	print('next parse')
    # 	print('>>>>>>>>>>>>>>>>>>>>>>>>>')
    # 	print(l)
    # 	print('<<<<<<<<<<<<<<<<<<<<<<<<<')

	#sent1, dep_arcs1 = generate_dep_arcs_stanford(stanford_deps)
	#print([da for da in dep_arcs1 if da.is_root==True])
	#write_tex_fig(sent1,dep_arcs1,'/Users/tom/Desktop/Cambridge/L95-SyntaxParsing/parsers/viz/test','test.tex','column sep=0.5cm')
