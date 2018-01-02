import spacy
import sys
from collections import namedtuple

if __name__ == '__main__':

	IndexedWord = namedtuple('IndexedWord','word index')
	DependencyArc = namedtuple('DependencyArc','start_word end_word label')
	
	nlp = spacy.load('en')
	sent = u'Letters delivered on time by old-fashioned means are increasingly rare, so it is as well that that is not the only option available.'
	doc = nlp(sent)
	arcs = set()

	for token in doc:
		newArc = DependencyArc(IndexedWord(token.head.text,token.head.i+1),IndexedWord(token.text,token.i+1),token.dep_)
		arcs.add(newArc)
		print(newArc)
		print()

