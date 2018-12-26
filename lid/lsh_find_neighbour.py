#coding: utf-8

from datasketch import MinHash, MinHashLSH
import cPickle
from nltk import ngrams
import pickle
from nltk.metrics import edit_distance
import time
import sqlite3
from indictrans import Transliterator
from libindic.soundex import Soundex



def start_lsh():

	create = True 
	sqlite_file = "/home/hkesavam/new_lid/code/gen_data/db_lid"
	conn = sqlite3.connect(sqlite_file)
	cur = conn.cursor()
	data = cur.execute("select distinct(soundex) from dev_table where count > 5")
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
		      print "Enterin continue"
		      continue
		  lsh.insert(c, minhash)
		  minhashes[c] = minhash
		print len(data)
		print("Dumping")
		#cPickle.dump(new_data, open("data", "wb"), -1)
		cPickle.dump(lsh, open("/home/hkesavam/new_lid/code/gen_data/lsh_model", "wb"), -1)
		print "Finished dumping"

	if not(create):
		data = cPickle.load( open("/home/hkesavam/new_lid/code/gen_data/data", "rb"))
		lsh = cPickle.load( open("/home/hkesavam/new_lid/code/gen_data/lsh_model", "rb"))
	hin_soundex_inst = Soundex()
	hin_trans = Transliterator(source='eng', target='hin', build_lookup=True)
	return cur, data, lsh, hin_soundex_inst, hin_trans



def find_hin_neighbour(inpword, c, data, lsh, hin_soundex_inst, hin_trans):
	word = hin_trans.transform(inpword)
	return word
	word = hin_soundex_inst.soundex(word)
	minhash = MinHash(num_perm=32)
	test_i = word
	for d in word:
	    d = d.encode("utf-8")
	    minhash.update(d)

	results = lsh.query(minhash)
	indx = -1
	min_res = 999
	for i in results:
		res = edit_distance(data[i][0], test_i)
		if min_res>res:
			indx = i
			min_res = res 
		if min_res == 0:
			break
	if indx == -1:
		return "npmatch"
	word = data[indx][0]
	count = c.execute("select max(count) from dev_table where soundex = '"+word+"'")
	a = list(count)
	dev_word = c.execute("select dev from dev_table where soundex = '"+word+"' AND count = %d"%a[0][0])
	return list(dev_word)[0][0]

if __name__ == "__main__":
	hin_cur, hin_data, hin_lsh, hin_soundex_inst, hin_trans = start_lsh()
	word = u"kare"
	print find_hin_neighbour(word, hin_cur, hin_data, hin_lsh, hin_soundex_inst, hin_trans)
