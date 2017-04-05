#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import urllib.request
import sys
import os

class myContentHandler(ContentHandler):
    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.link = ""
        self.title = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem: #dentro de <item> vemos si encontramos <title> o <link>
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item': #etiqueta de cierre </...>
            self.inItem = False
        elif self.inItem: #tengo contenido que me interesa
            if name == 'title': #si lo que se cierra es title
                self.title = "Title: " + self.theContent + "."
                # To avoid Unicode trouble
                afile = open(sys.argv[2], "a")
                afile.write(self.title)
                print (self.title)
                self.inContent = False  #he terminado de leer una etiqueta y lo reinicializo
                self.theContent = ""
                self.title= ""
            elif name == 'link': #si lo que se cierra es link
                self.link = "<p>Link: <a href='" + self.theContent + "'>" + self.theContent + "</a></p>"
                afile = open(sys.argv[2], "a")
                afile.write(self.link + "\n")
                print (self.link)
                self.inContent = False  #he terminado de leer una etiqueta y lo reinicializo
                self.theContent = ""
                self.link = ""

    def characters (self, chars):  #si tenemos contenido, lo guardamos
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog
if len(sys.argv)<3:
    print ("Usage: python xml-parser-barrapunto.py <document.rss> <document.html>")
    print ()
    print (" <document.rss>: file name of the document to save the xml code")
    print (" <document.html>: file name of the HTML document to save the output(titles & links)")
    sys.exit(1)

# creamos un fichero con la pagina barrapunto actual
afile = open(sys.argv[1], "w")
url = "http://barrapunto.com/barrapunto.rss"
f = urllib.request.urlopen(url)
body = f.read().decode('utf-8')
afile.write(body)
afile.close()
# comprobamos que existe fichero html que nos pasan para que con append no repitamos lo que guardamos en distintas ejecuciones y borramos
if os.path.exists(sys.argv[2]):
    os.remove(sys.argv[2])
# Load parser and driver
theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

xmlFile = open(sys.argv[1],"r")
theParser.parse(xmlFile)
