import argparse
from .spellcheck import *

def spellcheckEntry():
	parser = argparse.ArgumentParser(description='Code-mixed spellchecking')
	parser.add_argument('file', metavar = 'F', type=str, help='file with newline-separated code-mixed content.')
	parser.add_argument('-A', default = 1,type=int, help='least-interference normalization (default)')
	parser.add_argument('-outputType', default = "firstOf", type=str, help='what your program outputs. Options: \'firstOf\', \'lattice\'')
	parser.add_argument('-langTag', default = None, type=str, help='the non-English language in the code-mixed text. If not included, tags text for you.')
	parser.add_argument('-tagDoc',default = None, type=str,help='the text file containing words tagged with language id (word and language denoted)')
	parser.add_argument('-dictDoc',default = None, type=str,help='dictionary of words in language denoted by -langTag (ascii only)')
	parser.add_argument('-repklEng', action='store_true',help='remake and repickle the English spellchecker object')
	parser.add_argument('-repklAlt', action='store_true',help='remake and repickle the other language spellchecker object')


	args = parser.parse_args()

	if(not args.langTag):
		print("Must specify non-English code-mixed language.")

	if(not (args.tagDoc or args.dictDoc)):
		print("Must supply tagged corpus of code-mixed words or dictionary of words in given language.")

	spellchecker = Spellchecker(args.langTag, args.repklEng, args.repklAlt, args.A, args.outputType, args.tagDoc, args.dictDoc)

	with open(args.file) as f:
		lines = f.readlines()
		for line in lines:
			line = line[:-1]
			print(spellchecker.correctSentence(line))
