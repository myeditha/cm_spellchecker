import json
import metaphone
import re
import operator

def read_sm():
    print("loading social media corpus")
    worddict = set()
    with open("../data/social_raw.txt") as f:
        line = f.readline()[:-1]
        while line:
            print(repr(line))
            worddict.add(line)
            line = f.readline()[:-1]

    return worddict

def cleanse(stri, smwords, engdict):
    stri = stri.encode('utf-8')
    # textarr = [x.strip(string.punctuation) for x in stri.split()]
    regex = b"[\w']+"
    textarr = re.findall(regex, stri)
    words = []
    for word in textarr:
        word = word.lower()
        word2 = word.decode('utf-8')
        if word == b"" or b".com" in word or any(char.isdigit() for char in word2) or (word2 in smwords) or b"_" in word:
            continue
        isenglish = word2 in engdict
        if not isenglish:
            print(word2)
        words.append((word, isenglish))
    return words

def create_soundex_dict(nlines):
    dmeta = metaphone.dm
    mydict = dict()
    for word in nlines:
        try:
            word = word.decode('ascii', errors='ignore')
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
    return mydict

def cleanse_string(lines, smwords):
    mapped = []
    counter = 0
    engdict = dict()
    print("loading dictionary")
    with open("../data/DICT.txt") as f:
        mlines = f.readlines()
        for line in mlines:
            line = line[:-1].lower()
            engdict[line] = 1

    print("cleaning string")

    for x in lines:
        if(counter % 100 == 0):
            print("Preprocessing sentence " + str(counter))
        retval = cleanse(json.loads(x)["content"], smwords, engdict)
        # print(retval)
        mapped.extend(retval)
        counter+=1
    return mapped

def grab_max_lines(mydict):
    newdict = dict()
    for key, value in mydict.items():
        n = max(value.items(), key=operator.itemgetter(1))[0]
        newdict[key] = n
    return newdict

def main():
    filename = "../data/teluguraw.txt"
    nlines = []
    smwords = read_sm()
    with open("../data/outfile4.json") as f:
        print("reading file")
        lines = f.readlines()
        mapped = []
        mapped = cleanse_string(lines, smwords)
        # mapped = reduce(operator.add, mapped)
        # print(mapped)
        print("filtering...")
        nlines = map(lambda x: x[0], list(filter(lambda x: not x[1], mapped)))

        mydict = create_soundex_dict(nlines)
        newdict = grab_max_lines(mydict)
        nlines = newdict.values()

        with open(filename, 'w') as f:
            print(str(len(nlines)) + " words discovered")
            f.write("\n".join(list(nlines)))
        
        # with open(filename2, 'w') as f:
        #     f.write("\n").join(list(map(lambda x: UnicodeIndicTransliterator.transliterate(x,"eng","tel"), nlines)))

def filterOutMeta():
    newlines = []

    with open("../data/telugurawaug.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1].split(' ')
            newlines.append(line[1])
    
    with open("../data/teluguDict.txt", "w") as f:
        f.write("\n".join(list(newlines)))

main()  