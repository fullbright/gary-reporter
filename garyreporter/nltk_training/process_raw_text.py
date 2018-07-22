from __future__ import division
import feedparser, os
from BeautifulSoup import BeautifulSoup
import nltk, re, pprint
from nltk import word_tokenize
# from urllib2 import Request as request
import urllib2

def process_rawtext():
	# Process gutemberg text 2554
	url = "http://www.gutenberg.org/files/2554/2554-0.txt"


	response = urllib2.urlopen(urllib2.Request(url))
	# response = request.urlopen(url)
	raw = response.read().decode('utf8')
	type(raw)

	print "Length of the corpus is : ", len(raw)
	print "Here are the 75 first characters : ", raw[:75]


	# tockenization
	tokens = word_tokenize(raw)
	print "Here are the type of tokens", type(tokens)
	print "Number of tokens : ", len(tokens)
	print "First words in tokens", tokens[:10]

	# Create an nltk text
	text = nltk.Text(tokens)
	print "We now have a new type of text", type(text)
	print "Here are the collocations", text.collocations()

	# Finding the begining and end of the main text
	start_of_text = raw.find("PART I")
	end_of_text = raw.rfind("End of Project Gutenberg's Crime")
	raw = raw[start_of_text:end_of_text]
	print "Main part of the text is", raw

# Working with HTML text
def process_htmltext():

	url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
	response = urllib2.urlopen(urllib2.Request(url))
	html = response.read().decode('utf8')

	print "First characters from the html", html[:80]
	raw = BeautifulSoup(html).get_text()
	tokens = word_tokenize(raw)
	print "First tokens of the html data", tokens[:30]



def process_rssfeed():

	url = "http://languagelog.ldc.upenn.edu/nll/?feed=atom"
	llog = feedparser.parse(url)

	print "Title of the feed", llog['feed']['title']

def process_localfile():
	f = open('document.txt')
	for line in f:
		print line.strip()


# Process of processing some text
def process_some_document(url):
	# Download document
	html = urllib2.urlopen(urllib2.Request(url))
	raw = nltk.clean_html(html)

	# Extract the text from it, trim the desired content
	raw = raw[20:1840]

	# Tokenize the text
	# tokens = nltk.wordpunct_tokenize(raw)
	tokens = word_tokenize(raw)
	text = nltk.Text(tokens)

	# Normalize the words, build the vocabulary
	words = [word.lower() for word in text]
	vocabulary = sorted(set(words))




process_rssfeed()