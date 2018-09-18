from ..src.spellcheck import *

def testWrapper():

	# Define requisite classes up here

	spellchecker = Spellchecker()

	# Define tester functions here

	def levenshteinTests():
		tests = []
		tests.append((("hlelo","hello"), 2))
		tests.append((("appel","apple"), 2))
		tests.append((("ti","it"), 2))
		tests.append((("app", "ape"),1))
		tests.append((("app", "apply"),2))
		return {
			"function": spellchecker.calcLevenshteinDist,
			"tests": tests,
			"desc": "levenshtein"
		}

	def levenshteinSuggestionTests():
		tests = []
		tests.append(("ist", "its"))
		tests.append(("hlelo", "hello"))
		return {
			"function": spellchecker.levenshteinEditSuggestion,
			"tests": tests, 
			"desc": "edit suggestions"
		}

	#Append each of the tests you want to run here

	def getTests():
		tests = []
		tests.append(levenshteinTests)
		tests.append(levenshteinSuggestionTests)
		return tests

	return getTests()


