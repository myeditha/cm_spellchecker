import pybktree
import pickle
import os.path
import metaphone
import operator

spellcheckpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
datapath = os.path.join(spellcheckpath,"data")

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

def makeBkTreeFromPkl(func, lang, addr, bktreepath, repkl=False):
    if not os.path.exists(bktreepath) or repkl:
        if not repkl:
            print("cannot detect " + lang + " spellchecker file object")
        print("repickling " + lang + " spellchecker object")
        bktree = makeBkTree(func, addr)
        with open(bktreepath, "wb") as f: 
            pickle.dump(bktree, f)
        return bktree
    else:
        print("detected " + lang + " spellchecker object; loading")
        with open(bktreepath, "rb") as f:
            return pickle.load(f)        

def makeMetaDict(addr):
    metaDictAddr = addr.rsplit(".", 1)[0] + "PHTAGGED.txt"
    if(os.path.exists(metaDictAddr)):
        return readFileAsDict(metaDictAddr)
    else:
        metawords = []
        with open(addr, "r") as f:
            nlines = map(lambda x: x[:-1], f.readlines())
            metawords = create_soundex_dict(nlines)

        with open(metaDictAddr, "w") as f:
            f.write('\n'.join(metawords))

        return metawords
    

def readFileAsDict2(direc):
    dictionary = dict()
    with open(direc) as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1].lower()
            dictionary[line] = 1
    return dictionary

def create_soundex_dict(nlines):
    dmeta = metaphone.dm
    mydict = dict()
    for word in nlines:
        try:
            sound = dmeta(word)[0]
            wordkey = word
        except UnicodeDecodeError:
            sound = word
            wordkey = "count"

        if not sound in mydict:
                mydict[sound] = dict()
                mydict[sound][wordkey] = 1
        else:
            if not word in mydict[sound]:
                mydict[sound][wordkey] = 1
            else:
                mydict[sound][wordkey] += 1

    newdict = dict()

    for key, value in mydict.items():
        n = max(value.items(), key=operator.itemgetter(1))[0]
        newdict[key] = n
    
    return newdict.values()

def readFileAsDict(direc):
    dictionary = dict()
    with open(direc) as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1].split(' ')
            dictionary[line[0]] = line[1]
    return dictionary

