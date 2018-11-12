# -*- coding: utf-8 -*-
import re, string, unicodedata
import os
import codecs

from .constants import URL_REGEX, MENTION_REGEX, REPEAT_3_OR_MORE, REPEAT_STR_3_OR_MORE
from bs4 import BeautifulSoup

class filterCollection(object):
    def __init__(self):
        self.filters = []

    def filterFile(self,inpFile,outFileName):
        return NotImplementedError

    def filterLine(self,line):
        return  NotImplementedError

class dumbFilterCollection(filterCollection):
    def __init__(self):
        super().__init__()
        self.filters = [self.replaceUrl, self.replaceMention,
                        self.correctRepeatChars, self.correctRepeatStr, self.strip_unicode_punctuations]

    # some custom filters I was trying out.
    def stripHtml(self, text):
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    def replaceUrl(self, text):
        text = re.sub(URL_REGEX, "<URL>", text)
        return text

    def replaceMention(self, text):
        text = re.sub(MENTION_REGEX, "<USR>", text)
        return text

    def correctRepeatChars(self, text):
        text = re.sub(REPEAT_3_OR_MORE, r"\1", text)
        return text

    def strip_unicode_punctuations(self, text):
        clean_text = []
        for word in text.split():
          clean_text.append("".join(char for char in word if not unicodedata.category(char).startswith('P')))
        return " ".join(clean_text)

    def correctRepeatStr(self, text):
        text = re.sub(REPEAT_STR_3_OR_MORE, r"\1", text)
        return text

    def filterFile(self, inpPtr, outPtr):
        for line in inpPtr.readlines():
            for filter in self.filters:
                line = filter(line)
            outPtr.write(line)

    def filterLine(self, line):
        for filter in self.filters:
            line = filter(line)
        return line


