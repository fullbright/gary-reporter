#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import division
import feedparser, os
from BeautifulSoup import BeautifulSoup
import nltk, re, pprint
from nltk import word_tokenize
# from urllib2 import Request as request
import urllib2

def ie_preprocess(document):
	sentences = nltk.sent_tokenize(document)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]

	return sentences

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path+"/../bible_fulltext/Bible_French_djvu_Genesis.txt") as file:
	sentences = ie_preprocess(file.read().decode('utf8'))

	cp = nltk.RegexpParser('CHUNK: {<V.*> <TO> <V.*>}')
	for sent in sentences:
		#print sent
		tree = cp.parse(sent)
		for subtree in tree.subtrees():
			if subtree.label() == 'CHUNK': print (subtree)
