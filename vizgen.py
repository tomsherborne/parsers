import string
import re 
from collections import namedtuple

from graphviz import Digraph

# IndexedWord = namedtuple('IndexedWord','word index')
# filter_out = ['','(',')','.',',',' ']

# g = Digraph()
# g.attr('edge',dir='forward')
# g.attr('node',shape='plaintext')

# sentence = set()

# for line in deps.splitlines():
# 	elems = [e for e in re.split(r'(\(|\)|,| )', line) if e not in filter_out]
# 	rel = elems[0]

# 	words = []
# 	for word in elems[1:]:
# 		print(word)
# 		word_elems = word.split('-')
# 		new_word = IndexedWord(word_elems[0],int(word_elems[1]))
# 		sentence.add(new_word)
# 		words.append(new_word)

# 	words_formatted = ['({}) {}'.format(w.index,w.word) for w in words]
# 	print(words_formatted)

# 	g.edge(words_formatted[0],words_formatted[1],label=rel)

# print(g.source)
# g.view()
# sentence = list(sentence)
# sentence.sort(key=lambda w: w.index, reverse=False)
# print(' '.join([w.word for w in sentence]))

IndexedWord = namedtuple('IndexedWord','word index')
DependencyArc = namedtuple('DependencyArc','start_word end_word label index')
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



# \begin{deptext}
# My \& dog \& also \& likes \& eating \& sausage \\
# \end{deptext}
# \depedge{2}{1}{poss}
# \depedge{4}{2}{nsubj}
# \depedge{4}{3}{advmod}
# \depedge{4}{5}{xcomp}
# \depedge{5}{6}{dobj}

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
	dmp_file.writelines(postamble)
	dmp_file.close()

	for line in input_string.splitlines():
		elems = [e for e in re.split(stanford_re, line) if e not in filter_out]
		words = []
		for word in elems[1:]:
			word_elems = word.split('-')
			new_word = IndexedWord(word_elems[0],int(word_elems[1]))
			words.append(new_word)

		words_formatted = ['({}) {}'.format(w.index,w.word) for w in words]
		g.edge(words_formatted[0],words_formatted[1],label=elems[0])

	return None

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
