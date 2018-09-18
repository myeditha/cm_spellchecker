import sys
from .tests import *

class FailedTest(Exception):
		pass

def runFunction(test,func):
	if type(test[0] is tuple):
		return func(*test[0])
	else:
		return func(test[0])

def testFunction(test, func, num, verbose):
	res = runFunction(test,func()["function"])
	if res!=test[1]:
		if verbose:
			print("Failed test " + str(num+1) + ", " + func()["desc"] + ": on input " + repr(str(test[0])) + ", expected " + repr(str(test[1])) + " but received " + repr(str(res)))
		return False
	else:
		if verbose:
			print("Passed test " + str(num+1) + ", " + func()["desc"])
		return True

def main():
	verbose = False 
	if "-V" in sys.argv:
		verbose = True
	tests = testWrapper()
	for func in tests:
		counter = 0
		for num in range(0,len(func()["tests"])):
			test = func()["tests"][num]
			if(testFunction(test,func, num, verbose)):
				counter+=1
		print("\nPassed " + str(counter) + " out of " + str(len(func()["tests"])) + " for " + func()["desc"] + "\n")
	return

main()