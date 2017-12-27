from graphviz import Source, Digraph
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse import DependencyGraph
import os 

stanford_parser_dir = '/Users/tom/stanford-tools/stanford-parser-full-2017-06-09/'

my_path_to_models_jar = stanford_parser_dir  + "stanford-parser-3.8.0-models.jar"
my_path_to_jar = stanford_parser_dir  + "stanford-parser.jar"

sdp = StanfordDependencyParser(path_to_jar=my_path_to_jar, path_to_models_jar=my_path_to_models_jar)

sentence = 'The old car broke down in the car park.'

#sdp = StanfordDependencyParser()
result = list(sdp.raw_parse(sentence))
print([parse for parse in result])
print([parse.tree() for parse in result])
print()

dep_tree_dot_repr = [parse for parse in result][0].to_dot()
print(dep_tree_dot_repr)
source = Source(dep_tree_dot_repr, filename="dep_tree", format="png")
source.view()

deps = """
det(car-3, The-1)
amod(car-3, old-2)
nsubj(broke-4, car-3)
root(ROOT-0, broke-4)
compound:prt(broke-4, down-5)
case(park-9, in-6)
det(park-9, the-7)
compound(park-9, car-8)
nmod:in(broke-4, park-9)
"""

