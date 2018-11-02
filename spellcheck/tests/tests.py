from ..src.spellcheck import *

def testWrapper():

	# Define requisite classes up here

	spellchecker = Spellchecker(False, 1, "f", "../data/teluguwords.txt")

	# Define tester functions here

	# You can either directly check if the output is equivalent to a value ...

	def levenshteinTests():
		tests = []
		tests.append((("hellx","helix"), 1))
		tests.append((("appel","apple"), 2))
		tests.append((("ti","it"), 2))
		tests.append((("app", "ape"),1))
		tests.append((("apply", "app"),2))
		return {
			"function": spellchecker.calcLevenshteinDist,
			"tests": tests,
			"desc": "levenshtein"
		}

	# ... Or use a predicate function to determine if you pass the test.

	def levenshteinSuggestionTests():
		# WARNING: These tests are quite slow. 
		tests = []
		tests.append(("ist", lambda l: "is" in l))
		tests.append(("hlelo", lambda l: "hello" in l))
		return {
			"function": spellchecker.levenshteinEditSuggestion,
			"tests": tests, 
			"desc": "edit suggestions"
		}

	def levenshteinSuggestionTestsCap():
		tests = []
		tests.append((("ist",2), lambda l: "is" in list(map(lambda x: x[1], l))))
		tests.append((("hlelo",2), lambda l: "hello" in list(map(lambda x: x[1], l))))
		tests.append((("abacas",2), lambda l: "abacus" in list(map(lambda x: x[1], l))))
		return {
			"function": spellchecker.levenshteinEditSuggestionCap,
			"tests": tests, 
			"desc": "edit suggestions"
		}

	# Append each of the tests you want to run here

	def getTests():
		tests = []
		tests.append(levenshteinTests)
		# tests.append(levenshteinSuggestionTests)
		tests.append(levenshteinSuggestionTestsCap)
		return tests

	return getTests()


