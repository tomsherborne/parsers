# parsers
A review of dependency parsing (Stanford, C&amp;C CCG and spaCy)

## Requires
* spaCy
```
pipenv install spacy
```
then
```
pipenv run python -m spacy download en

```
* GraphViz
* A working LaTex installation including tikz-dependency.sty 
* Python 3.5
* A `src-parsers` folder containing the parsers e.g.
```
parsers 
	-> src-parsers 
		-> candc-1.00
	    -> stanford-parser-full-2017-06-09

```
