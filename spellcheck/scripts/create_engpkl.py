import pybktree
import pickle

def __readFilesAsList(direc):
    dictionary = []
    with open(direc) as f:
        dictionary = f.readlines()
    return dictionary

def makeBkTree(func, addr = "../data/DICT.txt"):
    return pybktree.BKTree(func, __readFilesAsList(addr))

def levenshtein(word1,word2):
    if len(word1) < len(word2):
        return levenshtein(word2, word1)

    v0 = [0] * (len(word2)+1)
    v1 = [0] * (len(word2)+1)

    for i in range(0,len(word2)+1):
        v0[i] = i;

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

def main():
    print("making tree")
    bktree = makeBkTree(levenshtein)
    print("creating pickle object")
    with open("../data/bktree.pkl", "wb") as f:
        pickle.dump(bktree, f)

main()