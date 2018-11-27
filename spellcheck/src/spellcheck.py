import metaphone
import pybktree
from .read_data import *
from symspellpy.symspellpy import SymSpell, Verbosity

# This is for initial commits and organization. This will be refactored.

bktreepath = os.path.join(datapath,"bktree.pkl")
engdictpath = os.path.join(datapath,"DICT.txt")

class Spellchecker(): 

    def __init__(self, mixedLang, majorLang="eng", repklEng=False, repklAlt=False, aggressiveness=1, outputType="firstOf", altPath=None, freqDocMajor=os.path.join(datapath,"freqdict.txt"), dictDocMixed=None):
        spellcheckpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        datapath = os.path.join(spellcheckpath,"data")
        # engbktreepath = os.path.join(datapath,"engbktree.pkl")
        altbktreepath = os.path.join(datapath, mixedLang + "bktree.pkl")
        self.mixedLang = mixedLang
        self.majorLang = majorLang
        self.dmeta = metaphone.dm
        # self.dictionary = makeBkTreeFromPkl(self.calcLevenshteinDist, "eng", engdictpath, engbktreepath, repklEng)
        if(dictDocMixed):
            self.altdictionary = makeBkTreeFromPkl(self.calcLevenshteinDist, mixedLang, dictDocMixed, altbktreepath, repklAlt)
        self.dictionary = getSymspellDict(freqDocMajor)
        # if(dictDoc):
        #     self.altdictionary = getSymspellDict(dictDoc)
        self.metaphones = makeMetaDict(dictDocMixed)

    def correctSentence(self, sentence):
        wordarr = sentence.split(" ")
        newsentence = []
        for word in wordarr:
            wordplustag = word.split("\\")
            myword = wordplustag[0]
            isUpper = myword[0].isupper()
            tag = wordplustag[1]
            newword = myword
            if tag==self.majorLang:
                newword = self.levenshteinEditSuggestionCapSym(myword, 1)[0].term
            elif tag!="O":
                # print(myword)
                if(len(myword) < 4):
                    suggestions = self.levenshteinEditSuggestionCap(myword, 2, False)
                    # print(suggestions)
                    if(suggestions):
                        newword = suggestions[0][1]
                    # print(newword)
                else:
                    newword = self.getMetaphone(myword)

            if(isUpper):
                newword = newword[0].upper() + newword[1:]

            newsentence.append(newword)
        return ' '.join(newsentence)

    def __levenshtein(self,word1,word2):
        if len(word1) < len(word2):
            return self.__levenshtein(word2, word1)

        v0 = [0] * (len(word2)+1)
        v1 = [0] * (len(word2)+1)

        for i in range(0,len(word2)+1):
            v0[i] = i

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

    # Method 1 of spell-checking: levenshtein

    def calcLevenshteinDist(self,word1,word2):
        return self.__levenshtein(word1,word2)

    def getMetaphone(self, word):
        sound = self.dmeta(word)
        if sound in self.metaphones:
            return self.metaphones[sound]
        else:
            return word
        

    def levenshteinEditSuggestion(self,word1):
        # The naive implementation - using levenshtein distance to
        # compare to every word in dictionary

        dictionary = makeEnglishDict(os.path.join(datapath,"DICT.txt"))
        minDist = len(word1) + 1
        minWords = []

        for word2 in dictionary:
            word2 = word2.strip()
            dist = self.__levenshtein(word1,word2)
            if dist<minDist :
                minWords = [word2]
                minDist = dist
            elif dist==minDist :
                minWords.append(word2)

        return minWords

    def levenshteinEditSuggestionCapSym(self,word1,cap,isEng=True):
        # The symspell-based suggestion function
        if not isEng:
            distances = list(self.altdictionary.lookup(word1, Verbosity.CLOSEST, cap))
        else:
            distances = list(self.dictionary.lookup(word1, Verbosity.CLOSEST, cap))

        return distances

    def levenshteinEditSuggestionCap(self,word1,cap,isEng=True):
        # The bktree-based suggestion function
        if not isEng:
            distances = self.altdictionary.find(word1, cap)
        else:
            distances = self.dictionary.find(word1,cap)

        return distances
        
    
