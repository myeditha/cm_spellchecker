from .read_data import *
import metaphone

class Tagger():
    def __init__(self):
        self.dmeta = metaphone.dm
        self.en = makeEnglishDict("spellcheck/data/DICT.txt")
        self.metaphones = makeMetaDict("spellcheck/data/telugu2rawaug.txt")
    