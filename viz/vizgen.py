# Documentation https://mirror.hmc.edu/ctan/graphics/pgf/contrib/tikz-dependency/tikz-dependency-doc.pdf

import string
import re 
from collections import namedtuple

from graphviz import Digraph

IndexedWord = namedtuple('IndexedWord','word index')
DependencyArc = namedtuple('DependencyArc','start_word end_word label')
stanford_re = r'(\(|\)|,| )'
filter_out = ['','(',')','.',',',' ']


def stanford_generator(input_string):
	g = Digraph()
	g.attr('edge',dir='forward')
	g.attr('node',shape='plaintext')
	
	for line in input_string.splitlines():
		elems = [e for e in re.split(stanford_re, line) if e not in filter_out]
		words = []
		for word in elems[1:]:
			word_elems = word.split('-')
			new_word = IndexedWord(word_elems[0],int(word_elems[1]))
			words.append(new_word)

		words_formatted = ['({}) {}'.format(w.index,w.word) for w in words]
		g.edge(words_formatted[0],words_formatted[1],label=elems[0])

	return g

def candc_generator(input_string):
	g = Digraph()
	g.attr('edge',dir='forward')
	g.attr('node',shape='plaintext')
	
	for line in input_string.splitlines():
		elems = [e for e in re.split(stanford_re, line) if e not in filter_out]

		if elems[0]=='ncsubj':
			elems[0] = elems[0]+elems[-1] if elems[-1]!='_' else elems[0]
			del elems[-1]
		elif len(elems)==4:
			elems[0] = elems[0]+elems[1] if elems[1]!='_' else elems[0]
			del elems[1]

		print(elems)
		words = []
		for word in elems[1:]:
			word_elems = word.split('_')
			new_word = IndexedWord(word_elems[0],int(word_elems[1]))
			words.append(new_word)

		words_formatted = ['({}) {}'.format(w.index,w.word) for w in words]
		g.edge(words_formatted[0],words_formatted[1],label=elems[0])

	return g

preamble = r'''
\documentclass{article}
\usepackage{pgfplots}
\usepackage{tikz-dependency}
\pgfplotsset{compat=1.14}
\begin{document}
\begin{tikzpicture}
\begin{dependency}
'''

postamble = r'''
\end{dependency}
\end{tikzpicture}
\end{document}
'''

def generate_tikz_stanford(input_string):
	dmp_file = open('./dmp.tex','w')
	dmp_file.writelines(preamble)

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

		deparcs.append(DependencyArc(new_arc[0],new_arc[1],elems[0]))
		#words_formatted = ['({}) {}'.format(w.index,w.word) for w in words]
		#g.edge(words_formatted[0],words_formatted[1],label=elems[0])

	print(deparcs)
	print(words)
	words_sorted = sorted(list(words), key=lambda x: x.index)
	ordered_sentence = [w.word for w in words_sorted]
	sent_str = ' \& '.join(ordered_sentence[1:]) + " \\\\\n"
	dmp_file.writelines('\\begin{deptext}\n')
	dmp_file.writelines(sent_str)
	dmp_file.writelines('\\end{deptext}\n')
	
	for arc in deparcs:
		print(arc)
		start = arc.start_word.index
		print(start)
		end = arc.end_word.index
		print(end)
		label = arc.label
		print(label)
		arc_str = u"\\depedge{%d}{%d}{%s}\n"%(start,end,label)
		print(arc_str)
		dmp_file.writelines(arc_str)

	dmp_file.writelines(postamble)
	dmp_file.close()


	return ordered_sentence

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
	print(generate_tikz_stanford(stanford_deps))
