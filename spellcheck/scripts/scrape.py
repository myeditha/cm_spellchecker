# from bs4 import BeautifulSoup
import urllib.request
import ssl
# from indictrans import Transliterator

def get_soup(link):
    context = ssl._create_unverified_context()
    request = urllib.request.Request(link)
    return BeautifulSoup(urllib.request.urlopen(request, context=context), 'html.parser')

def scrape_telugu():
    trn = Transliterator(source='tel', target='eng', build_lookup=True)
    link = "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Telugu/"
    optlist = ["1-1000", "1001-2000", "2001-3000", "3001-4000", "4001-5000", "5001-6000", "6001-7000", "7001-8000", "8001-9000", "9001-10000"]
    aggr = []
    for opt in optlist:
        soupt = get_soup(link + opt)
        classes = soupt.find_all("div", class_="mw-parser-output")[0].find_all("li")
        for cclass in classes:
            aref = cclass("a")
            if aref:
                aggr.append((aref[0].string, trn.transform(aref[0].string)))
                
    return aggr


def scrape_hindi():
    link = "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Hindi_1900"
    souph = get_soup(link)
    classes = souph.find_all("div", class_="mw-parser-output")[0].find_all("tbody")[0].find_all("tr")
    aggr = []
    for cclass in classes:
        aref = cclass("a")
        eref = cclass("span", class_ = "tr Latn")
        if aref:
            aggr.append((aref[0].string, eref[0].string))
    return aggr

def scrape_social_media():
    link = "https://www.webopedia.com/quick_ref/textmessageabbreviations.asp"
    soup = get_soup(link)
    allterms = soup.find_all("tbody")[0].find_all("tr")
    aggr = []
    for term in allterms:
        aref = term.find_all("td", class_=lambda x: "style4" not in str(x))
        if aref and aref[0] and aref[0].string:
            print(aref[0].string.lower())
            aggr.append(aref[0].string.lower())
    return aggr

def main():
    rawoutputfile_h = "../data/hindi_raw.txt"
    transoutputfile_h = "../data/hindi_trans.txt"
    rawoutputfile_t = "../data/telugu_raw.txt"
    transoutputfile_t = "../data/telugu_trans.txt"
    rawoutputfile_s = "../data/social_raw.txt"


    res = scrape_social_media()

    with open(rawoutputfile_s, "w") as f:
        f.write("\n".join(res))

    # res1 = scrape_hindi()

    # with open(rawoutputfile_h, "w") as f :
    #     f.write("\n".join([x[0] for x in res1]))
    # with open(transoutputfile_h, "w") as f:
    #     f.write("\n".join([x[1] for x in res1]))

    # res2 = scrape_telugu()

    # with open(rawoutputfile_t, "w") as f :
    #     f.write("\n".join([x[0] for x in res2]))
    # with open(transoutputfile_t, "w") as f:
    #     f.write("\n".join([x[1] for x in res2]))


main()

