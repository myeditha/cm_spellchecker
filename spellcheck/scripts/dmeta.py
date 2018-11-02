import json
import string
import metaphone
import re
import random
from ..src.spellcheck import *
from functools import reduce

def levenshtein(word1,word2):
    if len(word1) < len(word2):
        return levenshtein(word2, word1)

    v0 = [0] * (len(word2)+1)
    v1 = [0] * (len(word2)+1)

    for i in range(0,len(word2)+1):
        v0[i] = i;

    for i in range(0,len(word1)): 
        v1[0] = i + 1

        for j in range(0,len(word2)):

            deletioncost = v0[j+1] + 1
            insertioncost = v1[j] + 1
            substitutioncost = v0[j] + 1

            if(word1[i]==word2[j]):
                substitutioncost = v0[j]

            v1[j + 1] = min([deletioncost, insertioncost, substitutioncost])
    

        for j in range(0,len(v0)):
            v0[j] = v1[j]

    return v1[len(word2)]

def main2():
    spellchecker = Spellchecker(False, 1, "f", "")
    dmeta = metaphone.dm
    with open("spellcheck/data/teluguraw.txt", "r") as f:
        lines = f.readlines()
        newlines = []
        counter = 0
        for line in lines:
            line = line.strip()
            if((len(line) < 4 or len(spellchecker.levenshteinEditSuggestionCap(line,1))==0) and ("_" not in line)):
                newlines.append(line)
            counter+=1
            if(counter % 500==0):
                print("On line " + str(counter))

        newnewlines = list(map(lambda x: str(dmeta(x)[0]) + " " + x, newlines))
        with open("spellcheck/data/telugu3rawaug.txt", "w") as f:
            f.write("\n".join(newnewlines))
