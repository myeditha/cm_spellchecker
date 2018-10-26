from .read_data import *
import metaphone
import enchant

class Tagger():
    def __init__(self):
        self.dmeta = metaphone.dm
        self.en = enchant.Dict('en-us')
        self.metaphones = makeMetaDict("spellcheck/data/telugu2rawaug.txt")

    
