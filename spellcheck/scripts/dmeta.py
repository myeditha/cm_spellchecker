import json
import string
import metaphone
import re
import random
from ..src.spellcheck import *
from functools import reduce

def main2():
    spellchecker = Spellchecker(False, 1, "f", "")
    dmeta = metaphone.dm
    with open("spellcheck/data/teluguraw.txt", "r") as f:
        lines = f.readlines()
        newlines = []
        counter = 0
        print("processing")
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
