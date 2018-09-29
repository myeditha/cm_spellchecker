from bs4 import BeautifulSoup
import urllib.request
import ssl
from indictrans import Transliterator

def scrape_telugu():
    trn = Transliterator(source='tel', target='eng', build_lookup=True)
    context = ssl._create_unverified_context()
    link = "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Telugu/"
    optlist = ["1-1000", "1001-2000", "2001-3000", "3001-4000", "4001-5000", "5001-6000", "6001-7000", "7001-8000", "8001-9000", "9001-10000"]
    aggr = []
    for opt in optlist:
        request = urllib.request.Request(link + opt)
        soupt = BeautifulSoup(urllib.request.urlopen(request, context=context), 'html.parser')
        classes = soupt.find_all("div", class_="mw-parser-output")[0].find_all("li")
        for cclass in classes:
            aref = cclass("a")
            if aref:
                aggr.append((aref[0].string, trn.transform(aref[0].string)))
                
    return aggr


def scrape_hindi():
    context = ssl._create_unverified_context()
    link = "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Hindi_1900"
    request = urllib.request.Request(link)
    souph = BeautifulSoup(urllib.request.urlopen(request, context=context), 'html.parser')
    classes = souph.find_all("div", class_="mw-parser-output")[0].find_all("tbody")[0].find_all("tr")
    aggr = []
    for cclass in classes:
        aref = cclass("a")
        eref = cclass("span", class_ = "tr Latn")
        if aref:
            aggr.append((aref[0].string, eref[0].string))
    return aggr

def main():
    rawoutputfile_h = "../data/hindi_raw.txt"
    transoutputfile_h = "../data/hindi_trans.txt"
    rawoutputfile_t = "../data/telugu_raw.txt"
    transoutputfile_t = "../data/telugu_trans.txt"

    res1 = scrape_hindi()

    with open(rawoutputfile_h, "w") as f :
        f.write("\n".join([x[0] for x in res1]))
    with open(transoutputfile_h, "w") as f:
        f.write("\n".join([x[1] for x in res1]))

    res2 = scrape_telugu()

    with open(rawoutputfile_t, "w") as f :
        f.write("\n".join([x[0] for x in res2]))
    with open(transoutputfile_t, "w") as f:
        f.write("\n".join([x[1] for x in res2]))


main()

