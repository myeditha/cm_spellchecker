def __readFilesAsList(dir):
    dictionary = []
    with open(dir) as f:
        dictionary = f.readlines()
    return dictionary

def __retrieveDictionary(addr):
    return __readFilesAsList(addr)

def makeEnglishDict(addr = "../lib/DICT.txt"):
    return __retrieveDictionary(addr)

