import sys
import argparse

def main():
	parser = argparse.ArgumentParser(description='Code-mixed spellchecking')
	parser.add_argument('file', metavar = 'F', type=str, help='file with code-mixed content, separated by newlines.')
	parser.add_argument('-A1', action = 'store_true', help='least-interference normalization (default)')
	parser.add_argument('-A2', action = 'store_true', help='more aggressive normalization')
	parser.add_argument('-A3', action = 'store_true', help='most aggressive normalization')
	parser.add_argument('-outputType', default = "firstOf", type=str, help='what your program outputs. Options: \'firstOf\', \'lattice\'')
	parser.add_argument('-langTag', default = None, type=str, help='the non-English language in the code-mixed text. If not included, tags text for you.')
	parser.add_argument('-tagDoc',default = None, type=str,help='text is tagged with language id')
	parser.add_argument('-repklEng', action='store_true',help='remake and repickle the English spellchecker object')

	args = parser.parse_args()

	if(args.langTag != "tel"):
		print("")



