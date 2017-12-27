# parsers
A review of dependency parsing (Stanford, C&amp;C CCG and spaCy)

## Requires
* spaCy parser
```
pipenv install spacy
```
followed by
```
pipenv run python -m spacy download en
```
* GraphViz for Python for producing graph based visualisations
```
pip install graphviz
```
* A LaTeX installation including `tikz-dependency.sty` 
* A `src-parsers` folder containing the parsers e.g.
```
parsers \
	-> src-parsers \
		-> candc-1.00
		
		-> stanford-parser-full-2017-06-09
```
