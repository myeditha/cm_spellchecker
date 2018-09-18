import fuzzy
import enchant
from read_data import makeEnglishDict

# This is for initial commits and organization. This will be refactored.

class Spellchecker(): 

    def __init__(self):
        self.soundex = fuzzy.Soundex(4)
        self.en = enchant.Dict('en-us')

    def __levenshtein(self,word1, word2):
        v0 = [0] * (len(word2)+1)
        v1 = [0] * (len(word2)+1)

        for i in range(0,len(word2)+1):
            v0[i] = i;

        for i in range(0,len(word1)): 
            v1[0] = i + 1

            for j in range(0,len(word2)):
                cost = 0
                if(word1[i]==word2[j]):
                    cost = 0
                else:
                    cost = 1
                v1[j + 1] = min([v1[j] + 1, v0[j + 1] + 1, v0[j] + cost])
        
            for j in range(0,len(v0)):
                v0[j] = v1[j]

        return v1[len(word2)]

    # Method 1 of spell-checking: levenshtein

    def calcLevenshteinDist(self,word1,word2):
        return self.__levenshtein(word1,word2)

    def levenshteinEditSuggestion(self,word1):
        # The naive implementation - using levenshtein distance to 
        # compare to every word in dictionary

        dictionary = makeEnglishDict()
        minDist = len(word1) + 1
        minWord = word1
        for word2 in dictionary:
            dist = self.__levenshtein(word1,word2)
            if(dist<minDist or (dist==minDist and len(word1)==len(word2))):
                minDist = dist
                minWord = word2
        return minWord.rstrip()   
        
    
