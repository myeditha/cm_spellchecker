from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
import sys
import pickle
import numpy as np
from collections import defaultdict
import harini as hmm
from prob_h import LaplaceProbDist
# from lsh_find_neighbour import start_lsh as start_hin_lsh
# from lsh_find_neighbour import find_hin_neighbour
from eng_lsh_find_neighbour import start_eng_lsh, find_eng_neighbour


def lang_model():
    classes = ["PP", "EP", "PE", 'HE', "EH", "HH", "EE", "HP", "PH"]
    counter_ex = 0
    train_data = [[("Aapka*name", "HE"), ("name*kya", "EH"), ("Kya*hai", "HH"), ("hai*?", "HP")]]
    train_dict = defaultdict(int)
    with open("hmm_trial_to_2") as fin:
        for j,line in enumerate(fin):
            count = 0
            line = line.strip("\n")
            words = line.strip().split(" ")
            for i,word in enumerate(words):
                pair = word.split("***")
#print pair
                if (count==0):
                        #if pair[1] in states_list:
                    try:
                        if pair[1] in classes:
                            train_data.append([(pair[0],pair[1])])
                            count = 1
                    except:
                        counter_ex+= 1
                else:
#                               print "Pair",pair[0],pair[1]
                        #if pair[1] in states_list:
                    try:
                      if pair[1] in classes:
                                                train_data[j].append((pair[0],pair[1]))
                    except:
                        counter_ex+= 1
                              #train_dict[pair[0]] += 1

    trainer = hmm.HiddenMarkovModelTrainer()
    tagger = trainer.train_supervised(train_data, estimator = LaplaceProbDist)
    print("HMM ex", counter_ex)
    return tagger


def lang_model_prob(tagger, words):
    tags = tagger.tag(words)
    cond_prob =  tagger.point_prob(tags)
    word_dict = defaultdict(int)
    hdict = defaultdict(int)
    edict = defaultdict(int)
    pdict = defaultdict(int)
    for joint,jdict in cond_prob.iteritems():
#               print tag, type(tag)
        flag_0 = 0
        flag_1 = 0
        words = joint.split("*")
#               print words
        if word_dict[words[0]] != 0:
            flag_0 = 1
        else:
            word_dict[words[0]] = defaultdict(int)
        if word_dict[words[1]] != 0:
            flag_1 = 1
        else:
            word_dict[words[1]] = defaultdict(int)
            word_dict[words[0]]["H"] += jdict["HO"]+jdict["HH"]+jdict["HE"] 
            word_dict[words[0]]["E"] += jdict["EO"] + jdict["EE"] + jdict["EH"]
            word_dict[words[1]]["H"] += jdict["HH"] + jdict["OH"] + jdict["EH"]
            word_dict[words[1]]["E"] += jdict["EE"] + jdict["HE"] + jdict["OE"]
        if flag_0:
#                       print "before"
            word_dict[words[0]]["H"] /= 2
            word_dict[words[0]]["E"] /= 2
#                       print
        if flag_1:
            word_dict[words[1]]["H"] /= 2
            word_dict[words[1]]["E"] /= 2
        #print edict, hdict
    return word_dict 



def start_lid():
    tfidf_model = pickle.load(open("gen_data/"+"tfidf_model", "r"))
    mnb_model = pickle.load(open("gen_data/"+"mnb_model", "r"))
    cmu_dict = pickle.load(open("gen_data/"+"mod_cmu_dict", "r"))
    cmu_dict = defaultdict(int, cmu_dict)
    return tfidf_model, mnb_model, cmu_dict
    
    

def perform_lid(cmu_dict, tfidf_model, mnb_model, tagger, line, lang_prob_hin, lang_prob_eng):
    lang_prob_hin = 0.5
    lang_prob_eng = 0.5
    words = line.split()
    words = [word.lower() for word in words]
    nbwords = ["!"+word.lower()+"@" for word in words]
    test_vec = tfidf_model.transform(nbwords)
    output = (mnb_model.predict(test_vec))
    mnb_probs = mnb_model.predict_proba(test_vec)
    hmm_input = [words[i]+"*"+words[i+1] for i in range(0,len(words)-1)]
    hmm_probs = lang_model_prob(tagger, hmm_input)
    for (i,word) in enumerate(words):
        if cmu_dict[word]:
            output[i] = "C"
        else:
            hin_p = mnb_probs[i][1] * hmm_probs[word]["H"] /  lang_prob_hin
            eng_p = mnb_probs[i][0] * hmm_probs[word]["E"] / lang_prob_eng
#             hin_p = mnb_probs[i][1]
#             eng_p = mnb_probs[i][0]
#             print(mnb_probs[i][1], hmm_probs[word]["H"], hin_p, mnb_probs[i][0], hmm_probs[word]["E"] , eng_p,  word)
            if hin_p > eng_p:
                output[i] = "H"
            else:
                output[i] = "E"
    return zip(words, output)

if __name__ == "__main__":
    #fr = open("twit_in2.txt", "r")
    hinglishFileName = sys.argv[1]
    hinglishTaggedFileName = sys.argv[2]
    fr = open(hinglishFileName, "r")
    lang_fp = open(hinglishTaggedFileName, "w")
    lines = fr.readlines()

    print("Loading model")
    tfidf_model, mnb_model, cmu_dict = start_lid()
    #eng_cur, eng_data, eng_lsh, soundex_eng = start_eng_lsh()
    #hin_cur, hin_data, hin_lsh, hin_soundex_inst, hin_trans = start_hin_lsh()
    eng_cur, eng_data, eng_lsh = start_eng_lsh()
    tagger = lang_model()
    print("Performing lid")
    tot_hin = 918798
    tot_eng = 201520
    lang_prob_hin = tot_hin*1.0/(tot_hin+tot_eng)
    lang_prob_eng = 1 - lang_prob_hin
    for line in lines:
        try:
            results = perform_lid(cmu_dict, tfidf_model, mnb_model, tagger, line, lang_prob_hin, lang_prob_eng)
            for word,label in results:
                if label == "C":
                    label = 'O'
                    word  = word
                elif label == "E": 
                    label = 'Eng'
                    #word = find_eng_neighbour(word, eng_cur, eng_data, eng_lsh, soundex_eng)
                    word = word
                else:
                    label = 'Hin'
                    # word = find_hin_neighbour(word, hin_cur, hin_data, hin_lsh, hin_soundex_inst, hin_trans)
                    word = word.encode('utf-8')
                lang_fp.write(label+" ")
        except:
            print("some issue in perform lid")
            continue
        lang_fp.write("\n")
