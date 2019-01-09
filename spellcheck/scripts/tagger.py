#!/usr/bin/env python3
import json
import argparse
import string
import re

def cleanse(line):
    line = ' '.join([t for t in line.split() if not t.startswith('@')])
    # line = line.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
    line = s = re.sub('([.,!?()])', r' \1 ', line)
    line = ' '.join(map(lambda x: x.lower(), line.split()))
    return line

def checkformistakes(line, nline):
    incorrect = input("enter space-separated incorrect words")
    print("entering correction mode: enter \'skip\' to skip current word, and '\'end\' to exit correction mode")
    inclist = incorrect.split(" ")
    for inc in inclist:
        if inc in line:
            inp = input("Classify: " + inc + "\n")
            nline = map(lambda x: inc + "\\" + inp if x.split('\\')[0] == inc else x, nline)
        else:
            print("word not in line; skipping")
    
    sure = input("are you sure?\n")
    if(sure.lower()=='y' or sure.lower()=='yes'):
        return ' '.join(nline)
    else:
        checkformistakes(line, nline)

def grabclasses(line):
    nline = []
    for word in line.split():
        print("sentence: " + line)
        wclass = input('Classify: ' + word + '\n')
        nline.append(word + "\\" + wclass)
    print("sentence: " + nline)
    sure = input("are you sure?\n")
    if(sure.lower()=='y' or sure.lower()=='yes'):
        return ' '.join(nline)
    else:
        return checkformistakes(line, nline)



def main():

    parser = argparse.ArgumentParser(description='Andhra Friends scraping')
    parser.add_argument('file', default = None, type=str, help='Input file name')
    parser.add_argument('outfileplain', default = None, type=str, help='Name of output file of cleansed data')
    parser.add_argument('outfileclass', default = None, type=str, help='Name of output file of cleansed data augmented with classification')

    args = parser.parse_args()

    if(not args.file):
        print("must include filename")

    with open(args.file) as f:
        lines = f.readlines()
        jsons = map(lambda x: json.loads(x), lines)
        textlines = list(map(lambda x: x["content"], jsons))
        
        textlines = textlines[1:10]
        # need to tag each, pipe into separate files

        textlines = list(map(lambda x: cleanse(x), textlines))

        classification = list(map(lambda x: grabclasses(x), textlines))

        with open(args.outfileplain, 'w') as w:
            w.write('\n'.join(textlines))

        with open(args.outfileclass, 'w') as w:
            w.write('\n'.join(classification))    

main()