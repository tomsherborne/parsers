# Documentation https://mirror.hmc.edu/ctan/graphics/pgf/contrib/tikz-dependency/tikz-dependency-doc.pdf
import string
import re 
from collections import namedtuple


IndexedWord = namedtuple('IndexedWord','word index')
DependencyArc = namedtuple('DependencyArc','start_word end_word label is_root')
stanford_re = r'(\(|\)|,| )'
filter_out = ['','(',')','.',',',' ']

doc_preamble = r'''
\documentclass{article}
\usepackage[margin=1cm]{geometry}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{tikz-dependency}
\usetikzlibrary{positioning}
\pgfplotsset{compat=1.14}
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


def generate_dep_arcs_stanford(input_string):
	'''
	Take list of grammatical relations and return
	1. list of DependencyArc objects
	2. list of IndexedWord objects
	'''
	words = set()
	deparcs = []

	for line in input_string.splitlines():
		elems = [e for e in re.split(stanford_re, line) if e not in filter_out]
		new_arc = []
		for word in elems[1:]:
			word_elems = word.split('-')
			new_word = IndexedWord(word_elems[0],int(word_elems[1]))
			new_arc.append(new_word)
			words.add(new_word)
		print(elems[0])
		is_root = True if elems[0]=='root' else False
		deparcs.append(DependencyArc(new_arc[0],new_arc[1],elems[0],is_root))

	words_sorted = sorted(list(words), key=lambda x: x.index)
	return words_sorted,deparcs


def generate_dep_arcs_candc(input_string):
	pass

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
		current_arc_str = u"\\depedge{%d}{%d}{%s}\n"%(start,end,label)
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



# def generate_tikz_stanford(input_string):
# 	dmp_file = open('./dmp.tex','w')
# 	dmp_file.writelines(preamble)

# 	words = set()
# 	deparcs = []

# 	for line in input_string.splitlines():
# 		elems = [e for e in re.split(stanford_re, line) if e not in filter_out]
# 		new_arc = []
# 		for word in elems[1:]:
# 			word_elems = word.split('-')
# 			new_word = IndexedWord(word_elems[0],int(word_elems[1]))
# 			new_arc.append(new_word)
# 			words.add(new_word)

# 		deparcs.append(DependencyArc(naew_arc[0],new_arc[1],elems[0]))
# 		#words_formatted = ['({}) {}'.format(w.index,w.word) for w in words]
# 		#g.edge(words_formatted[0],words_formatted[1],label=elems[0])

# 	print(deparcs)
# 	print(words)
# 	words_sorted = sorted(list(words), key=lambda x: x.index)
# 	ordered_sentence = [w.word for w in words_sorted]
# 	sent_str = ' \& '.join(ordered_sentence[1:]) + " \\\\\n"
# 	dmp_file.writelines('\\begin{deptext}\n')
# 	dmp_file.writelines(sent_str)
# 	dmp_file.writelines('\\end{deptext}\n')
	
# 	for arc in deparcs:
# 		print(arc)
# 		start = arc.start_word.index
# 		print(start)
# 		end = arc.end_word.index
# 		print(end)
# 		label = arc.label
# 		print(label)
# 		arc_str = u"\\depedge{%d}{%d}{%s}\n"%(start,end,label)
# 		print(arc_str)
# 		dmp_file.writelines(arc_str)

# 	dmp_file.writelines(postamble)
# 	dmp_file.close()


# 	return ordered_sentence

if __name__ == '__main__':

	stanford_deps = """det(car-3, The-1)
amod(car-3, old-2)
nsubj(broke-4, car-3)
root(ROOT-0, broke-4)
compound:prt(broke-4, down-5)
case(park-9, in-6)
det(park-9, the-7)
compound(park-9, car-8)
nmod:in(broke-4, park-9)
"""

	candc_deps = '''(ncmod _ car_2 old_1)
(det car_2 The_0)
(xcomp _ broke_3 down_4)
(ncmod _ park._8 car_7)
(det park._8 the_6)
(dobj in_5 park._8)
(ncmod _ broke_3 in_5)
(ncsubj broke_3 car_2 _)
'''

	#a = stanford_generator(stanford_deps)
	#a.view()

	#b = candc_generator(candc_deps)
	#b.view()
	#print(generate_tikz_stanford(stanford_deps))

	sent1, dep_arcs1 = generate_dep_arcs_stanford(stanford_deps)

	print(' '.join(w.word for w in sent1))
	print([da for da in dep_arcs1 if da.is_root==True])
	write_tex_fig(sent1,dep_arcs1,'/Users/tom/Desktop/Cambridge/L95-SyntaxParsing/parsers/viz/test','test.tex','column sep=0.5cm')
