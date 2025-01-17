# -*- coding: utf-8 -*-
import re
from DataManagement.constants import ANNOT_REGEX, LITCM_CODE_TO_UNIV_CODE
import codecs
import os
import json
# from indic_transliteration import sanscript
# from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

__language_map__ = {}

def load_lexicon(languageObject):
    word2Idx = {}
    idx2Word = {}
    stopWordIds = []
    vocab_path = getattr(languageObject, 'vocab_path', None)
    if not vocab_path is None and os.path.exists(vocab_path):
        with codecs.open(vocab_path, 'r', 'utf-8') as fp:
            lexicon = fp.read().split()
        stopWords = []
        stop_word_path = getattr(languageObject, 'stop_word_path', None)
        if not stop_word_path is None and os.path.exists(stop_word_path):
            with codecs.open(stop_word_path, 'r', 'utf-8') as fp:
                stopWords = fp.read().split()

        for word in lexicon:
            if not word in word2Idx.keys():
                lastDictPosn = len(word2Idx.keys()) - 1
                word2Idx[word] = lastDictPosn + 1
                idx2Word[lastDictPosn + 1] = word
                if word in stopWords:
                    stopWordIds.append(lastDictPosn + 1)
    setattr(languageObject, 'word2Idx', word2Idx)
    setattr(languageObject, 'idx2Word', idx2Word)
    setattr(languageObject, 'stopWordIds', stopWordIds)


def languageLoader(languageConfigFile):
    with open(languageConfigFile) as json_data:
        languages = json.load(json_data)
        for langJSON in languages["languageObjects"]:
            # create a new language type from each of these JSONs
            langName, langProperties = next(iter(langJSON.keys())), dict(next(iter(langJSON.values())))
            # dynamically created language object
            langObject = type(langName, (object,), langProperties)
            __language_map__[langName] = langObject

# def indic_transliterator(text, src_lang, tgt_lang):
#     indic_transliterator_lang_codes = {"english":sanscript.ITRANS,
#                                        "hindi":sanscript.DEVANAGARI,
#                                        "telugu":sanscript.TELUGU,
#                                        "bengali":sanscript.BENGALI,
#                                        "gujarati":sanscript.GUJARATI,
#                                        "gurumukhi":sanscript.GURMUKHI,
#                                        "kannada":sanscript.KANNADA,
#                                        "malayalam":sanscript.MALAYALAM,
#                                        "tamil":sanscript.TAMIL
#                                        }
#     if not src_lang in indic_transliterator_lang_codes.keys() or \
#             not tgt_lang in indic_transliterator_lang_codes.keys():
#         raise KeyError("Unknown language code. Got source:'{}',target:'{}' ".format(src_lang,tgt_lang))
#     return transliterate(text, indic_transliterator_lang_codes[src_lang], indic_transliterator_lang_codes[tgt_lang])

class languageIdentifier(object):
    def __init__(self, languageSet):
        self.langSet = languageSet

    def detectLanguageInSentence(self, sentence):
        return NotImplementedError

    def detectLanguageInWord(self, word):
        return NotImplementedError

class indicLangIdentifier(languageIdentifier):
    def __init__(self,languageSet):
        super().__init__(languageSet)

    def detectLanguageInWord(self, word):
        return self.langSet[1]

def polyglot_SpellChecker(languageAnnotated_Text):
    correctedWords = []
    for wordLangPair in languageAnnotated_Text.split():
        word, lang = wordLangPair.split('\\')
        # if this word is an annotation tag or isn't in the language map then don't spell check
        if not re.search(ANNOT_REGEX, word) and lang.lower() in __language_map__.keys():
            langObject = __language_map__[lang.lower()]
        correctedWords.append(word + '\\' + lang)
    return " ".join(correctedWords)

# ****for testing****
# if __name__== "__main__":
#     languageLoader("./language-config.json")
#     print(__language_map__.keys(),__language_map__.values())


