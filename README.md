# parsers
## Tom Sherborne Dec 2017
A review of dependency parsing (Stanford PCFG and NNdep, C&amp;C CCG)
I use `pipenv` where one could use `pip`, but I would recommend in a `virtualenv` or `conda env`

## Folders
```
-> input 	# input file location
-> output 	# output file location
-> run		# run scripts for calling external parsers and handling input/output
-> viz 		# visualise parser output from output/ folder

```

## Requirements
* GraphViz for Python for producing graph based visualisations
```
pipenv install graphviz
```
* A LaTeX installation including `tikz-dependency.sty` 
* A `src-parsers` folder containing the parsers e.g.
```
-> parsers \
	-> src-parsers \
		-> candc-1.00
		
		-> stanford-parser-full-2017-06-09
```
* spaCy parser **spacy is currently 'unsupported'**
```
pipenv install spacy
```
followed by
```
pipenv run python -m spacy download en
```

## Todo
* [x] Refactor `tikz-dependency` arc generator with comments
* [ ] File writing safety checks
* [ ] Fix offset bug which causes C&C parse graph generator to orphan words