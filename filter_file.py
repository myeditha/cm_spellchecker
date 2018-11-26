from DataManagement import indicLangIdentifier
from DataManagement import dumbFilterCollection

import codecs
# from docopt import docopt
import os
from os import path
import argparse

def filter_codemixed_text(source_file, lang_list, do_lang=False):
    '''
    :param source_file: file containing tweets
    :param lang_list: list of languages with which to condition the language identifier
    :return: text cleaned from #tags, RT, transliterated and language-tagged
    '''
    dumbFilter = dumbFilterCollection()

    # loads a language identifier
    lid_tool = None
    if do_lang:
        lid_tool = indicLangIdentifier(lang_list)

    head, inpFileName = os.path.split(source_file)
    fileName, ext = inpFileName.split(".")
    outFile = fileName + "_filtered"
    outFile = os.path.join(head, outFile + "." + ext)

    with codecs.open(source_file, 'r', encoding='utf-8') as f_src,\
            codecs.open(outFile, 'w', encoding='utf-8') as fw:
            for line in f_src:
                # 1. Apply basic filtering
                filtered_line = dumbFilter.filterLine(line)
                if not lid_tool is None:
                    lids = lid_tool.detectLanguageInSentence(line)
                    # 2. Zip together the Language Tag and the words
                    filtered_line = " ".join([x+'\\'+y for x,y in zip(filtered_line.split(),lids)])
                    print("Line observed:{}".format(filtered_line))

                fw.write(filtered_line)

    return outFile

if __name__== "__main__":
    parser = argparse.ArgumentParser(description='filter out weird punctutations, retweets, hashtags, urls etc. and optionally language tag ')
    parser.add_argument('source_file',type=str, help='file to be cleaned')
    parser.add_argument('lang_pair', type=str, help='comma separated tuple of languages in file')
    parser.add_argument('--do_lang',dest='do_lang', action='store_true', help='set to True if you also wish to language tag.')

    args = parser.parse_args()

    source_file = args.source_file
    major_lang, mixed_lang = args.lang_pair.strip().split(",")

    filter_codemixed_text(source_file, [major_lang, mixed_lang], args.do_lang)