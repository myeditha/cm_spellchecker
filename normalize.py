# -*- coding: utf-8 -*-
"""
Usage:
    main.py --source-file=<file> --lang-set=<string>


Options:
    -h --help                               show this screen.

    --source-file=<file>                    source file to cleanse
                                            [default:  'file.txt']
    --lang-set=<string>                     list of languages in the corpus
                                            [default: ['eng','hin']]
    --lang-file=<file>                      language annotated file
                                            [default:  'file.txt']
    --aggressiveness=<float>                aggressiveness of cleaning
                                            [default: 1.0]
"""

from DataManagement import indicLangIdentifier, polyglot_SpellChecker
from DataManagement import dumbFilterCollection
from spellcheck import Spellchecker
import codecs
# from docopt import docopt
import os
from os import path
import argparse

spellcheckPath = os.path.abspath(os.path.join(os.path.dirname(__file__),"spellcheck"))
datapath = os.path.join(spellcheckPath,"data")
hinDictPath = os.path.join(datapath,"hindi_trans.txt")

def normalize_codemixed_text(source_file, language_file, lang_list, to_pickle=False):
    '''
    :param source_file: file containing tweets
    :param lang_list: list of languages with which to condition the language identifier
    :return: text cleaned from #tags, RT, transliterated and spell-corrrected
    '''
    dumbFilter = dumbFilterCollection()

    # loads a language identifier
    lid = indicLangIdentifier(lang_list)

    head, inpFileName = os.path.split(source_file)
    fileName, ext = inpFileName.split(".")
    outFile = fileName + "_filtered"
    outFile = os.path.join(head, outFile + "." + ext)

    major_lang = lang_list[0] # TODO: For now this is english but could be french. Adapt the constructors accordingly.
    mixed_lang = lang_list[1]
    repkl_Major = repkl_Alt = to_pickle

    spellChecker = Spellchecker(langTag=mixed_lang,repklEng=repkl_Major, repklAlt=repkl_Alt,aggressiveness=1, outputType="firstOf", altPath=None,
                                dictDoc=hinDictPath)

    # if the lines within this file are already language annotated
    isLangTagged = True

    with codecs.open(source_file, 'r', encoding='utf-8') as f_src,\
            codecs.open(language_file, 'r', encoding='utf-8') as f_lang:
        with codecs.open(outFile, 'w', encoding='utf-8') as fw:
            for line,lids in zip(f_src, f_lang):
                # 1. Apply basic filtering
                line = dumbFilter.filterLine(line)
                line = line.split()
                lids = lids.split()
                # 2. Zip together the Language Tag and the words

                lang_tagged_line = " ".join([x+'\\'+y for x,y in zip(line,lids)])
                print("Line observed:{}".format(lang_tagged_line))

                # spell_corrected_line = " ".join(words)
                spell_corrected_line = spellChecker.correctSentence(lang_tagged_line)
                fw.write(spell_corrected_line)
                # # 3. Transliterate each word to their language specific script
                # translit_words = []
                #
                # for word, lang in zip(spell_corrected_line.split(" "), lid_tags):
                #     translit_words.append(indic_transliterator(word, "english", lang))
                #
                # fw.write(" ".join(translit_words))

    return outFile

# TODO Features:
# 1. Create the pickle files as part of setup.py and save it as a constant. Same with dict file.

if __name__== "__main__":
    parser = argparse.ArgumentParser(description='Code-mixed spellchecking')
    parser.add_argument('source_file',type=str, help='file with code-mixed content, separated by newlines.')
    parser.add_argument('lang_file',type=str, help='file containing the language tags for each word per sentence.')
    parser.add_argument('lang_pair', type=str, help='comma separated tuple of major_lang,mixed_lang')

    parser.add_argument('--do_repickle',dest='do_repickle', action='store_true', help='set to True for first time use with a language or '
                                                                                   'if you have modified the dictionary for your language.')
    args = parser.parse_args()

    source_file = args.source_file
    language_file = args.lang_file
    major_lang, mixed_lang = args.lang_pair.strip().split(",")

    normalize_codemixed_text(source_file, language_file, [major_lang, mixed_lang], args.do_repickle)