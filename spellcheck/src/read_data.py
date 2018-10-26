import pybktree
import pickle
import os.path

def __readFilesAsList(direc):
    dictionary = []
    with open(direc) as f:
        dictionary = list(map(lambda x: x.strip(), f.readlines()))
    return dictionary

def __retrieveDictionary(addr):
    return __readFilesAsList(addr)

def makeEnglishDict(addr = "spellcheck/data/DICT.txt"):
    return __retrieveDictionary(addr)

def makeBkTree(func, addr = "spellcheck/data/DICT.txt"):
    return pybktree.BKTree(func, __readFilesAsList(addr))

def makeBkTreeFromPkl(func, repkl, addr = "spellcheck/data/bktree.pkl"):
    if not os.path.exists(addr) or repkl:
        if not repkl:
            print("cannot detect English spellchecker file object")
        print("repickling English spellchecker object")
        bktree = makeBkTree(func)
        with open(addr, "wb") as f: 
            pickle.dump(bktree, f)
        return bktree
    else:
        print("detected English spellchecker object; loading")
        with open(addr, "rb") as f:
            return pickle.load(f)        

def makeMetaDict(addr = "spellcheck/data/DICT.txt"):
    return readFileAsDict(addr)

def readFileAsDict(direc):
    dictionary = dict()
    with open(direc) as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1].split(' ')
            dictionary[line[0]] = line[1]
    return dictionary

