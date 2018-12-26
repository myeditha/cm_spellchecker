#coding: utf-8

from datasketch import MinHash, MinHashLSH
import cPickle
from nltk import ngrams
import pickle
from nltk.metrics import edit_distance
import time
import sqlite3
#ignoring Soundex because not doing english nearest neighbor search
#from libindic.soundex import Soundex

GEN_DATA = "gen_data/"

def start_eng_lsh():
	create = True 
	sqlite_file = GEN_DATA + "lid_db"
	conn = sqlite3.connect(sqlite_file)
	cur = conn.cursor()
	data = cur.execute("select distinct(soundex) from eng_table")
	data = list(data)

	#soundex_dict = pickle.load(open("/home/hkesavam/new_lid/code/gen_data/data_dev/dev_to_soundex.pkl", "r"))
	#data =  soundex_dict.keys()
	#data = ["e16512", "e16532", "hello", "hell"]
	lsh = MinHashLSH(threshold=0.5, num_perm=32)# Create MinHash objects
	minhashes = {}
	tot_wr_count = 0
	if create:
		for c, i in enumerate(data):
		  minhash = MinHash(num_perm=32)
		  for d in i[0]:
		    try:
		      d = d.encode("utf-8")
		      minhash.update(d)
		    except:
		      print("Exception computing minhash. Continue...")
		      continue
		  lsh.insert(c, minhash)
		  minhashes[c] = minhash
		print(len(data))
		print("Dumping lsh model")
		#cPickle.dump(new_data, open("data", "wb"), -1)
		cPickle.dump(lsh, open(GEN_DATA + "lsh_model", "wb"), -1)
		print("Finished dumping")

	if not(create):
		data = cPickle.load(open(GEN_DATA + "data", "rb"))
		lsh = cPickle.load(open(GEN_DATA + "lsh_model", "rb"))
	#soundex_inst = Soundex()
	return cur, data, lsh #, soundex_inst



def find_eng_neighbour(inpword, c, data, lsh, soundex_eng):
	minhash = MinHash(num_perm=32)
	word = soundex_eng.soundex(inpword)
	test_i = word
	for d in word:
	    d = d.encode("utf-8")
	    minhash.update(d)

	results = lsh.query(minhash)
	min_res = 999
	indx = -1
	for i in results:
		res = edit_distance(data[i][0], test_i)
		if min_res>res:
			indx = i
			min_res = res 
		if min_res == 0:
			break
	if indx == -1:
		return "nomatch"
	word = data[indx][0]
	#count = c.execute("select max(count) from dev_table where soundex = '"+word+"'")
	#a = list(count)
	dev_word = c.execute("select eng from eng_table where soundex = '"+word+"'") 
	dev_word = list(dev_word)
	min_res = 999
	for word in dev_word:
		word = word[0]
		res = edit_distance(word, inpword)
		if min_res>res:
                        final_word = word
                        min_res = res
	return final_word

# if __name__ == "__main__":
# 	eng_cur, eng_data, eng_lsh, soundex_eng = start_eng_lsh()
# 	word = "pursunt"
# 	find_eng_neighbour(word, eng_cur, eng_data, eng_lsh, soundex_eng)
