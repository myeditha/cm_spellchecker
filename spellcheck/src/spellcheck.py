import metaphone
import pybktree
from .read_data import *

# This is for initial commits and organization. This will be refactored.
spellcheckpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
datapath = os.path.join(spellcheckpath,"data")
bktreepath = os.path.join(datapath,"bktree.pkl")
dictpath = os.path.join(datapath,"DICT.txt")

class Spellchecker(): 

    def __init__(self, repklEng=bktreepath, aggressiveness=1, outputType="firstOf", altPath=None):
        self.dmeta = metaphone.dm
        self.en = makeEnglishDict()
        self.dictionary = makeBkTreeFromPkl(self.calcLevenshteinDist, repklEng)
        self.altdictionary = makeBkTreeFromPkl(self.calcLevenshteinDist, repklEng)
        self.metaphones = makeMetaDict(os.path.join(datapath,"telugu3rawaug.txt"))

    def correctSentence(self, sentence):
        wordarr = sentence.split(" ")
        newsentence = []
        for word in wordarr:
            wordplustag = word.split("\\")
            myword = wordplustag[0]
            tag = wordplustag[1]
            if tag=="English":
                newword = self.levenshteinEditSuggestionCap(myword, 1)[0][1]
            else:
                newword = self.getMetaphone(myword)
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

        dictionary = makeEnglishDict()
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


    def levenshteinEditSuggestionCap(self,word1,cap):
        # The bktree-based suggestion function

        distances = self.dictionary.find(word1,cap)

        return distances
        
    
