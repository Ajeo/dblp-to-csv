#!/usr/bin/python

import xml.sax
import sys
import codecs
from unidecode import unidecode

class DBLPHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""
        self.title =  ""
        self.article = {'year':'', 'title':''}
        self.file = codecs.open("dblp.csv", "w", "iso-8859-1")

    def startElement(self, tag, attributes):
        self.CurrentData = tag

    def endElement(self, tag):
        if tag == "title":
            self.article['title'] = self.title
        if tag == "year":
            self.article['year'] = self.year

        if len(self.article['title']) > 0 and len(self.article['year']) > 0 and int(self.article['year']) >= 1936:
            data = unidecode(self.article['year'] + ',' + self.article['title'] + '\n')
            self.file.write(data)
            print data
            self.article['title'] = ""
            self.article['year'] = ""
        elif self.CurrentData == "dblp":
            self.file.close()
            sys.exit("stop")

    def characters(self, content):
        if self.CurrentData == "title":
            self.title = content.strip().rstrip('\n').replace('"','')
        elif self.CurrentData == "year":
            self.year = content.strip().rstrip('\n')

if ( __name__ == "__main__"):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = DBLPHandler()
    parser.setContentHandler(Handler)
    parser.parse("dblp.xml")
