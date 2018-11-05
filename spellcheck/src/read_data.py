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

def makeEnglishDict(addr):
    return readFileAsDict2(addr)

def makeBkTree(func, addr):
    return pybktree.BKTree(func, __readFilesAsList(addr))

def makeBkTreeFromPkl(func, repkl, lang, addr):
    if not os.path.exists(addr) or repkl:
        if not repkl:
            print("cannot detect English spellchecker file object")
        print("repickling English spellchecker object")
        bktree = makeBkTree(func, addr)
        with open(addr, "wb") as f: 
            pickle.dump(bktree, f)
        return bktree
    else:
        print("detected English spellchecker object; loading")
        with open(addr, "rb") as f:
            return pickle.load(f)        

def makeMetaDict(addr):
    return readFileAsDict(addr)

def readFileAsDict2(direc):
    dictionary = dict()
    with open(direc) as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1].lower()
            dictionary[line] = 1
    return dictionary

def readFileAsDict(direc):
    dictionary = dict()
    with open(direc) as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1].split(' ')
            dictionary[line[0]] = line[1]
    return dictionary

