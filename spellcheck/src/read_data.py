def __readFilesAsList(direc):
    dictionary = []
    with open(direc) as f:
        dictionary = f.readlines()
    return dictionary

def __retrieveDictionary(addr):
    return __readFilesAsList(addr)

def makeEnglishDict(addr = "spellcheck/data/DICT.txt"):
    return __retrieveDictionary(addr)

